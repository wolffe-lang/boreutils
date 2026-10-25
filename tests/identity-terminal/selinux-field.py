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
try:
    label=pathlib.Path('/proc/self/attr/current').read_bytes()
    print('FIELD_LSM_READ',repr(label),flush=True)
except OSError as error:
    label=None
    print('FIELD_LSM_READ_ERROR',error.errno,error.strerror,flush=True)
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
            if util=='runcon' and not args:
                print('FIELD_CURRENT_CONTEXT','GNU',repr(expected),'BORE',repr(actual),flush=True)
                if label is not None:
                    assert expected==(0,label+b'\n',b''),('GNU current label output is proc bytes plus one LF',label,expected)
            assert actual==expected,(util,args,actual,expected)
            passed+=1
            print('FIELD ok',util,repr(args),flush=True)
print(f'SELinux field: {passed} passed, 0 failed; NOT GNU 9.11 evidence')
