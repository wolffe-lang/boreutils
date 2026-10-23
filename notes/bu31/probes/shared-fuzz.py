import os,random,subprocess
os.environ['LC_ALL']='C';r=random.Random(31035)
for k in range(1500):
 data=b'\n'.join(r.choice([b'',b'a',b'b',b'c',b'\xff']) for _ in range(r.randrange(13)))
 if r.randrange(2):data+=b'\n'
 opts=r.choice([[],['--check-order'],['--nocheck-order'],['--total'],['-123'],['-z']])
 if opts==['-z']:data=data.replace(b'\n',b'\0')
 g=subprocess.run(['.gnu-bin/bin/comm',*opts,'-','-'],input=data,capture_output=True)
 for tier in ['release','dev']:
  b=subprocess.run(['target/'+tier+'/comm',*opts,'-','-'],input=data,capture_output=True)
  if (g.returncode,g.stdout,g.stderr)!=(b.returncode,b.stdout,b.stderr):
   print('SHARED-MISMATCH',data,opts,tier,(g.returncode,g.stdout,g.stderr),(b.returncode,b.stdout,b.stderr),flush=True);raise SystemExit(1)
 if k%500==0:print('SHARED-progress',k,flush=True)
print('SHARED-RESULT',1500,'cases per tier',flush=True)
