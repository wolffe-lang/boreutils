#!/usr/bin/env python3
"""GNU 9.11 black-box CLI discovery; no implementation source."""
import os, subprocess, tempfile
from pathlib import Path
with tempfile.TemporaryDirectory() as td:
 os.chdir(td)
 Path('f').write_bytes(b'abc'); Path('empty').touch(); Path('back\\slash').write_bytes(b'abc'); Path('new\nline').write_bytes(b'abc')
 def run(tool,args, data=b'abc'):
  p=subprocess.run([tool,*args],input=data,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  print(tool,repr(args),repr(data),'=>',p.returncode,repr(p.stdout),repr(p.stderr),flush=True)
 for a in ['crc','crc32b','sysv','bsd','md5','sha1','sha2','blake2b']:
  for args in [[],['-'],['f'],['empty'],['f','empty'],['--tag','f'],['--untagged','f'],['--base64','f'],['--raw','f'],['--zero','f'],['--tag','back\\slash'],['--tag','new\nline']]:
   run('cksum',['-a',a,*args])
 for args in [['-r'],['-s'],['-r','-'],['-s','-'],['-r','f'],['-s','f'],['-r','f','empty'],['-s','back\\slash']]: run('sum',args)
 for tool in ['cksum','md5sum','b2sum']:
  for args in [['--quiet'],['--status'],['--strict'],['-w'],['--ignore-missing'],['-c','-z'],['-c','--tag'],['--tag','-t'],['-t','--tag'],['--raw','--base64'],['-a','crc','-c'],['-l','0'],['-l','1'],['-l','513'],['-l','256'],['-l','+8'],['-l','-1'],['-l','bad'],['--debug'],['-a','bad'],['-a','sha2','-l','0'],['-a','sha2','-l','1']]: run(tool,args)
 good=b'900150983cd24fb0d6963f7d28e17f72  f\n'
 for data in [b'',b'junk\n',b'# comment\n',good,good.upper(),good.replace(b'  f',b' f'),good.replace(b'  f',b' *f'),good.replace(b'  f',b'\tf'),good.replace(b'  f',b'  missing'),good.replace(b'9001',b'0001'),b'MD5 (f) = 900150983cd24fb0d6963f7d28e17f72\n',b'crc (f) = 1219131554\n',b'1219131554 3 f\n',good+b'junk\n',good+b'00000000000000000000000000000000  empty\n']:
  for args in [['-c'],['-c','-w'],['-c','--status'],['-c','--quiet'],['-c','--strict'],['-c','--ignore-missing']]:run('md5sum',args,data)
 for args in [['-c'],['-a','md5','-c'],['-a','crc32b','-c'],['-a','sysv','-c']]:
  for data in [good,b'MD5 (f) = 900150983cd24fb0d6963f7d28e17f72\n',b'CRC32B (f) = 352441c2\n',b'1219131554 3 f\n',b'294 1 f\n']:run('cksum',args,data)
