#!/usr/bin/env bash
# bu27: the system calls of the static kill and timeout for PAX (inside a throwaway container only:
# every signal goes to a process this script started). usage: straces.sh BINDIR OUTDIR
B=$1; O=$2; mkdir -p "$O"; cd "$(mktemp -d /tmp/strace.XXXXXX)" || exit 9
st() { name=$1; shift; strace -f -qq -o "$O/$name.strace" "$@"; echo "$name: exit $?"; }
calls() { sed -E 's/^[0-9]+ +//; s/^<\.\.\. ([a-z0-9_]+) resumed>.*/\1/; s/\(.*//' "$O/$1.strace" | grep -E '^[a-z_0-9]+$' | sort -u | tr '\n' ' '; echo; }
for tier in release dev; do
  K=$B/$tier/kill; T=$B/$tier/timeout
  setsid sleep 30 & L=$!; sleep 0.2
  st kill-$tier-group "$K" -s TERM -- -"$L"; wait $L 2>/dev/null
  setsid sh -c 'sleep 30 & sleep 30 & sleep 0.2; exec "$@"' lead strace -f -qq -o "$O/kill-$tier-zero.strace" "$K" 0; echo "kill-$tier-zero: exit $?"
  sleep 30 & a=$!; sleep 0.2
  st kill-$tier-all "$K" -s 0 -- -1; kill $a; wait $a 2>/dev/null
  st kill-$tier-list "$K" -t 64
  st timeout-$tier-expiry "$T" 0.3 sh -c 'sleep 30 & wait'
  st timeout-$tier-kill-after "$T" -k 0.2 0.2 sh -c 'trap "" TERM; sleep 5'
  st timeout-$tier-foreground "$T" --foreground 0.3 sleep 5
  st timeout-$tier-ends "$T" 5 true
  for f in kill-$tier-group kill-$tier-zero kill-$tier-all kill-$tier-list timeout-$tier-expiry timeout-$tier-kill-after timeout-$tier-foreground timeout-$tier-ends; do
    printf '%s calls: ' "$f"; calls "$f"
  done
done
for f in "$O"/*.strace; do sha256sum "$f"; done
