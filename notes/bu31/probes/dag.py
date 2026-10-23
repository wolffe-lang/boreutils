#!/usr/bin/env python3
"""Exhaustive four-/five-node DAGs plus edge-order permutations.

GNU binary stdout is the expected order; validity alone is insufficient.
Run on hasu only. Seeded shuffle chooses input permutations, not answers.
"""
import itertools,json,os,random,subprocess,sys,time
from pathlib import Path
os.environ['LC_ALL']='C'
rng=random.Random(31031)
exe=['.gnu-bin/bin/tsort','target/release/tsort','target/dev/tsort']
counts={};total=0
for n in [3,4,5]:
 directed=list(itertools.permutations(range(n),2)); unique=set()
 # Every DAG has a topological ordering: enumerate all orders and all
 # forward-edge subsets, deduplicating the labeled directed graphs.
 for order in itertools.permutations(range(n)):
  possible=list(itertools.combinations(order,2))
  for mask in range(1<<len(possible)):
   edges=tuple(sorted(p for k,p in enumerate(possible) if mask>>k&1))
   unique.add(edges)
 counts[n]={'graphs':len(unique),'inputs':0}
 for graph in sorted(unique):
  variants=[list(graph)]
  if n<5 or rng.randrange(10)==0:
   variants += [list(reversed(graph)),rng.sample(list(graph),len(graph))]
  for pairs in variants:
   # Self pairs preserve isolated nodes and exercise their ordering.
   data=' '.join(chr(a+97)+' '+chr(b+97) for a,b in pairs+[(k,k) for k in range(n)]).encode()
   expected=subprocess.run([exe[0]],input=data,capture_output=True)
   for target in exe[1:]:
    got=subprocess.run([target],input=data,capture_output=True)
    if (expected.returncode,expected.stdout,expected.stderr)!=(got.returncode,got.stdout,got.stderr):
     print('DAG-MISMATCH',n,data,target,expected.returncode,expected.stdout,expected.stderr,got.returncode,got.stdout,got.stderr,flush=True)
     sys.exit(1)
   counts[n]['inputs']+=1;total+=1
   if total%1000==0:print('DAG-progress',total,flush=True)
print('DAG-RESULT',json.dumps(counts,sort_keys=True),'inputs',total,'comparisons',total*2,flush=True)
