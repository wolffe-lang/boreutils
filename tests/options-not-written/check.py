#!/usr/bin/env python3
"""Complete-state and inherited-mask witnesses; GNU 9.11, container only.

Run in a disposable Linux container with BORE_OPTIONS_CONTAINER=1,
/bu36-mount tmpfs, and /lane/tmp/bu36-cp-source/mount tmpfs. No signals
are sent: subprocess preexec changes only that child's inherited mask.
"""
from pathlib import Path
import datetime as dt
import os
import signal
import subprocess
import tempfile
import time

ROOT = Path(__file__).resolve().parents[2]
assert os.environ.get('BORE_OPTIONS_CONTAINER') == '1', 'container witness only'
assert os.path.ismount('/bu36-mount'), 'disposable tmpfs required'
MOUNT = Path('/bu36-mount')
SOURCE = Path('/lane/tmp/bu36-cp-source')
assert os.path.ismount(SOURCE/'mount'), 'source-boundary tmpfs required'
ENV = dict(os.environ, LC_ALL='C', TZ='UTC0', _POSIX2_VERSION='200112')
COUNT = 0

def check(condition, label):
    global COUNT
    assert condition, label
    COUNT += 1
    print('ok', label, flush=True)

def run(binary, args, blocked=False):
    def block():
        signal.pthread_sigmask(signal.SIG_BLOCK, [signal.SIGPIPE])
    return subprocess.run([str(binary), *map(str,args)], env=ENV,
                          capture_output=True, timeout=10,
                          preexec_fn=block if blocked else None)

GNU = ROOT/'.gnu-bin/bin'
check(run(GNU/'ls',['--version']).stdout.splitlines()[0] == b'ls (GNU coreutils) 9.11', 'oracle identity')
for provider in [GNU, ROOT/'target/dev', ROOT/'target/release']:
    label = str(provider.relative_to(ROOT))
    (MOUNT/'sentinel').write_bytes(b'unchanged')
    r = run(provider/'rm',['--preserve-root=all','-r',MOUNT])
    expected = b"rm: skipping '/bu36-mount', since it's on a different device\nrm: and --preserve-root=all is in effect\n"
    check(r.returncode == 1 and r.stdout == b'' and r.stderr == expected and (MOUNT/'sentinel').read_bytes() == b'unchanged', label+' rm device refusal complete state')
    SOURCE.mkdir(exist_ok=True)
    (SOURCE/'root-file').write_text('root')
    (SOURCE/'mount'/'mounted-file').write_text('mounted')
    with tempfile.TemporaryDirectory(prefix='bu36-options-',dir=os.environ['TMPDIR']) as scratch:
        tmp=Path(scratch)
        for flag, name in [('-rx','bounded'),('-r','control')]:
            r=run(provider/'cp',[flag,SOURCE,tmp/name])
            check(r.returncode==0 and not r.stdout and not r.stderr,label+' cp '+flag+' status')
            check((tmp/name/'root-file').read_text()=='root',label+' cp '+flag+' ordinary file')
            check((tmp/name/'mount').is_dir(),label+' cp '+flag+' mountpoint directory exists')
            check((tmp/name/'mount'/'mounted-file').exists() == (flag=='-r'),label+' cp '+flag+' boundary contents')
        for date, shift in [('yesterday',-86400),('2 days ago',-172800),('tomorrow',86400)]:
            path=tmp/'stamp';path.write_bytes(b'body')
            before=time.time_ns();r=run(provider/'touch',['-d',date,path]);after=time.time_ns()
            t=path.stat()
            check(r.returncode==0 and before+shift*10**9-10**7 <= t.st_mtime_ns <= after+shift*10**9+10**7,label+' touch '+date+' independent clock bound')
            check(t.st_atime_ns==t.st_mtime_ns and path.read_bytes()==b'body',label+' touch '+date+' both times and bytes')
        path=tmp/'stamp';before=dt.datetime.now(dt.timezone.utc)
        r=run(provider/'touch',['-d','next monday',path]);after=dt.datetime.now(dt.timezone.utc)
        possible=set()
        for current in [before,after]:
            days=(7-current.weekday())%7
            if days==0: days=7
            possible.add(int((current.replace(hour=0,minute=0,second=0,microsecond=0)+dt.timedelta(days=days)).timestamp())*10**9)
        check(r.returncode==0 and path.stat().st_mtime_ns in possible,label+' touch next monday midnight')
    report='import signal; print(int(signal.SIGPIPE in signal.pthread_sigmask(signal.SIG_BLOCK, [])))'
    r=run(provider/'env',['--default-signal=PIPE','/usr/bin/python3','-c',report],blocked=True)
    if provider==GNU:
        check(r.returncode==0 and r.stdout==b'0\n',label+' default-signal actually unblocks inherited PIPE')
    else:
        check(r.returncode==125 and not r.stdout and b'no mask setter' in r.stderr,label+' blocked default-signal named refusal, never runs child')
        r=run(provider/'env',['--default-signal=PIPE','--ignore-signal=PIPE','/usr/bin/python3','-c',report],blocked=True)
        check(r.returncode==125 and not r.stdout and b'no mask setter' in r.stderr,label+' later ignore cannot hide an earlier unblock request')
        r=run(provider/'env',['--block-signal=PIPE','/usr/bin/python3','-c',report])
        check(r.returncode==125 and not r.stdout and b'no signal-mask setter' in r.stderr,label+' block-signal named refusal')
    r=run(provider/'env',['--list-signal-handling','true'],blocked=True)
    check(r.returncode==0 and f'PIPE       ({signal.SIGPIPE:2d}): BLOCK\n'.encode() in r.stderr,label+' lists actual inherited blocked PIPE')
print(f'options integration: {COUNT} passed, 0 failed, 0 skipped',flush=True)
