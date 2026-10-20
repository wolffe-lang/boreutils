#!/usr/bin/env bash
# bu28 (inside box.sh only): the calls GNU's timeout and ours make at the expiry, from the timer's signal
# to the end (strace of the binary, black-box). Every signal goes to the group the timeout leads.
ulimit -c 0; cd "$(mktemp -d /tmp/expiry.XXXXXX)" || exit 9
for T in "$@"; do
  strace -f -qq -tt -e trace=kill,tgkill,rt_sigaction,rt_sigprocmask,timer_settime,alarm,setitimer -o st "$T" 0.3 sh -c "trap 'echo got TERM; exit 3' TERM; sleep 5 & wait" > o 2>&1
  echo "== $T: exit $?; out: $(tr '\n' '|' < o)"
  grep -n -E 'SIGALRM|kill\(|tgkill|SIGTERM|SIGCONT' st | grep -v -E 'rt_sigaction\(SIG(TERM|CONT|ALRM), NULL' | sed -E 's/^([0-9]+):[0-9]+ /\1: /' | head -24
done
