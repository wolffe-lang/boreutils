import subprocess,itertools
for x in ['a b a c','a c a b','a b a c b d c d','z x a y','a b c d e f','z z b b a a','a b b a a c c a','a b b c c b','c b b a a b','a b a c b a c a','a b b a c a','a b b c c a d e']:
 p=subprocess.run(['.gnu-bin/bin/tsort'],input=x.encode(),capture_output=True);print(x,repr(p.stdout),repr(p.stderr))
