import os,subprocess,tempfile
from pathlib import Path
with tempfile.TemporaryDirectory() as td:
 os.chdir(td);Path('f').write_bytes(b'abc')
 for algo in ['md5','sha1','sha224','sha256','sha384','sha512','sha2','blake2b']:
  for length in ([8,256,512] if algo=='blake2b' else [224,256,384,512] if algo=='sha2' else [None]):
   flags=['-a',algo]+(['-l',str(length)] if length else [])
   for format in [[],['--base64'],['--untagged'],['--base64','--untagged']]:
    made=subprocess.run(['cksum',*flags,*format,'f'],capture_output=True)
    for checkflags in [['-c'],['-c','-a',algo],['-c',*flags]]:
     p=subprocess.run(['cksum',*checkflags],input=made.stdout,capture_output=True)
     print(algo,length,format,checkflags,repr(made.stdout),'=>',p.returncode,repr(p.stdout),repr(p.stderr))
