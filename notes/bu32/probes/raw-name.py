import os, subprocess, tempfile
with tempfile.TemporaryDirectory() as td:
 os.chdir(td)
 with open(b'bad\xff', 'wb') as f:f.write(b'abc')
 data=b'900150983cd24fb0d6963f7d28e17f72  bad\xff\n'
 for path in ['/l/boreutils/.gnu-bin/bin/md5sum','/l/boreutils/target/release/md5sum']:
  p=subprocess.run([path,'-c'],input=data,capture_output=True,env=dict(os.environ,LC_ALL='C'))
  print(path,p.returncode,repr(p.stdout),repr(p.stderr))
