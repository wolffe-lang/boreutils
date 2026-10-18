#!/usr/bin/env bash
# bu27: what a `timeout` does, black-box. Run INSIDE a throwaway container only (box.sh): every
# signal here goes to a process this script started, or to the group the timeout under test leads.
# usage: tprobe.sh TIMEOUT-PROGRAM   (GNU's /g/bin/timeout, or ours)
T=$1
ulimit -c 0
cd "$(mktemp -d /tmp/tprobe.XXXXXX)" || exit 9
# r CMD...: run, guard 15 s; print how it ended (raw wait status), elapsed, its stdout and stderr.
r() {
    perl -e 'use Time::HiRes qw(time); $t=time; pipe(R,W);
      $p=fork; if(!$p){ open(STDOUT,">out"); open(STDERR,">err"); exec @ARGV; exit 99 }
      $SIG{ALRM}=sub{ kill 9,$p; print "GUARD fired\n" }; alarm 15; waitpid($p,0); $s=$?;
      printf "  -> %s %d, %.1f s\n", ($s&127)?"signal":"exit", ($s&127)?($s&127):($s>>8), time-$t' -- "$@"
    printf '  out: %s\n' "$(od -An -c out | tr -s ' ' | tr -d '\n')"
    printf '  err: %s\n' "$(sed 's/^/        /' err | tr '\n' '|')"
}
# rs SIG DELAY CMD...: as r, and send SIG to the program DELAY seconds after it starts.
rs() {
    sig=$1; d=$2; shift 2
    perl -e 'use Time::HiRes qw(time sleep); $t=time; ($sig,$d)=(shift,shift);
      $p=fork; if(!$p){ open(STDOUT,">out"); open(STDERR,">err"); exec @ARGV; exit 99 }
      sleep $d; kill $sig, $p;
      $SIG{ALRM}=sub{ kill 9,$p; print "GUARD fired\n" }; alarm 15; waitpid($p,0); $s=$?;
      printf "  -> %s %d, %.1f s\n", ($s&127)?"signal":"exit", ($s&127)?($s&127):($s>>8), time-$t' -- "$sig" "$d" "$@"
    printf '  out: %s\n' "$(od -An -c out | tr -s ' ' | tr -d '\n')"
    printf '  err: %s\n' "$(sed 's/^/        /' err | tr '\n' '|')"
}
c() { echo "== $*"; }
printf '#!/bin/sh\necho noshebang ran\n' > noshebang; chmod +x noshebang
printf 'x\n' > plain
c "statuses"
c 0.3 sleep 5;                      r $T 0.3 sleep 5
c -s KILL 0.3 sleep 5;              r $T -s KILL 0.3 sleep 5
c -k 0.3 0.3 TERM-ignoring;         r $T -k 0.3 0.3 sh -c 'trap "" TERM; sleep 5'
c --foreground -k 0.3 0.3 TERM-ignoring; r $T --foreground -k 0.3 0.3 sh -c 'trap "" TERM; sleep 5'
c --foreground -s KILL 0.3 sleep 5; r $T --foreground -s KILL 0.3 sleep 5
c -p 0.3 sleep 5;                   r $T -p 0.3 sleep 5
c -p -s KILL 0.3 sleep 5;           r $T -p -s KILL 0.3 sleep 5
c -p -s HUP 0.3 sleep 5;            r $T -p -s HUP 0.3 sleep 5
c 5 exit 3;                         r $T 5 sh -c 'exit 3'
c 5 the command ends by TERM;       r $T 5 sh -c 'kill -TERM $$'
c 5 the command ends by SEGV;       r $T 5 sh -c 'kill -SEGV $$'
c 5 the command ends by KILL;       r $T 5 sh -c 'kill -KILL $$'
c -p 5 the command ends by TERM;    r $T -p 5 sh -c 'kill -TERM $$'
c 5 not found;                      r $T 5 /nonexistent/x
c 5 not found bare;                 r $T 5 no-such-command-bu27
c 5 a plain file;                   r $T 5 ./plain
c 5 a directory;                    r $T 5 /tmp
c 5 no shebang;                     r $T 5 ./noshebang
c 0 sleep 0.2;                      r $T 0 sleep 0.2
c 0.3 trap TERM and exit 3;         r $T 0.3 sh -c 'trap "echo got TERM; exit 3" TERM; sleep 5 & wait'
c -p 0.3 trap TERM and exit 3;      r $T -p 0.3 sh -c 'trap "echo got TERM; exit 3" TERM; sleep 5 & wait'
c "usage"
c none;                             r $T
c 1;                                r $T 1
c x true;                           r $T x true
c -s FOO 1 true;                    r $T -s FOO 1 true
c --bogus;                          r $T --bogus 1 true
c -k x 1 true;                      r $T -k x 1 true
c 1 -s KILL true;                   r $T 1 -s KILL true
c -- 1 true;                        r $T -- 1 true
c -s;                               r $T -s
c --signal=9 0.3 sleep 5;           r $T --signal=9 0.3 sleep 5
c -s 0 0.3 sleep 1;                 r $T -s 0 0.3 sleep 1
c -s EXIT 0.3 sleep 1;              r $T -s EXIT 0.3 sleep 1
c -s CONT 0.3 sleep 1;              r $T -s CONT 0.3 sleep 1
c -s SEGV 0.3 sleep 5;              r $T -s SEGV 0.3 sleep 5
c -s RTMIN 0.3 sleep 5;             r $T -s RTMIN 0.3 sleep 5
c -s USR1 0.3 sleep 5;              r $T -s USR1 0.3 sleep 5
c -s CHLD 0.3 sleep 1;              r $T -s CHLD 0.3 sleep 1
c -s TTOU 0.3 sleep 1;              r $T -s TTOU 0.3 sleep 1
c -v 0.3 sleep 5;                   r $T -v 0.3 sleep 5
c -v -k 0.3 0.3 TERM-ignoring;      r $T -v -k 0.3 0.3 sh -c 'trap "" TERM; sleep 5'
c -v -s 9 0.3 sleep 5;              r $T -v -s 9 0.3 sleep 5
c -v --foreground -s RTMIN+2 0.3 sleep 5; r $T -v --foreground -s RTMIN+2 0.3 sleep 5
c --help;                           r $T --help
c --version;                        r $T --version
c "durations"
for d in 0.1 .1 0.1s 1e-1 0x.2 0x1p-3 " 0.1" "0.1 " -0 -1 -0.1 +0.1 0.1x 0.1S 1d 1m 1h inf infinity INF nan 1e100 1e-400 99999999999999999999 0x 1.5.2 "" ss 1ss; do
  c "duration [$d] true"; r $T "$d" true
