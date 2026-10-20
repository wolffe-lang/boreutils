#!/usr/bin/env bash
# bu28: the double delivery, measured (inside ONE throwaway container only: every signal goes to a process
# this script started; the load is this container's own busy loops, on its own cpus).
# usage: double.sh N LOADERS TIMEOUT...   (each TIMEOUT: GNU's or ours)
N=$1; LOAD=$2; shift 2
ulimit -c 0; cd "$(mktemp -d /tmp/double.XXXXXX)" || exit 9
cc -O2 -o sigcount /p/sigcount.c || exit 9
pids=""; for i in $(seq 1 "$LOAD"); do sh -c 'while :; do :; done' & pids="$pids $!"; done
echo "cpus $(grep Cpus_allowed_list /proc/self/status | cut -f2); loaders $LOAD; nproc $(nproc)"
for T in "$@"; do
  two=0; trap2=0
  for i in $(seq 1 "$N"); do
    o=$("$T" 0.3 ./sigcount)
    case "$o" in "deliveries 1 "*) ;; *) two=$((two+1)); echo "  $T sigcount run $i: $o";; esac
    g=$("$T" 0.3 sh -c 'trap "echo got TERM; exit 3" TERM; sleep 5 & wait' | grep -c 'got TERM')
    [ "$g" = 1 ] || { trap2=$((trap2+1)); echo "  $T trap run $i: $g lines"; }
  done
  echo "$T: $two of $N sigcount runs with more than one delivery; $trap2 of $N trap runs with other than one line"
done
kill $pids
