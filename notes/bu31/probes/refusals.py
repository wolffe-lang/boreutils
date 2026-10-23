"""Retain both measured answers for every explicitly refused fixture."""
import json,os,subprocess,tempfile,tomllib
from pathlib import Path
os.environ['LC_ALL']='C';root=Path.cwd()
with tempfile.TemporaryDirectory(dir='/l/tmp') as t:
 Path(t,'r').write_bytes(b'abcd'*100)
 for util in ['tsort','shuf']:
  for c in tomllib.loads((root/'tests/cases'/f'{util}.toml').read_text())['case']:
   if 'skip' not in c:continue
   row={'utility':util,'case':c['name'],'scope':c['skip'],'stdin':repr(c.get('stdin','').encode())}
   for side,exe in [('gnu',root/'.gnu-bin/bin'/util),('bore',root/'target/dev'/util)]:
    p=subprocess.run([str(exe),*c.get('args',[])],input=c.get('stdin','').encode(),cwd=t,capture_output=True)
    row[side]={'exit':p.returncode,'stdout':repr(p.stdout),'stderr':repr(p.stderr)}
   print(json.dumps(row,sort_keys=True))
