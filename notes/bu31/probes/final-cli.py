import os,subprocess,tempfile
from pathlib import Path
os.environ['LC_ALL']='C'
with tempfile.TemporaryDirectory(dir='/l/tmp') as t:
 a,b=str(Path(t)/'a'),str(Path(t)/'b')
 Path(a).write_text('L k A\n');Path(b).write_text('R k B\n')
 for opts in [['-j1','2'],['-j2','2'],['-j1'],['-j2'],['-j1','x'],['-o','1.2','2.2'],['-o','0','1.2','2.2'],['-o','0','-o','1.1'],['-o','auto','-o','1.1'],['-o','1.1','-o','auto'],['-1','1','-1','2'],['-1','2','-j','1']]:
  p=subprocess.run(['.gnu-bin/bin/join',*opts,a,b],capture_output=True);print('JOIN',opts,p.returncode,p.stdout,p.stderr)
