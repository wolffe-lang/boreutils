#!/usr/bin/env bash
# bu28 (inside box.sh only): the calls GNU's timeout makes when it passes a signal sent to it on to
# its command (strace of the binary, black-box). Every signal goes to a process this script started.
ulimit -c 0; cd "$(mktemp -d /tmp/passon.XXXXXX)" || exit 9
T=${1:-/g/bin/timeout}
strace -f -qq -tt -e trace=kill,tgkill,rt_sigaction,rt_sigprocmask,setpgid -o st "$T" 5 sh -c "trap 'echo got TERM; exit 3' TERM; sleep 5 & wait" > o 2>&1 &
sleep 0.6
p=$(pgrep -f "^$T 5 sh" | head -1); echo "timeout pid $p"; kill -TERM "$p"; wait
echo "out: $(tr '\n' '|' < o)"
grep -n -E 'kill\(|tgkill|SIGTERM' st | grep -v 'rt_sigaction(SIGTERM, NULL' | sed -E 's/^([0-9]+):[0-9]+ /\1: /' | tail -14
