#!/usr/bin/env bash
# bu28: the system calls of the static timeout and kill that are new at wolf 0.2.33, for PAX (inside a
# throwaway container only, `ulimit -c 0`: every signal goes to a process this script started or to the
# group the timeout under test leads). usage: straces.sh BINDIR OUTDIR
B=$1; O=$2; mkdir -p "$O"; ulimit -c 0; cd "$(mktemp -d /tmp/strace.XXXXXX)" || exit 9
st() { name=$1; shift; strace -f -qq -o "$O/$name.strace" "$@"; echo "$name: exit $?"; }
calls() { sed -E 's/^[0-9]+ +//; s/^<\.\.\. ([a-z0-9_]+) resumed>.*/\1/; s/\(.*//' "$O/$1.strace" | grep -E '^[a-z_0-9]+$' | sort -u | tr '\n' ' '; echo; }
for tier in release dev; do
  K=$B/$tier/kill; T=$B/$tier/timeout
  st timeout-$tier-segv-group "$T" -s SEGV 0.3 sleep 5
  st timeout-$tier-rtmin-group "$T" -s RTMIN 0.3 sleep 5
  st timeout-$tier-ends-by-segv "$T" 5 sh -c 'kill -SEGV $$'
  st timeout-$tier-ends-by-rtmin "$T" 5 sh -c 'kill -34 $$'
  st kill-$tier-table-zero "$K" -t 0
  for f in timeout-$tier-segv-group timeout-$tier-rtmin-group timeout-$tier-ends-by-segv timeout-$tier-ends-by-rtmin kill-$tier-table-zero; do
    printf '%s calls: ' "$f"; calls "$f"
  done
  # the lines that are the new calls' own
  for f in timeout-$tier-segv-group timeout-$tier-rtmin-group; do
    echo "-- $f: the ignore and the group send"; grep -E 'rt_sigaction\((SIGSEGV|SIGRT_2|SIGRTMIN|34)|kill\(-|kill\(0' "$O/$f.strace" | sed -E 's/^[0-9]+ +//' | head -8
  done
  for f in timeout-$tier-ends-by-segv timeout-$tier-ends-by-rtmin; do
    echo "-- $f: the poll and the end"; grep -E 'wait4|rt_sigaction\((SIGSEGV|SIGRT_2|SIGRTMIN|34)|rt_sigprocmask\(SIG_UNBLOCK|tgkill|^\+\+\+ killed|exit_group' "$O/$f.strace" | sed -E 's/^[0-9]+ +//' | tail -8
  done
done
for f in "$O"/*.strace; do sha256sum "$f"; done
