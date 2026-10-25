#!/usr/bin/env python3
"""FIELD information only: pinned GNU 9.11 omits these two programs.

Run inside a disposable Ubuntu container with BORE_UTMP_CONTAINER=1.
Never call these field comparisons a 9.11 oracle verdict.
"""
import os,re,subprocess,tempfile,pathlib
if os.environ.get('BORE_UTMP_CONTAINER')!='1':
    raise SystemExit('REFUSED: SELinux field cases require the lane container')
root=pathlib.Path(__file__).resolve().parents[2]
cases={'runcon':[[],['u:r:t','/usr/bin/true'],['junk','/usr/bin/true'],['-t','t','/usr/bin/true'],['-c','/usr/bin/true'],['u:r:t']],
       'chcon':[[],['u:r:t','f'],['u:r:t','missing'],['--reference=f','g'],['--reference=missing','g'],['-t','t','f'],['-v','u:r:t','f'],['-f','u:r:t','f'],['junk','f']]}
passed=0
for util,argslist in cases.items():
    field='/usr/bin/'+util
    version=subprocess.run([field,'--version'],capture_output=True,check=True).stdout.splitlines()[0]
    print('FIELD',version.decode(),flush=True)
    for args in argslist:
        with tempfile.TemporaryDirectory(prefix='bu35-selinux-') as d:
            for f in ['f','g']:(pathlib.Path(d)/f).write_text(f)
            def run(exe):
                p=subprocess.run([str(exe),*args],cwd=d,env={**os.environ,'LC_ALL':'C'},capture_output=True)
                return p.returncode,p.stdout,p.stderr.replace(str(exe).encode(),b'PROG').replace(util.encode(),b'PROG')
            expected=run(field)
            actual=run(root/'target/release'/util)
            assert actual==expected,(util,args,actual,expected)
            passed+=1
            print('FIELD ok',util,repr(args),flush=True)
print(f'SELinux field: {passed} passed, 0 failed; NOT GNU 9.11 evidence')
