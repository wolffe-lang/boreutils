import os,subprocess,random,itertools
os.environ['LC_ALL']='C';rng=random.Random(31032)
for u in ['base64','base32']:
 cases=[bytes(x) for n in range(5) for x in itertools.product(b'A=B!\n',repeat=n)]
 cases += [bytes(rng.choice(b'ABZgz29+/=MY7!\r\n') for _ in range(rng.randrange(1,60))) for _ in range(1000)]
 for k,x in enumerate(cases):
  for opt in ['-d','-di']:
   g=subprocess.run(['.gnu-bin/bin/'+u,opt],input=x,capture_output=True)
   for tier in ['release','dev']:
    b=subprocess.run(['target/'+tier+'/'+u,opt],input=x,capture_output=True)
    if (g.returncode,g.stdout,g.stderr)!=(b.returncode,b.stdout,b.stderr):
     print('CODEC-MISMATCH',u,opt,x,tier,(g.returncode,g.stdout,g.stderr),(b.returncode,b.stdout,b.stderr),flush=True);raise SystemExit(1)
  if k%1000==0:print('CODEC-progress',u,k,flush=True)
 print('CODEC-RESULT',u,len(cases)*2,'cases per tier',flush=True)
