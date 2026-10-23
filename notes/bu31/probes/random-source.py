import subprocess,tempfile
from pathlib import Path
with tempfile.TemporaryDirectory(dir='/l/tmp') as t:
 for byte in [0,1,2,3,127,128,254,255]:
  p=Path(t)/'r';p.write_bytes(bytes([byte])*4096)
  for n in [2,3,4,5,8,10]:
   r=subprocess.run(['.gnu-bin/bin/shuf','--random-source='+str(p),'-i',f'1-{n}'],capture_output=True)
   print(byte,n,r.returncode,r.stdout,r.stderr)
