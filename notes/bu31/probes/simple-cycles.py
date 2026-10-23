import os,itertools,subprocess,random
os.environ['LC_ALL']='C';rng=random.Random(31033);total=0
for n in range(2,9):
 for k in range(100):
  nodes=list(range(n));rng.shuffle(nodes)
  pairs=[(nodes[i],nodes[(i+1)%n]) for i in range(n)];rng.shuffle(pairs)
  data=' '.join(chr(a+97)+' '+chr(b+97) for a,b in pairs).encode()
  g=subprocess.run(['.gnu-bin/bin/tsort'],input=data,capture_output=True)
  for tier in ['release','dev']:
   b=subprocess.run(['target/'+tier+'/tsort'],input=data,capture_output=True)
   if (g.returncode,g.stdout,g.stderr)!=(b.returncode,b.stdout,b.stderr):print('CYCLE-MISMATCH',data,tier,(g.returncode,g.stdout,g.stderr),(b.returncode,b.stdout,b.stderr));raise SystemExit(1)
  total+=1
print('SIMPLE-CYCLES',total,'cases per tier')
