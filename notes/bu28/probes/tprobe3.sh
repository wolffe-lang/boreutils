#!/usr/bin/env bash
# bu28: what a `timeout` does with a fault or host signal and with a core, black-box. Run INSIDE a
# throwaway container only (box.sh, `--ulimit core=0:0`): every signal here goes to a process this
# script started, or to the group the timeout under test leads.
# usage: tprobe3.sh TIMEOUT-PROGRAM   (GNU's /g/bin/timeout, or ours)
T=$1
ulimit -c 0
echo "ulimit -c $(ulimit -c), hard $(ulimit -Hc); core_pattern $(cat /proc/sys/kernel/core_pattern)"
cd "$(mktemp -d /tmp/tprobe3.XXXXXX)" || exit 9
# r CMD...: run, guard 15 s; print the RAW wait status (exit, signal, core bit), elapsed, out, err, and
# how many core files the run left here.
r() {
    perl -e 'use Time::HiRes qw(time); $t=time;
      $p=fork; if(!$p){ open(STDOUT,">out"); open(STDERR,">err"); exec @ARGV; exit 99 }
      $SIG{ALRM}=sub{ kill 9,$p; print "GUARD fired\n" }; alarm 15; waitpid($p,0); $s=$?;
      printf "  -> raw %d: %s %d%s, %.1f s\n", $s, ($s&127)?"signal":"exit", ($s&127)?($s&127):($s>>8), ($s&128)?" core":"", time-$t' -- "$@"
    printf '  out: %s\n' "$(od -An -c out | tr -s ' ' | tr -d '\n')"
    printf '  err: %s\n' "$(sed 's/^/        /' err | tr '\n' '|')"
    printf '  cores here: %s\n' "$(ls | grep -c '^core')"
}
# rc: as r, standard error closed.
rc() {
    perl -e '$p=fork; if(!$p){ open(STDOUT,">out"); close(STDERR); exec @ARGV; exit 99 }
      alarm 15; waitpid($p,0); $s=$?; printf "  -> raw %d: %s %d%s\n", $s, ($s&127)?"signal":"exit", ($s&127)?($s&127):($s>>8), ($s&128)?" core":""' -- "$@"
}
c() { echo "== $*"; }
c "the command's own end, no expiry"
for s in SEGV ILL ABRT QUIT BUS FPE TRAP SYS XCPU XFSZ TERM; do
  c 5 the command ends by $s; r $T 5 sh -c "kill -$s \$\$"
done
c -p 5 the command ends by SEGV;      r $T -p 5 sh -c 'kill -SEGV $$'
c -v 5 the command ends by SEGV;      r $T -v 5 sh -c 'kill -SEGV $$'
c --foreground 5 the command ends by SEGV; r $T --foreground 5 sh -c 'kill -SEGV $$'
c 5 the command ends by 32;          r $T 5 sh -c 'kill -32 $$'
c 5 the command ends by RTMIN;       r $T 5 sh -c 'kill -34 $$'
c 5 SEGV, standard error closed;     rc $T 5 sh -c 'kill -SEGV $$'
c "at the expiry"
for s in SEGV ILL TRAP BUS FPE SYS QUIT ABRT RTMIN RTMAX RTMIN+5 16 32 33; do
  c -s $s 0.3 sleep 5;                r $T -s $s 0.3 sleep 5
done
c -p -s SEGV 0.3 sleep 5;            r $T -p -s SEGV 0.3 sleep 5
c -p -s RTMIN 0.3 sleep 5;           r $T -p -s RTMIN 0.3 sleep 5
c -v -s SEGV 0.3 sleep 5;            r $T -v -s SEGV 0.3 sleep 5
c --foreground -s SEGV 0.3 sleep 5;  r $T --foreground -s SEGV 0.3 sleep 5
c --foreground -s QUIT 0.3 sleep 5;  r $T --foreground -s QUIT 0.3 sleep 5
c -s SEGV 0.3, stderr closed;        rc $T -s SEGV 0.3 sleep 5
c -s SEGV -k 0.3 0.3, the command ignores SEGV; r $T -s SEGV -k 0.3 0.3 sh -c 'trap "" SEGV; sleep 5'
c -s RTMIN -k 0.3 0.3, sleep 5;      r $T -s RTMIN -k 0.3 0.3 sleep 5
c "the group"
for s in SEGV RTMIN 16 KILL; do
  c "-s $s 0.3, the command's child"; rm -f gc
  r $T -s $s 0.3 sh -c 'sleep 30 & echo $! > gc; wait'
  if [ -s gc ] && kill -0 "$(cat gc)" 2>/dev/null; then echo "  child: alive"; kill -KILL "$(cat gc)"; else echo "  child: gone"; fi
done
c "timeout's own dispositions after a group send the command lives through"
for s in SEGV RTMIN TERM; do
  c -s $s 0.3, the command ignores it
  n=$s; [ $s = RTMIN ] && n=34
  ( $T -s $s 0.3 sh -c "trap '' $n; sleep 2" > out 2> err & tp=$!; sleep 1.0
    echo "  at 1.0 s: $(grep -E '^(SigBlk|SigIgn|SigCgt)' /proc/$tp/status | tr '\t\n' '  ')"
    wait $tp; echo "  -> \$? $?"; echo "  err: $(tr '\n' '|' < err)" )
done
c "a SEGV sent to timeout after its group send of SEGV"
( $T -s SEGV 0.3 sh -c "trap '' SEGV; sleep 3" > out 2> err & tp=$!; sleep 1.0; kill -SEGV $tp; sleep 0.5
  if kill -0 $tp 2>/dev/null; then echo "  timeout alive after the SEGV"; else echo "  timeout gone after the SEGV"; fi
  wait $tp; echo "  -> \$? $?"; echo "  err: $(tr '\n' '|' < err)" )
echo PROBE-DONE
