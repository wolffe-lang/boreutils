#!/usr/bin/env bash
# bu28: timeouttest's row `expiry: the command traps TERM and exits 3`, run N times a timeout under load
# (inside ONE throwaway container only, its own cpus; the load is its own busy loops). A run is red when the
# trap's line is printed other than once. usage: traprow.sh N LOADERS TIMEOUT...
N=$1; LOAD=$2; shift 2
ulimit -c 0; cd "$(mktemp -d /tmp/traprow.XXXXXX)" || exit 9
pids=""; for i in $(seq 1 "$LOAD"); do sh -c 'while :; do :; done' & pids="$pids $!"; done
echo "cpus $(grep Cpus_allowed_list /proc/self/status | cut -f2); loaders $LOAD; nproc $(nproc); $(date -u +%FT%TZ)"
for T in "$@"; do
  red=0
  for i in $(seq 1 "$N"); do
    out=$(env LC_ALL=C "$T" 0.3 sh -c 'trap "echo got TERM; exit 3" TERM; sleep 5 & wait' < /dev/null); rc=$?
    n=$(printf '%s' "$out" | grep -c 'got TERM')
    if [ "$n" != 1 ] || [ "$rc" != 124 ]; then red=$((red+1)); echo "  $T run $i: $n lines, exit $rc"; fi
  done
  echo "$T: $red of $N red"
done
kill $pids; echo "TRAPROW-DONE $(date -u +%FT%TZ)"
