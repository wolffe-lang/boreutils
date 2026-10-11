#!/usr/bin/env bash
# bu21 census — run every probe on wolf's four machines.
#
#   notes/bu21/census/run.sh WORK
#
# WORK is a directory this script creates and empties; it must be under
# ~/lanes/bu21/ and is refused otherwise, because the probes make and
# remove files in it. The toolchain is the repository's pin
# (`tools/fetch-toolchain`). Output is the census transcript.
set -u
here=$(cd "$(dirname "$0")" && pwd)
root=$(cd "$here/../../.." && pwd)
WOLF="$root/.wolf-bin/wolf"
LUPIN="$root/.wolf-bin/lupin"
WORK=${1:?usage: run.sh WORK}
lane="$HOME/lanes/bu21/"
case "$WORK" in
    "$lane"?*) ;;
    *) echo "census: refusing a work directory outside $lane: $WORK" >&2; exit 2 ;;
esac
case "$WORK" in *..*) echo "census: refusing a path with .." >&2; exit 2 ;; esac
mkdir -p "$WORK"
WORK=$(cd "$WORK" && pwd -P)
case "$WORK" in "$lane"?*) ;; *) echo "census: $WORK resolves outside $lane" >&2; exit 2 ;; esac

echo "census: $("$WOLF" --version | head -1); $("$LUPIN" --version | head -1)"
echo "census: host $(uname -sm), filesystem $(stat -f -c %T "$WORK"), umask $(umask)"

# One fresh directory per (probe, machine). Emptied by this script only,
# and only under the checked prefix.
fresh() {
    local d="$WORK/$1"
    case "$d" in "$lane"?*) ;; *) echo "census: bad dir $d" >&2; exit 2 ;; esac
    if [ -d "$d/there" ]; then rmdir "$d/there" 2>/dev/null || true; fi
    rm -rf -- "$d"
    mkdir -p "$d"
    echo "$d"
}

machines="native release checked lupin"
run_probe() {
    local probe=$1 src="$here/$1/p.lu" setup=${2:-}
    for m in $machines; do
        local d; d=$(fresh "$probe.$m")
        if [ -n "$setup" ]; then ( cd "$d" && eval "$setup" ) || { echo "== $probe on $m: setup failed"; continue; }; fi
        echo "== $probe on $m"
        case "$m" in
            native)  "$WOLF" build --deny-warnings "$src" -o "$WORK/$probe.$m.bin" >"$WORK/$probe.$m.build" 2>&1; rc=$?
                     if [ $rc -ne 0 ]; then echo "   wolf build exit $rc: $(grep -m1 -E 'error|cannot' "$WORK/$probe.$m.build")"; continue; fi
                     ( cd "$d" && "$WORK/$probe.$m.bin" ) 2>&1 | sed 's/^/   /'; echo "   exit ${PIPESTATUS[0]}" ;;
            release) "$WOLF" build --release --deny-warnings "$src" -o "$WORK/$probe.$m.bin" >"$WORK/$probe.$m.build" 2>&1; rc=$?
                     if [ $rc -ne 0 ]; then echo "   wolf build --release exit $rc: $(grep -m1 -E 'error|cannot' "$WORK/$probe.$m.build")"; continue; fi
                     ( cd "$d" && "$WORK/$probe.$m.bin" ) 2>&1 | sed 's/^/   /'; echo "   exit ${PIPESTATUS[0]}" ;;
            checked) ( cd "$d" && "$WOLF" conform-run "$src" --checked --json ) >"$WORK/$probe.$m.json" 2>&1; rc=$?
                     python3 - "$WORK/$probe.$m.json" <<'PY' | sed 's/^/   /'
import json, sys
text = open(sys.argv[1]).read()
try:
    rec = json.loads(text)
except Exception:
    print("(not a record) " + text.strip().splitlines()[0][:200] if text.strip() else "(empty)")
    sys.exit(0)
out = rec.get("stdout_inline", "")
sys.stdout.write(out if out.endswith("\n") or not out else out + "\n")
print("verdict " + str(rec.get("verdict")))
PY
                     echo "   conform-run exit $rc" ;;
            lupin)   ( cd "$d" && cp "$src" p.lu && "$LUPIN" run p.lu ) 2>&1 | sed 's/^/   /'; echo "   exit ${PIPESTATUS[0]}" ;;
        esac
    done
}

run_probe exists 'ln -s target link'
run_probe rename
run_probe holes
# Two devices: a btrfs subvolume beside a plain directory. lupin is left
# out by the probe's own note; it runs anyway and says what it says.
if command -v btrfs >/dev/null 2>&1; then
    run_probe xdev 'mkdir here && btrfs subvolume create there >/dev/null'
else
    echo "== xdev: no btrfs here, not run"
fi
for p in "$here"/missing/*/; do
    n=$(basename "$p")
    echo "== missing/$n"
    "$WOLF" build --deny-warnings "$p/p.lu" -o "$WORK/missing.$n.bin" >"$WORK/missing.$n.build" 2>&1
    echo "   native: wolf build exit $? — $(grep -m1 -E '^error' "$WORK/missing.$n.build")"
    "$WOLF" build --release --deny-warnings "$p/p.lu" -o "$WORK/missing.$n.bin" >"$WORK/missing.$n.build" 2>&1
    echo "   release: wolf build exit $? — $(grep -m1 -E '^error' "$WORK/missing.$n.build")"
    ( cd "$WORK" && "$WOLF" conform-run "$p/p.lu" --checked --json ) >"$WORK/missing.$n.json" 2>&1
    echo "   checked: conform-run exit $? — $(grep -m1 -E '^error' "$WORK/missing.$n.json"); record $(grep -o '"verdict":"[^"]*"' "$WORK/missing.$n.json")"
    d=$(fresh "missing.$n.lupin"); ( cd "$d" && cp "$p/p.lu" p.lu && "$LUPIN" run p.lu ) >"$WORK/missing.$n.lupin.out" 2>&1
    echo "   lupin: exit $? — $(grep -m1 -E 'error|unsupported' "$WORK/missing.$n.lupin.out")"
done
echo "census: done"
