#!/usr/bin/env bash
set -euo pipefail
L=$HOME/lanes/bu30
export PATH=$L/bin:$HOME/lanes/hasu-env/bin:$HOME/lanes/hasu-env/profile/bin:$PATH
export TMPDIR=$L/tmp
exec 9>"$HOME/lanes/hasu-A.lock"
until flock -w 120 9; do echo "waiting for block A: $(date -u +%FT%TZ)"; done
cd "$L/boreutils"
git pull --ff-only
echo "suite $1 $(date -u +%FT%TZ) head $(git rev-parse HEAD)"
args=(--engine podman --image localhost/bu30-ubuntu --gnu "$L/boreutils/.gnu-bin/bin" --bin "$L/boreutils/target/suite")
if [[ $1 == killtest || $1 == timeouttest ]]; then args+=(--cpus 0-3); fi
python3 "tools/$1" "${args[@]}"
echo "SUITE-DONE $1"
