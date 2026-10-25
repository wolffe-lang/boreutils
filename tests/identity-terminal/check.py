#!/usr/bin/env python3
"""PTY state, synthetic utmp, independent date bounds and named refusals.

Run only in a disposable Linux container, with BORE_UTMP_CONTAINER=1.
Use --bin target/dev to repeat against the second tier. No compile skip.
"""
import argparse,copy,fcntl,os,pathlib,pty,re,struct,subprocess,termios,time
p=argparse.ArgumentParser();p.add_argument('--bin',default='target/release');args=p.parse_args()
ROOT=pathlib.Path(__file__).resolve().parents[2]
BIN=(ROOT/args.bin).resolve();GNU=ROOT/'.gnu-bin/bin'
if os.environ.get('BORE_UTMP_CONTAINER')!='1' or not pathlib.Path('/run/.containerenv').exists():
    raise SystemExit('REFUSED: identity/terminal integration requires its disposable container')
for u in ['date','test','[','uname','hostname','hostid','arch','users','who','uptime','pinky','pathchk','stty','chcon','runcon']:
    if not (BIN/u).is_file():raise SystemExit(f'REFUSED: missing {BIN/u}')
ENV={**os.environ,'LC_ALL':'C','TZ':'UTC0','_POSIX2_VERSION':'200112'}
passed=0

def run(exe,a,**kw):
    q=subprocess.run([str(exe),*a],capture_output=True,env=ENV,timeout=15,**kw)
    err=q.stderr.replace(str(exe).encode(),b'PROG')
    # Some errors mention the utility twice, not just as the line prefix.
    err=err.replace(exe.name.encode(),b'PROG')
    return q.returncode,q.stdout,err

def ok(name):
    global passed
    passed+=1;print('ok',name,flush=True)

def compare(u,a,**kw):
    actual=run(BIN/u,a,**kw);expected=run(GNU/u,a,**kw)
    assert actual==expected,(u,a,actual,expected)
    ok(u+' '+repr(a))

# A pty is opened by this test, never the operator's terminal. Compare
# all flags, both speeds, every control character and the full winsize.
master,slave=pty.openpty()
try:
    attrs=termios.tcgetattr(slave)
    win=fcntl.ioctl(slave,termios.TIOCGWINSZ,b'\0'*8)
    settings=[]
    for flag in ['echo','icanon','isig','ixon','iexten','icrnl','opost','istrip','cbreak']:
        settings += [[flag],['-'+flag]]
    settings += [['min','0'],['min','255'],['time','0'],['time','255'],
                 ['-echo','-icanon','min','7','time','3'],['size']]
    for a in settings:
        observed=[]
        for exe in [GNU/'stty',BIN/'stty']:
            termios.tcsetattr(slave,termios.TCSANOW,copy.deepcopy(attrs))
            fcntl.ioctl(slave,termios.TIOCSWINSZ,win)
            result=run(exe,a,stdin=slave)
            observed.append((result,termios.tcgetattr(slave),fcntl.ioctl(slave,termios.TIOCGWINSZ,b'\0'*8)))
        assert observed[0]==observed[1],('pty state',a,observed)
        ok('stty complete state '+repr(a))
    # -F reaches this same slave with stdin deliberately not a terminal.
    termios.tcsetattr(slave,termios.TCSANOW,copy.deepcopy(attrs))
    device=os.ttyname(slave)
    for exe in [GNU/'stty',BIN/'stty']:
        termios.tcsetattr(slave,termios.TCSANOW,copy.deepcopy(attrs))
        result=run(exe,['-F',device,'-echo'])
        assert result[0]==0,result
        assert not termios.tcgetattr(slave)[3]&termios.ECHO
    ok('stty -F reaches the named pty')
    unsupported={
      'c_iflag':'brkint ignbrk igncr ignpar imaxbel inlcr inpck iutf8 iuclc ixany ixoff parmrk tandem',
      'c_oflag':'bs0 bs1 cr0 cr1 cr2 cr3 ff0 ff1 nl0 nl1 ocrnl ofdel ofill olcuc onlcr onlret onocr tab0 tab1 tab2 tab3 tabs -tabs vt0 vt1',
      'c_cflag':'clocal cread crtscts cs5 cs6 cs7 cs8 cstopb hup hupcl parenb parodd cmspar',
      'c_lflag':'crterase crtkill ctlecho echoctl echoe echok echoke echonl echoprt extproc flusho noflsh prterase tostop xcase',
      'c_cc':'discard eof eol eol2 erase intr kill lnext quit rprnt start stop susp swtch werase',
      'speed':'0 50 75 110 134 150 200 300 600 1200 1800 2400 4800 9600 19200 38400 57600 115200 230400 460800 500000 576000 921600 1000000 1152000 1500000 2000000 2500000 3000000 3500000 4000000 ispeed ospeed',
      'other':'line rows cols columns drain -drain',
      'combinations':'raw -raw cooked -cooked crt dec decctlq -decctlq ek evenp -evenp lcase -lcase LCASE -LCASE litout -litout nl -nl oddp -oddp parity -parity pass8 -pass8 sane',
      'report':'-a -g'}
    counts={}
    for field,words in unsupported.items():
        counts[field]=0
        for word in words.split():
            termios.tcsetattr(slave,termios.TCSANOW,copy.deepcopy(attrs))
            result=run(BIN/'stty',[word,'1'] if field in ['c_cc'] or word in ['line','rows','cols','columns','ispeed','ospeed'] else [word],stdin=slave)
            assert result[0]==1 and b'unsupported' in result[2] and b'termios-issue.txt' in result[2],(field,word,result)
            assert termios.tcgetattr(slave)==attrs,('refusal changed terminal',word)
            counts[field]+=1;ok('stty named refusal '+field+' '+word)
    print('stty refusal census',counts,'total',sum(counts.values()),flush=True)
    saved=run(GNU/'stty',['-g'],stdin=slave)[1].decode().strip()
    result=run(BIN/'stty',[saved],stdin=slave)
    assert result[0]==1 and b'termios-issue.txt' in result[2],result
    assert termios.tcgetattr(slave)==attrs
    ok('stty complete saved state is explicitly refused')
