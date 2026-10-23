"""Test graph-walk hypotheses against binary observations, no source."""
import subprocess,itertools
pairs=list(itertools.permutations(range(3),2))
graphs=[]
for mask in range(64):
 edges=[p for k,p in enumerate(pairs) if mask>>k&1]
 data=' '.join(chr(a+97)+' '+chr(b+97) for a,b in edges)
 p=subprocess.run(['.gnu-bin/bin/tsort'],input=data.encode(),capture_output=True)
 loops=[]
 for line in p.stderr.decode().splitlines():
  if 'loop:' in line:loops.append([])
  elif loops:loops[-1].append(ord(line[-1])-97)
 if loops:graphs.append((edges,loops[0]))
for orient,mode,rot,rootorder in itertools.product(['in','out'],['asc','desc','first','last'],['first','last','min'],['asc','desc','first']):
 hits=0
 for edges,want in graphs:
  edges=edges.copy()
  nodes=sorted(set(sum((list(p) for p in edges),[])))
  while True:
   roots0=[x for x in nodes if not any(b==x for a,b in edges)]
   if not roots0:break
   nodes=[x for x in nodes if x not in roots0]
   edges=[(a,b) for a,b in edges if a not in roots0]
  if not nodes:continue
  roots=nodes if rootorder=='asc' else nodes[::-1] if rootorder=='desc' else list(dict.fromkeys(sum((list(p) for p in edges),[])))
  seen=set();path=[];got=[]
  def walk(x):
   global got
   if x in path:
    got=path[path.index(x):].copy()
    if orient=='in':got=[got[0]]+got[:0:-1]
    if rot=='last':got=got[-1:]+got[:-1]
    if rot=='min':
     n=got.index(min(got));got=got[n:]+got[:n]
    return True
   if x in seen:return False
   seen.add(x);path.append(x)
   successors=[a if orient=='in' else b for a,b in edges if (b if orient=='in' else a)==x]
   if mode=='asc':successors.sort()
   elif mode=='desc':successors.sort(reverse=True)
   elif mode=='last':successors.reverse()
   for y in successors:
    if walk(y):return True
   path.pop();return False
  for x in roots:
   if walk(x):break
  hits+=got==want
 print(hits,len(graphs),orient,mode,rot,rootorder)
