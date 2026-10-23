import os,random,subprocess,tempfile
from pathlib import Path
os.environ['LC_ALL']='C';rng=random.Random(31034)
flags={'comm':[[],['--check-order'],['--nocheck-order'],['--total'],['-12'],['--output-delimiter=']], 'join':[[],['--check-order'],['--nocheck-order'],['--header'],['--header','--check-order'],['-a1','-a2'],['-v1','-a2'],['-o','auto','-e','?','-a1','-a2'],['-o','0,1.1,2.1,1.9','-e','?'],['-i'],['-t',':'],['-t','']]}
with tempfile.TemporaryDirectory(dir='/l/tmp') as top:
 a,b=str(Path(top)/'a'),str(Path(top)/'b')
 for util in flags:
  for k in range(3000):
   content=[]
   for side in range(2):
    if util=='join':rows=[rng.choice([b'',b' ',b'a x',b'a  x\ty ',b'B Y',b'b',b'c:z',b'a\rX',b'\xff q']) for _ in range(rng.randrange(8))]
    else:rows=[rng.choice([b'',b'a',b'a',b'B',b'b',b'c',b'\xff']) for _ in range(rng.randrange(8))]
    if k%3!=0:rows.sort()
    content.append(b'\n'.join(rows)+(b'\n' if rows else b''))
   Path(a).write_bytes(content[0]);Path(b).write_bytes(content[1]);args=rng.choice(flags[util])+[a,b]
   g=subprocess.run(['.gnu-bin/bin/'+util,*args],capture_output=True)
   for tier in ['dev']:
    p=subprocess.run(['target/'+tier+'/'+util,*args],capture_output=True)
    if (g.returncode,g.stdout,g.stderr)!=(p.returncode,p.stdout,p.stderr):
     print('TEXT-MISMATCH',util,k,content,args[:-2],tier,(g.returncode,g.stdout,g.stderr),(p.returncode,p.stdout,p.stderr),flush=True);raise SystemExit(1)
   if k%1000==0:print('TEXT-progress',util,k,flush=True)
  print('TEXT-RESULT',util,3000,flush=True)
