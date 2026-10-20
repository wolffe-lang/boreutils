#!/usr/bin/env bash
# bu28: the double delivery, the second measure (inside ONE throwaway container only: every signal goes to a
# process this script started; the load is this container's own busy loops on its own cpus). Each run is
# `timeout -v 0.3 sigcount`: the -v lines say how many sends timeout made, sigcount how many TERMs reached
# the command and when. usage: double2.sh N LOADERS TIMEOUT...
N=$1; LOAD=$2; shift 2
ulimit -c 0; cd "$(mktemp -d /tmp/double2.XXXXXX)" || exit 9
cc -O2 -o sigcount /p/sigcount.c || exit 9
pids=""; for i in $(seq 1 "$LOAD"); do sh -c 'while :; do :; done' & pids="$pids $!"; done
echo "cpus $(grep Cpus_allowed_list /proc/self/status | cut -f2); loaders $LOAD; nproc $(nproc)"
for T in "$@"; do
  sends2=0; del2=0; long=0
  for i in $(seq 1 "$N"); do
    o=$("$T" -v 0.3 ./sigcount 2> err); v=$(grep -c 'sending signal' err)
    [ "$v" = 1 ] || { sends2=$((sends2+1)); echo "  $T run $i: $v sends: $(tr '\n' '|' < err) / $o"; }
    case "$o" in "deliveries 1 "*) ;; *) del2=$((del2+1))
      g=$(echo "$o" | sed -E 's/.*\+([0-9]+)us\]$/\1/'); [ "$g" -gt 50 ] && { long=$((long+1)); echo "  $T run $i: $o ($v sends)"; } ;; esac
  done
  echo "$T: $N runs; $sends2 with more than one send; $del2 with two deliveries, $long of them more than 50 us apart"
done
kill $pids
