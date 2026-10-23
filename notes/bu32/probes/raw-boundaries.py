import os,subprocess,tempfile
H=b'900150983cd24fb0d6963f7d28e17f72';good=H+b'  f\n'
with tempfile.TemporaryDirectory() as td:
 os.chdir(td);open('f','wb').write(b'abc');open(b'(x)\xff','wb').write(b'abc')
 for name,data in [('bad-escape',good+b'\\'+H+b'  bad\\q\xff\n'+good),('bad-marker',good+H+b' \xff\n'+good),('parenthesized-raw',good+H+b'  (x)\xff\n')]:
  for root in ['/l/boreutils/.gnu-bin/bin','/l/boreutils/target/release']:
   p=subprocess.run([root+'/md5sum','-c'],input=data,capture_output=True,env=dict(os.environ,LC_ALL='C'))
   print(name,root,p.returncode,repr(p.stdout),repr(p.stderr),flush=True)
