#!/usr/bin/env bash
# bu29: the gauntlet at a kasumi tree (bu28's gauntlet.sh, the lane's paths; the archives from the lane's
# own reads through BORE_ARCHIVE_DIR, the same digest check). Everything that BUILDS or RUNS a utility runs
# in box.sh. usage: T=tree gauntlet.sh TAG
L=$HOME/lanes/bu29; tag=$1; T=${T:-boreutils}; export T
log=$L/ev/gauntlet-$tag.log; B=$L/box.sh
cd "$L/$T" || exit 9
{
  echo "gauntlet: $(date -u +%FT%TZ) on $(hostname) at $tag (tree $T, $(git rev-parse --short HEAD) + $(git status --short | wc -l) changed), load $(cat /proc/loadavg)"
  echo "core store before: $(ls /var/lib/systemd/coredump | wc -l)"
  BORE_ARCHIVE_DIR=$L/arch tools/fetch-toolchain; echo "fetch rc=$?"
  cat .wolf-bin/STAMP; .wolf-bin/wolf --version; .wolf-bin/lupin --version | head -1; cat .wolf-bin/std/STD-REV
  echo "wolf $(sha256sum .wolf-bin/wolf | cut -c1-64)  libwolf_rt.a $(sha256sum .wolf-bin/libwolf_rt.a | cut -c1-64)  lupin $(sha256sum .wolf-bin/lupin | cut -c1-64)"
  $B bash -c "rm -rf target; tools/build >/l/ev/build-release-$tag.log 2>&1; echo build release rc=\$?; tools/build --dev >/l/ev/build-dev-$tag.log 2>&1; echo build dev rc=\$?; ls target/release | wc -l; ls target/dev | wc -l; tools/check-fmt; echo fmt rc=\$?; tools/check-test > /l/ev/check-test-$tag.log 2>&1; echo test rc=\$?; tail -1 /l/ev/check-test-$tag.log; (cd target && sha256sum release/* dev/*) > /l/ev/bins-$tag.txt"
  grep -c -i "warning\|error" $L/ev/build-release-$tag.log $L/ev/build-dev-$tag.log
  $B tools/difftest > "$L/ev/difftest-release-$tag.log" 2>&1; echo "difftest release rc=$?"; tail -1 "$L/ev/difftest-release-$tag.log"
  $B tools/difftest --bin target/dev > "$L/ev/difftest-dev-$tag.log" 2>&1; echo "difftest dev rc=$?"; tail -1 "$L/ev/difftest-dev-$tag.log"
  for t in release dev; do
    echo "verdict list, $t: $(grep -E "^(ok  |FAIL|SKIP) " "$L/ev/difftest-$t-$tag.log" | sed "s/  args=.*//" | sha256sum | cut -c1-16)  ok $(grep -c "^ok  " "$L/ev/difftest-$t-$tag.log") FAIL $(grep -c "^FAIL" "$L/ev/difftest-$t-$tag.log") SKIP $(grep -c "^SKIP" "$L/ev/difftest-$t-$tag.log")"
  done
  $B bash -c "tools/difftest-selftest > /l/ev/selftest-$tag.log 2>&1; echo selftest rc=\$?; tools/difftest-evidence > /l/ev/evidence-$tag.log 2>&1; echo evidence rc=\$?; tools/field-verdict-selftest > /l/ev/field-verdict-selftest-$tag.log 2>&1; echo field-verdict-selftest rc=\$?"
  $B tools/killprobe --table --gnu /g/bin/kill target/release/kill target/dev/kill > "$L/ev/killprobe-$tag.log" 2>&1; echo "killprobe rc=$?"; grep -E '^(agree|PART|killprobe: every|killprobe: [0-9]+ answers)' "$L/ev/killprobe-$tag.log"
  echo "core store after: $(ls /var/lib/systemd/coredump | wc -l)"
  echo "load: $(cat /proc/loadavg)"; date -u +%FT%TZ; echo GAUNTLET-DONE
} > "$log" 2>&1
