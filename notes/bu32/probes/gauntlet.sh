#!/usr/bin/env bash
set -uo pipefail
echo $$ > "$HOME/lanes/bu32/gauntlet.pid"
exec 9>"$HOME/lanes/hasu-B.lock"
until flock -w 120 9; do echo "waiting B $(date -u)"; done
L=$HOME/lanes/bu32
export PATH=$L/bin:$HOME/lanes/hasu-env/bin:$HOME/lanes/hasu-env/profile/bin:$PATH
export TMPDIR=$L/tmp
cd "$L/boreutils"
git pull --ff-only || exit 2
head=$(git rev-parse HEAD)
echo "GAUNTLET-HEAD $head START $(date -u +%FT%TZ)"
"$L/box" bash /l/whole-inner.sh
rc=$?
if [[ $rc != 0 ]]; then echo "GAUNTLET-EXIT $rc HEAD $head"; exit "$rc"; fi
for suite in killtest timeouttest idtest inouttest roottest; do
  echo "SUITE-START $suite $(date -u +%FT%TZ)"
  args=(--engine podman --image localhost/bu30-ubuntu --gnu "$PWD/.gnu-bin/bin" --bin "$PWD/target/suite")
  if [[ $suite == killtest || $suite == timeouttest ]]; then args+=(--cpus 6-9); fi
  if [[ $suite != roottest ]]; then
    "tools/$suite-selftest" "${args[@]}" > "$L/ev/final-$suite-selftest.log" 2>&1
    rc=$?
    if [[ $rc != 0 ]]; then echo "GAUNTLET-EXIT $rc HEAD $head SELFTEST $suite"; exit "$rc"; fi
  fi
  taskset -c 6-11 python3 "tools/$suite" "${args[@]}" > "$L/ev/final-$suite.log" 2>&1
  rc=$?
  tail -n 3 "$L/ev/final-$suite.log"
  if [[ $rc != 0 ]]; then echo "GAUNTLET-EXIT $rc HEAD $head SUITE $suite"; exit "$rc"; fi
done
same=$(git rev-parse HEAD)
if [[ $same != "$head" ]]; then echo "HEAD-CHANGED $head $same"; exit 2; fi
echo "GAUNTLET-EXIT 0 HEAD $head END $(date -u +%FT%TZ)"
exit 0
