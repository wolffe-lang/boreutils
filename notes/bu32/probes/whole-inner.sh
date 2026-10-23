#!/usr/bin/env bash
set -euo pipefail
cd /l/boreutils
echo "INNER affinity $(taskset -pc $$) memory=$(cat /sys/fs/cgroup/memory.max)"
python3 ci/tiers-test.py
tools/check-fmt
tools/build > /l/ev/final-build-release.log 2>&1
tools/build --dev > /l/ev/final-build-dev.log 2>&1
WOLF_STD=$PWD/.wolf-bin/std .wolf-bin/wolf test --nocapture > /l/ev/final-unit.log 2>&1
cat /l/ev/final-unit.log
tools/difftest > /l/ev/final-difftest-release.log 2>&1
tools/difftest --bin target/dev > /l/ev/final-difftest-dev.log 2>&1
tail -n 1 /l/ev/final-difftest-{release,dev}.log
tools/checksumtest > /l/ev/final-checksum-release.log 2>&1
BORE_CHECKSUM_TIER=dev tools/checksumtest > /l/ev/final-checksum-dev.log 2>&1
tools/checksumtest --large > /l/ev/final-large.log 2>&1
tools/difftest-selftest
tools/difftest-evidence
tools/field-verdict-selftest
python3 tools/smalltest
BORE_SMALL_TIER=dev python3 tools/smalltest
tools/killprobe --table --gnu .gnu-bin/bin/kill target/release/kill target/dev/kill
# Every suite build is inside Ubuntu, never the NixOS host.
export WOLF_STD=$PWD/.wolf-bin/std
export PATH=/l/static/bin:$PATH
for tier in release dev; do
  mkdir -p "target/suite/$tier"
  flags=()
  if [[ $tier == release ]]; then flags=(--release); fi
  for u in rm mv cp kill timeout id whoami groups logname chown chgrp cat; do
    .wolf-bin/wolf build "${flags[@]}" --no-cache --deny-warnings "src/$u.lu" -o "target/suite/$tier/$u" > "/l/ev/final-static-$tier-$u.log" 2>&1
    echo "STATIC $tier $u"
  done
done
