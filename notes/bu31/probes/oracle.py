#!/usr/bin/env python3
"""GNU binaries only; never reads implementation source."""
import os, subprocess, tempfile
from pathlib import Path
os.environ['LC_ALL']='C'
BIN=Path('.gnu-bin/bin').resolve()
def run(u,args=(),data=b''):
 p=subprocess.run([str(BIN/u),*args],input=data,capture_output=True)
 print(repr((u,args,data[:100])), '=>', p.returncode,repr(p.stdout),repr(p.stderr))
for u in ('base64','base32','comm','join','tsort','shuf'):
 p=subprocess.run(['.gnu-bin/bin/'+u,'--help'],capture_output=True); print(p.stdout.decode())
for u, good in [('base64',b'Zg=='),('base32',b'MY======')]:
 for data in [b'',good,good[:-1],good.rstrip(b'='),good+b'A',good+good,good+b'!',good+b'\r\n',b'\n'+good,good.replace(b'=',b''),b'=',b'====',b'AA',b'AAA',b'AAAA',b'AAAAA',b'AAAAAA',b'AAAAAAA',b'AAAAAAAA',good.lower()]:
  run(u,['-d'],data);run(u,['-di'],data)
 for args in [['-w','-1'],['-w','+4'],['-w','x'],['-w',''],['x','y'],['/']]: run(u,args,b'a')
with tempfile.TemporaryDirectory(dir='/l/tmp') as t:
 os.chdir(t)
 # preserve absolute binary path after chdir
 def files(a,b): Path('a').write_bytes(a);Path('b').write_bytes(b)
 for a,b in [(b'b\na\n',b''),(b'b\na\n',b'c\n'),(b'b\na\n',b'b\na\n'),(b'a\nc\nb\n',b'a\nc\nb\n'),(b'a\na\n',b'a\n')]:
  files(a,b)
  for flags in [[],['--check-order'],['--nocheck-order'],['-123'],['--total']]:run('comm',flags+['a','b'])
 for flags in [['--output-delimiter='],['--output-delimiter=x','--output-delimiter=y'],['-z','--total']]:run('comm',flags+['a','b'])
 for a,b in [(b'b B\na A\n',b''),(b'b B\na A\n',b'b X\na Y\n'),(b'a A\nc C\nb B\n',b'a X\nc X\nb X\n'),(b'a A1\na A2\n',b'a B1\na B2\n'),(b' a  A  \n',b'a B\n')]:
  files(a,b)
  for flags in [[],['--check-order'],['--nocheck-order'],['-a1'],['-v1'],['--header']]:run('join',flags+['a','b'])
 for flags in [['-t',''],['-o','auto'],['-o','0,1.1,2.1,1.9'],['-o','3.1'],['-1','0'],['-t','xx'],['-e','?','-a1']]:run('join',flags+['a','b'])
for data in [b'a b b c',b'a b a b',b'b b a a c c',b'a b c d',b'a b c b d a',b'a b b a',b'a b b a c d d c',b'a b b c c a',b'a b c',b'a\vb\fc\rd',b'a\x00b c']:
 run('tsort',data=data)
for args in [[],['a','b'],['-e'],['-i','3-1'],['-i','1-0'],['-i','0-0','-n','0'],['-r','-n','2'],['-n','-1'],['-n','x'],['-i','+1-3'],['-i','1-3','x'],['--random-source=/dev/null','-e','x'],['--random-source=/dev/null','-e','x','y']]:run('shuf',args)
for args in [['-a','3'],['-v','0'],['-1','x'],['-j','+2'],['-o',''],['-o','1.0'],['-o','x'],['-o','1.1,,2.1'],['-t',':','-t',';'],['-e','x','-e','y'],['--check-order'],['-t','\\0']]:run('join',args+['/dev/null','/dev/null'])
for data in [b'b\vc',b'b\fc',b'b\rc',b'b\tc',b'b\nc',b'b c',b'b\x00x c',b'b\x00x c c d']:
 run('tsort',data=data)
for x in [' 2','2 ','-0','+0','18446744073709551615','18446744073709551616','9223372036854775808','0002','2x','+','\t2']:
 for u,args in [('base64',['-w',x]),('shuf',['-n',x,'-e','a']),('join',['-1',x,'/dev/null','/dev/null'])]:run(u,args,b'a')
for x in ['9223372036854775808-9223372036854775808','18446744073709551615-18446744073709551615','0-18446744073709551615','0-18446744073709551614','18446744073709551616-18446744073709551616','-0-1','1--0']:
 run('shuf',['-i',x,'-n','1'])
for x in ['+1','01',' 1','-0','3']:
 run('join',['-a',x,'/dev/null','/dev/null'])