done
c "the group and the child"
c 0.3 a grandchild;                 r $T 0.3 sh -c 'sleep 30 & echo $! > gc; wait'; sleep 0.3; kill -0 "$(cat gc)" 2>/dev/null && echo "  grandchild alive" || echo "  grandchild gone"; kill -9 "$(cat gc)" 2>/dev/null
c --foreground 0.3 a grandchild;    r $T --foreground 0.3 sh -c 'sleep 30 & echo $! > gc; wait'; sleep 0.3; kill -0 "$(cat gc)" 2>/dev/null && echo "  grandchild alive" || echo "  grandchild gone"; kill -9 "$(cat gc)" 2>/dev/null
c "pgid: timeout's, the command's, and the script's $$ (pgid $(cut -d' ' -f5 /proc/$$/stat))"
r $T 5 sh -c 'echo "cmd pid $$ pgid $(cut -d" " -f5 /proc/$$/stat) sid $(cut -d" " -f6 /proc/$$/stat); timeout pid $PPID pgid $(cut -d" " -f5 /proc/$PPID/stat)"'
r $T --foreground 5 sh -c 'echo "cmd pid $$ pgid $(cut -d" " -f5 /proc/$$/stat); timeout pid $PPID pgid $(cut -d" " -f5 /proc/$PPID/stat)"'
c "setsid: a session leader cannot move";  r setsid $T 0.3 sh -c 'echo "pgid $(cut -d" " -f5 /proc/$PPID/stat) of timeout $PPID"; sleep 5'
c "the command's signal state (and this script's)"; grep -E 'Sig(Blk|Ign)' /proc/self/status | sed 's/^/  script /'
r $T 5 grep -E 'Sig(Blk|Ign)' /proc/self/status
r $T --foreground 5 grep -E 'Sig(Blk|Ign)' /proc/self/status
c "timeout's own signal state, read by its command"
r $T 5 sh -c 'grep -E "Sig(Blk|Ign|Cgt)" /proc/$PPID/status; grep -c . /proc/$PPID/task/*/stat | wc -l'
c "argv: the command's /proc/self/cmdline"; r $T 5 sh -c 'tr "\0" "|" < /proc/$$/cmdline'
c "stdin passes";  echo hello | r $T 5 cat
c "stdin closed";  r $T 5 sh -c 'cat; echo "cat $?"' <&-
c "a descriptor above 2 passes"; r $T 5 sh -c 'echo three >&3 && echo wrote' 3>three; cat three 2>/dev/null | sed 's/^/  file: /'
c "stdout closed, -v, a timeout"; r sh -c "$T -v 0.2 sleep 1 >&-"
c "stderr closed, -v, a timeout"; r sh -c "$T -v 0.2 sleep 1 2>&-"
c "a stopped command"; r $T 0.5 sh -c 'kill -STOP $$; echo resumed'
c "a stopped command, -s KILL"; r $T -s KILL 0.5 sh -c 'kill -STOP $$; echo resumed'
c "signals sent to timeout"
for s in TERM INT HUP QUIT ALRM USR1 USR2 PIPE CHLD CONT TSTP WINCH; do
  c "$s to timeout 5, the command traps it and exits 3"; rs $s 0.3 $T 5 sh -c "trap 'echo got $s; exit 3' $s; sleep 5 & wait"
  c "$s to timeout 5, the command does not trap"; rs $s 0.3 $T 5 sleep 2
done
c "TERM to timeout -k 0.3 5, the command ignores TERM"; rs TERM 0.3 $T -k 0.3 5 sh -c 'trap "" TERM; sleep 3'
c "TERM to timeout --foreground 5, a grandchild"; rs TERM 0.3 $T --foreground 5 sh -c 'sleep 30 & echo $! > gc; wait'; sleep 0.3; kill -0 "$(cat gc)" 2>/dev/null && echo "  grandchild alive" || echo "  grandchild gone"; kill -9 "$(cat gc)" 2>/dev/null
echo PROBE-DONE
