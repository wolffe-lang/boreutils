import os,subprocess,tempfile
with tempfile.TemporaryDirectory() as td:
 os.chdir(td);os.mkdir('d')
 for tool in ['cksum','md5sum','b2sum']:
  for args,close in [(['-c','d'],False),(['-c'],True),([],True)]:
   for root in ['/l/boreutils/.gnu-bin/bin','/l/boreutils/target/release']:
    p=subprocess.run([root+'/'+tool,*args],capture_output=True,env=dict(os.environ,LC_ALL='C'),preexec_fn=(lambda:os.close(0)) if close else None)
    print(tool,args,'closed0='+str(close),root,p.returncode,repr(p.stdout),repr(p.stderr))
