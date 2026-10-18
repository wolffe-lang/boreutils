#!/usr/bin/env bash
# bu27: more of what a `timeout` does (inside a throwaway container only). usage: tprobe2.sh TIMEOUT
T=$1
ulimit -c 0
cd "$(mktemp -d /tmp/tprobe.XXXXXX)" || exit 9
r() {
    perl -e 'use Time::HiRes qw(time); $t=time;
      $p=fork; if(!$p){ open(STDOUT,">out"); open(STDERR,">err"); exec @ARGV; exit 99 }
      $SIG{ALRM}=sub{ kill 9,$p; print "GUARD fired\n" }; alarm 8; waitpid($p,0); $s=$?;
      printf "  -> %s %d, %.1f s\n", ($s&127)?"signal":"exit", ($s&127)?($s&127):($s>>8), time-$t' -- "$@"
    printf '  out: %s\n' "$(tr '\n' '|' < out)"
    printf '  err: %s\n' "$(tr '\n' '|' < err)"
}
rs() {
    sig=$1; d=$2; shift 2
    perl -e 'use Time::HiRes qw(time sleep); $t=time; ($sig,$d)=(shift,shift);
      $p=fork; if(!$p){ open(STDOUT,">out"); open(STDERR,">err"); exec @ARGV; exit 99 }
      sleep $d; kill $sig, $p;
      $SIG{ALRM}=sub{ kill 9,$p; print "GUARD fired\n" }; alarm 8; waitpid($p,0); $s=$?;
      printf "  -> %s %d, %.1f s\n", ($s&127)?"signal":"exit", ($s&127)?($s&127):($s>>8), time-$t' -- "$sig" "$d" "$@"
    printf '  out: %s\n' "$(tr '\n' '|' < out)"
    printf '  err: %s\n' "$(tr '\n' '|' < err)"
}
c() { echo "== $*"; }
c -s STOP 0.3 sleep 1;            r $T -s STOP 0.3 sleep 1
c --foreground -s STOP 0.3 sleep 1; r $T --foreground -s STOP 0.3 sleep 1
c -v -s 0 0.3 sleep 1;            r $T -v -s 0 0.3 sleep 1
c -v -s EXIT 0.3 sleep 1;         r $T -v -s EXIT 0.3 sleep 1
c -v TERM to timeout;             rs TERM 0.3 $T -v 5 sleep 2
c -v -k 0.3 TERM to timeout;      rs TERM 0.3 $T -v -k 0.3 5 sh -c 'trap "" TERM; sleep 3'
c -v -s 32 --foreground;          r $T -v --foreground -s 32 0.3 sleep 1
c -p --foreground -s KILL;        r $T -p --foreground -s KILL 0.3 sleep 5
c -k 0 0.3 TERM-ignoring;         r $T -k 0 0.3 sh -c 'trap "" TERM; sleep 2'
c -k 1e-400 0.3 TERM-ignoring;    r $T -k 1e-400 0.3 sh -c 'trap "" TERM; sleep 2'
c -k -1 0.3 sleep 1;              r $T -k -1 0.3 sleep 1
c -k 0.3 0 TERM-ignoring;         r $T -k 0.3 0 sh -c 'trap "" TERM; sleep 1'
c 1e-9 true;                      r $T 1e-9 true
c 0.0005 sleep 1;                 r $T 0.0005 sleep 1
c --foreground -s SEGV 0.3 sleep 5;  r $T --foreground -s SEGV 0.3 sleep 5
c --foreground -s RTMIN 0.3 sleep 5; r $T --foreground -s RTMIN 0.3 sleep 5
c 0.3 a command that is its own group leader; r $T 0.3 setsid sleep 3
c 0.3 sh -c exec sleep in a new group then exit; r $T 0.3 sh -c 'setsid sleep 30 & echo $! > gc; wait'; kill -0 "$(cat gc)" 2>/dev/null && echo "  grandchild alive" || echo "  grandchild gone"; kill -9 "$(cat gc)" 2>/dev/null
c --signal=HUP --kill-after=0.2 -vp 0.3 TERM HUP-ignoring; r $T --signal=HUP --kill-after=0.2 -vp 0.3 sh -c 'trap "" HUP; sleep 2'
c -fv 0.2 sleep 1;                r $T -fv 0.2 sleep 1
c --sig=KILL 0.2 sleep 1;         r $T --sig=KILL 0.2 sleep 1
c --fore 0.2 sleep 1;             r $T --fore 0.2 sleep 1
c --k=0.1 0.2 sleep 1;            r $T --k=0.1 0.2 sleep 1
c --verbose=x;                    r $T --verbose=x 1 true
c the env passes;                 FOO=bar r $T 5 sh -c 'echo $FOO'
c a TTOU to timeout;              rs TTOU 0.3 $T 1 sleep 2
c a TTIN to timeout;              rs TTIN 0.3 $T 1 sleep 2
c USR1 twice;                     perl -e 'use Time::HiRes qw(sleep); $p=fork; if(!$p){exec @ARGV} sleep 0.3; kill "USR1",$p; sleep 0.2; kill "USR1",$p; waitpid($p,0); $s=$?; printf "  -> %s %d\n", ($s&127)?"signal":"exit", ($s&127)?($s&127):($s>>8)' -- $T 5 sh -c 'n=0; trap "n=\$((n+1)); echo got \$n" USR1; while [ \$n -lt 2 ]; do sleep 0.05; done; exit 5'
echo PROBE-DONE
