#!/usr/bin/env bash
# bu27: how often a waiting `timeout` wakes. Inside a throwaway container only. usage: idle.sh TIMEOUT...
cs() { local n=0; for f in /proc/$1/task/*/status; do v=$(awk '/^voluntary_ctxt_switches/ {a=$2} /^nonvoluntary_ctxt_switches/ {b=$2} END {print a+b}' "$f"); n=$((n + v)); done; echo $n; }
for T in "$@"; do
  "$T" 20 sleep 15 & p=$!
  sleep 1
  a=$(cs $p); threads=$(ls /proc/$p/task | wc -l)
  sleep 10
  b=$(cs $p)
  echo "$T: $threads threads; $((b - a)) context switches in 10 s, every thread"
  kill -TERM $p; wait $p
done
