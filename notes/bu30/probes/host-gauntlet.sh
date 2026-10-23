#!/usr/bin/env bash
set -euo pipefail
echo $$ > ~/lanes/bu30/gauntlet.pid
exec 9>"$HOME/lanes/hasu-A.lock"
until flock -w 120 9; do echo "waiting for block A: $(date -u +%FT%TZ)"; done
L=$HOME/lanes/bu30
git -C "$L/boreutils" pull --ff-only
echo "gauntlet $(date -u +%FT%TZ) $(git -C "$L/boreutils" rev-parse HEAD)"
"$L/box" bash -c 'set -e; tools/build > /l/ev/build-final-release.log 2>&1; tools/build --dev > /l/ev/build-final-dev.log 2>&1; tools/check-fmt; WOLF_STD=$PWD/.wolf-bin/std .wolf-bin/wolf test --nocapture; tools/difftest > /l/ev/difftest-final-release.log 2>&1; tools/difftest --bin target/dev > /l/ev/difftest-final-dev.log 2>&1; tail -n 1 /l/ev/difftest-final-release.log /l/ev/difftest-final-dev.log; tools/difftest-selftest; BORE_SMALL_TIER=dev python3 tools/smalltest; tools/difftest-evidence; tools/field-verdict-selftest; tools/killprobe --table --gnu .gnu-bin/bin/kill target/release/kill target/dev/kill'
echo GAUNTLET-DONE
