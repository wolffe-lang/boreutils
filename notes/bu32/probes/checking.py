import os,subprocess,tempfile
from pathlib import Path
with tempfile.TemporaryDirectory() as td:
 os.chdir(td);Path('f').write_bytes(b'abc');Path('dir').mkdir();Path('-').write_bytes(b'abc');Path('car\rriage').write_bytes(b'abc')
 def run(args,data=b''):
  p=subprocess.run(args,input=data,capture_output=True);print(args,repr(data),p.returncode,repr(p.stdout),repr(p.stderr))
 good=b'900150983cd24fb0d6963f7d28e17f72  f\n'
 for args in [['cksum','-cw'],['cksum','-a','md5','-cw'],['b2sum','-cw'],['md5sum','-cw']]:
  for data in [b'bad\n',good+b'\n\n',b'  # hi\n'+good,b'\t'+good,b'kAFQmDzST7DWlj99KOF/cg==  f\n',b'MD5(f) = 900150983cd24fb0d6963f7d28e17f72\n',b'MD5 (f)=900150983cd24fb0d6963f7d28e17f72\n',b'MD5 (f) = kAFQmDzST7DWlj99KOF/cg==\n',b'BLAKE2b-8 (f) = 6b\n',b'6b  f\n',b'\\900150983cd24fb0d6963f7d28e17f72  f\n',good.replace(b'  f',b'  -'),good.replace(b'  f',b'  dir')]:run(args,data)
 for args in [['md5sum'],['md5sum','--tag'],['cksum'],['sum'],['md5sum','-c']]:run(args+['car\rriage'],good)
 for args in [['md5sum','-c','-b'],['md5sum','-c','-t'],['cksum','-c','--untagged'],['cksum','-c','--raw'],['cksum','-a','md5','--raw','f','f'],['cksum','-a','md5','--tag','--untagged','f']]:run(args,good)
