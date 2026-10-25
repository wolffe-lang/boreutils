#!/usr/bin/env python3
"""Ordinary kernel-access parity and set-id effective-access NOT-YET rows.

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
    assert answers==[0,0],('ordinary ACL parity',answers)
    print('PARITY test -r ACL grant with equal ids: GNU 9.11=0; boreutils=0',flush=True)
    answers=[]
    for exe in [root/'.gnu-bin/bin/test',root/'target/release/test']:
        answers.append(subprocess.run(['setpriv','--ruid=0','--euid=1000','--rgid=0','--egid=1000','--clear-groups',str(exe),'-r',str(f)],env={**os.environ,'LC_ALL':'C'}).returncode)
    assert answers==[0,1],('set-id effective access exception',answers)
    print('NOT-YET set-id ACL read, real0/effective1000: GNU=0; mode-bit fallback=1',flush=True)
# CI and the lane mount the repository read-only, not the ephemeral /tmp.
f=root/'tests/fixtures/bu35-logins.utmp';answers=[]
for exe in [root/'.gnu-bin/bin/test',root/'target/release/test']:
    answers.append(subprocess.run([str(exe),'-w',str(f)],env={**os.environ,'LC_ALL':'C'}).returncode)
assert answers==[1,1],('ordinary read-only mount parity',answers)
print('PARITY test -w read-only bind with equal ids: GNU 9.11=1; boreutils=1',flush=True)
answers=[]
for exe in [root/'.gnu-bin/bin/test',root/'target/release/test']:
    answers.append(subprocess.run(['setpriv','--ruid=1000','--euid=0','--rgid=1000','--egid=0','--clear-groups',str(exe),'-w',str(f)],env={**os.environ,'LC_ALL':'C'}).returncode)
assert answers==[1,0],('set-id read-only mount exception',answers)
print('NOT-YET set-id read-only write, real1000/effective0: GNU=1; mode-bit fallback=0',flush=True)
print('effective access: 2 parity rows, 2 reviewed set-id NOT-YET rows, 0 unexpected failures',flush=True)
