import os,subprocess,tempfile
with tempfile.TemporaryDirectory() as td:
 os.chdir(td);open('f','wb').write(b'abc')
 for bits in range(8,513,8):
  row=[]
  for form in [[],['--base64'],['--untagged'],['--base64','--untagged']]:
   made=subprocess.run(['cksum','-a','blake2b','-l',str(bits),*form,'f'],capture_output=True)
   for check in [['-c'],['-c','-a','blake2b'],['-c','-a','blake2b','-l',str(bits)]]:
    p=subprocess.run(['cksum',*check],input=made.stdout,capture_output=True)
    row.append(p.returncode)
  print(bits,row,repr(made.stdout),flush=True)
