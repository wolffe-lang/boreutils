"""bu36 black-box derivation attempts, GNU manual/binary only."""
from pathlib import Path
import subprocess,itertools,json,random,hashlib
root=Path('/lane');repo=root/'boreutils';ev=root/'ev';gnu=repo/'.gnu-bin/bin'
env={'PATH':str(gnu)+':/usr/bin:/bin','LC_ALL':'C','_POSIX2_VERSION':'200112','TZ':'UTC0'}
def run(util,args=(),data=b''):
 p=subprocess.run([str(gnu/util),*args],input=data,capture_output=True,env=env,timeout=5)
 return {'exit':p.returncode,'stdout':p.stdout.decode('ascii','backslashreplace'),'stderr':p.stderr.decode('ascii','backslashreplace')}
# Read published doc nodes only, never archive/source contents.
doc=''.join(p.read_text(errors='replace') for p in (repo/'.gnu-bin/share/info').glob('coreutils.info*') if p.suffix!='.gz')
with (ev/'refusal-documentation.txt').open('w') as f:
 for title in ['shuf invocation','Random sources','tsort invocation','tsort background']:
  for node in doc.split('\x1f'):
   if 'Node: '+title+',' in node or 'Node: '+title+'\n' in node:f.write(node+'\n')
inputs={f'constant-{v}':bytes([v])*4096 for v in [0,1,2,3,127,128,254,255]}
inputs.update({'ascending':bytes(range(256))*16,'descending':bytes(range(255,-1,-1))*16,'alternating':b'\x00\xff'*2048,'seed-36':random.Random(36).randbytes(4096)})
for length in [0,1,2,3,7,8,16]:inputs[f'short-{length}']=bytes(range(length))
records=[]
for name,data in inputs.items():
 path=root/'tmp'/('draw-'+name);path.write_bytes(data)
 for n in [2,3,4,5,8,10,17,257]:
  r=run('shuf',['--random-source='+str(path),'-i','0-'+str(n-1)])
  records.append({'source':name,'sha256':hashlib.sha256(data).hexdigest(),'length':len(data),'n':n,'gnu':r})
(ev/'shuf-attempt.jsonl').write_text(''.join(json.dumps(x,sort_keys=True)+'\n' for x in records))
# Simple unbiased byte-rejection and modulo candidates for full Fisher-Yates.
hyp=[]
for mode in ['modulo','rejection']:
 for direction in ['forward','backward']:
  good=0;bad=[]
  for r in records:
   if r['gnu']['exit']!=0:continue
   data=inputs[r['source']];n=r['n'];a=list(range(n));at=0
   try:
    for k in (range(n-1) if direction=='forward' else range(n-1,0,-1)):
     bound=n-k if direction=='forward' else k+1
     while True:
      value=data[at];at+=1
      if mode=='modulo' or value<256//bound*bound:break
     index=(k if direction=='forward' else 0)+value%bound
     a[k],a[index]=a[index],a[k]
    predicted=''.join(str(x)+'\n' for x in a)
   except IndexError:predicted='source exhausted'
   if predicted==r['gnu']['stdout']:good+=1
   elif len(bad)<2:bad.append({'source':r['source'],'n':n,'predicted':predicted,'gnu':r['gnu']})
  hyp.append({'mode':mode,'direction':direction,'matches':good,'compared':sum(x['gnu']['exit']==0 for x in records),'counterexamples':bad})
(ev/'shuf-hypotheses.json').write_text(json.dumps(hyp,indent=2))
# All 3-node directed graphs, plus deterministic 4-node graphs and order variants.
pairs=list(itertools.permutations('abc',2));graphs=[]
for mask in range(64):graphs.append([p for k,p in enumerate(pairs) if mask>>k&1])
rng=random.Random(36);p4=list(itertools.permutations('abcd',2))
for _ in range(256):
 edges=[p for p in p4 if rng.randrange(2)];rng.shuffle(edges);graphs.extend([edges,edges[::-1]])
observed=[]
for edges in graphs:
 data=' '.join(' '.join(e) for e in edges).encode();r=run('tsort',data=data)
 cycles=[]
 for line in r['stderr'].splitlines():
  if 'input contains a loop:' in line:cycles.append([])
  elif cycles:cycles[-1].append(line.removeprefix('tsort: '))
 observed.append({'input':data.decode(),'edges':edges,'cycles':cycles,'gnu':r})
(ev/'tsort-attempt.jsonl').write_text(''.join(json.dumps(x,sort_keys=True)+'\n' for x in observed))
variants=[]
for orient,adjorder,rootorder,rotation in itertools.product(['in','out'],['asc','desc','first','last'],['asc','desc','first'],['first','last','min']):
 hits=0;compared=0;bad=[]
 for obs in observed:
  if not obs['cycles']:continue
  compared+=1;edges=[tuple(x) for x in obs['edges']];nodes=sorted(set(itertools.chain.from_iterable(edges)))
  while True:
   roots=[n for n in nodes if not any(b==n for a,b in edges)]
   if not roots:break
   nodes=[n for n in nodes if n not in roots];edges=[(a,b) for a,b in edges if a not in roots]
  roots=nodes if rootorder=='asc' else nodes[::-1] if rootorder=='desc' else list(dict.fromkeys(x for e in edges for x in e if x in nodes))
  seen=set();path=[];found=[]
  def visit(x):
   if x in path:
    found.extend(path[path.index(x):]);return True
   if x in seen:return False
   seen.add(x);path.append(x)
   ns=[a if orient=='in' else b for a,b in edges if (b if orient=='in' else a)==x]
   if adjorder=='asc':ns.sort()
   if adjorder=='desc':ns.sort(reverse=True)
   if adjorder=='last':ns.reverse()
   for y in ns:
    if visit(y):return True
   path.pop();return False
  for n in roots:
   if visit(n):break
  if orient=='in' and found:found=[found[0],*found[:0:-1]]
  if found and rotation=='last':found=found[-1:]+found[:-1]
  if found and rotation=='min':k=found.index(min(found));found=found[k:]+found[:k]
  if found==obs['cycles'][0]:hits+=1
  elif not bad:bad=[{'input':obs['input'],'predicted_first_cycle':found,'gnu':obs['gnu'],'cycles':obs['cycles']}]
 variants.append({'orientation':orient,'adjacency':adjorder,'roots':rootorder,'rotation':rotation,'matches':hits,'compared':compared,'counterexample':bad})
variants.sort(key=lambda x:-x['matches']);(ev/'tsort-hypotheses.json').write_text(json.dumps(variants,indent=2))
print('shuf',len(records),'oracle rows;',[(x['mode'],x['direction'],x['matches'],x['compared']) for x in hyp])
print('tsort',len(observed),'oracle rows;',len(variants),'walk hypotheses; best',variants[0])
print('RECOMMEND retain #49/#50 named refusals; none of the tested general hypotheses fits all measurements. This is not proof black-box derivation is impossible.')
