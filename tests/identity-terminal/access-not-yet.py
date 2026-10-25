#!/usr/bin/env python3
"""Reviewed NOT-YET rows: effective access differs from mode-bit access.

Only a disposable container's own files/ids, plus a read-only source bind.
Requires acl's setfacl in the container, never a host package.
"""
import os,pathlib,shutil,subprocess,tempfile
if os.environ.get('BORE_UTMP_CONTAINER')!='1' or os.geteuid()!=0:
    raise SystemExit('REFUSED: access witnesses require disposable container root')
root=pathlib.Path(__file__).resolve().parents[2]
if not shutil.which('setfacl') or not shutil.which('setpriv'):
    raise SystemExit('REFUSED: install acl and util-linux inside the container')
with tempfile.TemporaryDirectory(prefix='bu35-acl-') as d:
    os.chmod(d,0o755)
    f=pathlib.Path(d)/'f';f.write_text('x');os.chmod(f,0)
    subprocess.run(['setfacl','-m','u:1000:r--',str(f)],check=True)
    answers=[]
    for exe in [root/'.gnu-bin/bin/test',root/'target/release/test']:
        q=subprocess.run(['setpriv','--reuid=1000','--regid=1000','--clear-groups',str(exe),'-r',str(f)],env={**os.environ,'LC_ALL':'C'})
        answers.append(q.returncode)
    assert answers==[0,1],('ACL expected GNU true / mode-bit false',answers)
    print('NOT-YET test -r ACL grant: GNU 9.11=0; mode-bit test=1; wolf-lang#685, effective-access issue draft',flush=True)
# CI and the lane mount the repository read-only, not the ephemeral /tmp.
f=root/'tests/fixtures/bu35-logins.utmp';answers=[]
for exe in [root/'.gnu-bin/bin/test',root/'target/release/test']:
    answers.append(subprocess.run([str(exe),'-w',str(f)],env={**os.environ,'LC_ALL':'C'}).returncode)
assert answers==[1,0],('read-only bind expected GNU false / mode-bit true',answers)
print('NOT-YET test -w read-only bind: GNU 9.11=1; mode-bit test=0; effective-access issue draft',flush=True)
print('access exceptions: 2 reviewed not-yet rows, 0 unexpected failures',flush=True)