finally:
    os.close(master);os.close(slave)

# Neither side observes another run's random clock. Named zones and
# all fixed epoch conversions compare against the actual pinned binary.
for zone in ['UTC0','EST5EDT','Europe/Berlin','Asia/Kathmandu','<+0330>-3:30']:
    ENV['TZ']=zone
    for epoch in ['@0','@-1.5','@946818245.123456789','@1604212200','@2208988800']:
        for fmt in ['%a|%A|%b|%B|%c|%C|%d|%D|%e|%F|%g|%G|%h|%H|%I|%j|%k|%l|%m|%M|%N|%p|%P|%q|%r|%R|%s|%S|%T|%u|%U|%V|%w|%W|%x|%X|%y|%Y|%z|%Z', '%z|%:z|%::z|%:::z', '%3N|%12N|%Ec|%Ex|%EX|%Od|%%|%Q']:
            compare('date',['-d',epoch,'+'+fmt])
ENV['TZ']='UTC0'
for date in ['2022-11-14 12:00 3 hours ago','14nov2022 9:02pm','11/14/22 2102','2022-11-14 UTC+05:30','2022-11-14 12:00 (nested (comment))','2022-11-14 -1 year','2022-11-14 1 fortnight','2022-11-14 (unclosed']:
    compare('date',['-d',date,'+%F %T.%N %s'])
start=time.time_ns();clock=run(BIN/'date',['+%s.%N']);end=time.time_ns()
assert clock[0]==0 and re.fullmatch(rb'-?[0-9]+\.[0-9]{9}\n',clock[1]),clock
seconds,nanos=clock[1].strip().split(b'.');got=int(seconds)*10**9+int(nanos)
assert start-1_000_000<=got<=end+1_000_000,(start,got,end)
ok('date clock shape and independent wall-clock interval')
for a in [['-s','2000-01-01'],['--resolution'],['--debug','-d','@0'],['-d','TZ="right/UTC" @0']]:
    r=run(BIN/'date',a);assert r[0]==1 and (b'unsupported' in r[2] or b'not implemented' in r[2]),(a,r)
    ok('date named gap '+repr(a))
ENV['TZ']='right/UTC'
r=run(BIN/'date',['-d','@0']);assert r[0]==1 and b'leap-second' in r[2],r
ok('date refuses a leap table from metadata');ENV['TZ']='UTC0'

# Require root INSIDE the container for replacing its own login database.
# No host file is mounted at /var/run/utmp.
if os.geteuid()!=0:raise SystemExit('REFUSED: synthetic live utmp requires container root')
utmp=pathlib.Path('/var/run/utmp');previous=utmp.read_bytes() if utmp.exists() else None
try:
    utmp.write_bytes((ROOT/'tests/fixtures/bu35-logins.utmp').read_bytes())
    for u,options in [('users',[[]]),('who',[[],['-a'],['-H'],['-Hu'],['-HT'],['-Ha'],['-q'],['-b'],['-d'],['-l'],['-p'],['-r'],['-t'],['am','i']]),('pinky',[[],['-w'],['-i'],['-q'],['-f'],['-s'],['-fi'],['-w','zed'],['amy']])]:
        for a in options:compare(u,a)
    # UTMP is not a supported GNU environment override, independently witnessed.
    utmp.write_bytes(b'')
    ENV['UTMP']=str(ROOT/'tests/fixtures/bu35-logins.utmp')
    for u in ['who','users']:compare(u,[])
    del ENV['UTMP']
    # Current uptime is independently shaped, with a plausible /proc duration.
    r=run(BIN/'uptime',[])
    assert r[0]==0 and re.fullmatch(rb' [0-9]{2}:[0-9]{2}:[0-9]{2}  up (?:[0-9]+ days? )? *[0-9]+:[0-9]{2},  0 users,  load average: [0-9]+\.[0-9]{2}, [0-9]+\.[0-9]{2}, [0-9]+\.[0-9]{2}\n',r[1]),r
    match=re.search(rb'up (?:(\d+) days? )? *(\d+):(\d+),',r[1]);days,hours,minutes=match.groups();reported=(int(days or 0)*24+int(hours))*60+int(minutes)
    expected=float(pathlib.Path('/proc/uptime').read_text().split()[0])/60
    assert 0<=expected-reported<2,(reported,expected)
    ok('uptime shape and independent procfs elapsed interval')
finally:
    if previous is None:utmp.unlink(missing_ok=True)
    else:utmp.write_bytes(previous)
print(f'identity-terminal: {passed} passed, 0 failed, 0 skipped',flush=True)
