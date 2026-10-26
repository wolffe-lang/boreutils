#!/usr/bin/env bash
set -euo pipefail
root=/home/mfwolffe/lanes/bu36
export PATH=/home/mfwolffe/lanes/hasu-env/bin:/home/mfwolffe/lanes/hasu-env/profile/bin:$PATH
printf '%s\n' "$$" > "$root/full.pid"
trap 'rc=$?; printf "%s\n" "$rc" > "$root/full.exit"; printf "FULL EXIT=%s " "$rc"; date -u' EXIT
expected="$1"
check_head() {
    test "$(git -C "$root/boreutils" rev-parse HEAD)" = "$expected"
    git -C "$root/boreutils" diff --exit-code --quiet
}
check_head
printf 'START HEAD=%s ' "$expected"; date -u
available=$(df -Pk "$root" | awk 'NR==2 {print $4}')
test "$available" -ge 4194304
exec 9>/home/mfwolffe/lanes/hasu-B.lock
flock 9
exec 8>/home/mfwolffe/lanes/hasu-block-B.lock
flock 8
printf 'LOCKED B 6-11 '; date -u
podman image inspect localhost/bu30-ubuntu:latest --format '{{.Id}}'
uid=$(id -u); gid=$(id -g)
podman run --rm -i --name bu36-full-base --cidfile "$root/ev/full-base.cid" --network none --userns keep-id --user "$uid:$gid" --memory 12g --pids-limit 16384 --ulimit nproc=32768:32768 -e TMPDIR=/lane/tmp -e BORE_DISK_CONTAINER=1 -v "$root:/lane" -w /lane/boreutils localhost/bu30-ubuntu:latest taskset -c 6-11 bash -s <<'BASE'
set -euo pipefail
ulimit -c 0
export PATH=/lane/boreutils/.gnu-bin/bin:$PATH
for step in inputs fmt release dev unit diff-release diff-dev harness text checksum evidence small field splitter number disk-integration static-rigs gaps; do
    printf 'START %s ' "$step"; date -u
    case "$step" in
      inputs) python3 -I /lane/verify-inputs.py > /lane/ev/full-inputs.log 2>&1 ;;
      fmt) tools/check-fmt > /lane/ev/full-fmt.log 2>&1 ;;
      release) tools/build > /lane/ev/full-build-release.log 2>&1 ;;
      dev) tools/build --dev > /lane/ev/full-build-dev.log 2>&1 ;;
      unit) tools/check-test > /lane/ev/full-unit.log 2>&1 ;;
      diff-release) tools/difftest --bin target/release > /lane/ev/full-diff-release.log 2>&1 ;;
      diff-dev) tools/difftest --bin target/dev > /lane/ev/full-diff-dev.log 2>&1 ;;
      harness) tools/difftest-selftest > /lane/ev/full-harness.log 2>&1 ;;
      text) tools/texttest > /lane/ev/full-text.log 2>&1 ;;
      checksum) tools/checksumtest > /lane/ev/full-checksum.log 2>&1 ;;
      evidence) tools/difftest-evidence > /lane/ev/full-evidence.log 2>&1 ;;
      small) tools/smalltest > /lane/ev/full-small.log 2>&1 ;;
      field) tools/field-verdict-selftest > /lane/ev/full-field.log 2>&1 ;;
      splitter) tools/splittertest > /lane/ev/full-splitter.log 2>&1 ;;
      number) tools/numbertest > /lane/ev/full-number.log 2>&1 ;;
      disk-integration) python3 -I tests/disk-process/check.py > /lane/ev/full-disk-integration.log 2>&1 ;;
      static-rigs)
        python3 -I - <<'PY' > /lane/ev/full-static-rigs.log 2>&1
import runpy
runpy.run_path('tools/idtest',run_name='bu36_idtest')['build']('/lane/boreutils/target/idtest',True)
runpy.run_path('tools/roottest',run_name='bu36_roottest')['build_static']('/lane/boreutils/target/roottest')
PY
        ;;
      gaps)
        for g in tests/gaps/bu36/*/main.lu; do
          name=$(basename "$(dirname "$g")")
          set +e
          WOLF_STD=/lane/boreutils/.wolf-bin/std .wolf-bin/wolf build "$g" -o /lane/tmp/gap-probe > "/lane/ev/full-gap-$name.log" 2>&1
          code=$?
          set -e
          test "$code" = 2
          grep -q E0301 "/lane/ev/full-gap-$name.log"
          printf 'EXPECTED COMPILE ERROR %s exit=%s\n' "$name" "$code"
        done ;;
    esac
    printf 'PASS %s ' "$step"; date -u
 done
BASE
check_head
printf 'START options integration '; date -u
podman run --rm --name bu36-full-options --network none --userns keep-id --user "$uid:$gid" --memory 12g --tmpfs /bu36-mount:rw,mode=1777 --tmpfs /lane/tmp/bu36-cp-source/mount:rw,mode=1777 -e TMPDIR=/lane/tmp -e BORE_OPTIONS_CONTAINER=1 -v "$root:/lane" -w /lane/boreutils localhost/bu30-ubuntu:latest taskset -c 6-11 python3 -I tests/options-not-written/check.py > "$root/ev/full-options-integration.log" 2>&1
printf 'PASS options integration '; date -u
printf 'START identity terminal '; date -u
podman run --rm --name bu36-full-identity-terminal --network none --memory 12g -e BORE_UTMP_CONTAINER=1 -v "$root:/lane:ro" -w /lane/boreutils localhost/bu30-ubuntu:latest taskset -c 6-11 bash -c '
set -euo pipefail
ulimit -c 0
python3 -I tests/identity-terminal/check.py
python3 -I tests/identity-terminal/check.py --bin target/dev
python3 -I tests/identity-terminal/selinux-field.py
' > "$root/ev/full-identity-terminal.log" 2>&1
printf 'PASS identity terminal '; date -u
export TMPDIR="$root/tmp"
cd "$root/boreutils"
printf 'START idtest '; date -u
taskset -c 6-11 tools/idtest --engine "$root/podman-rig" --image localhost/bu30-ubuntu:latest --bin target/idtest --gnu .gnu-bin/bin > "$root/ev/full-idtest.log" 2>&1
taskset -c 6-11 tools/idtest-selftest --engine "$root/podman-rig" --image localhost/bu30-ubuntu:latest --bin target/idtest --gnu .gnu-bin/bin > "$root/ev/full-idtest-selftest.log" 2>&1
printf 'PASS idtest and selftest '; date -u
printf 'START roottest '; date -u
taskset -c 6-11 tools/roottest --engine "$root/podman-rig" --image localhost/bu30-ubuntu:latest --bin target/roottest --gnu .gnu-bin/bin > "$root/ev/full-roottest.log" 2>&1
printf 'PASS roottest '; date -u
check_head
printf 'FINAL HEAD=%s ' "$expected"; date -u
