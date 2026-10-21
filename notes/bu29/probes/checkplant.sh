#!/usr/bin/env bash
# bu29 (inside box.sh): does each test file run its OWN main under `wolf test` (#799's reach)? A copy of the
# tree, then `wolf test` as it stands and with a failing assert planted first in the last-sorted test file.
# usage: checkplant.sh WOLF STDDIR TAG
W=$1; std=$2; tag=$3; d=/l/tmp/bu29-ctplant-$tag
rm -rf "$d"; mkdir -p "$d"
tar --exclude=./target --exclude=./.wolf-bin --exclude=./.git -C /l/boreutils -cf - . | tar -xf - -C "$d"
cd "$d" || exit 9
echo "checkplant $tag: $($W --version | head -1), std $(cat $std/STD-REV)"
echo "test files, sorted: $(ls src/*_test.lu | tr '\n' ' ')"
WOLF_STD=$std $W test > /l/ev/checkplant-$tag-plain.log 2>&1; echo "plain rc=$?"; cat /l/ev/checkplant-$tag-plain.log
n=$(grep -n '^fn main() {' src/signals_test.lu | cut -d: -f1)
sed -i "${n}a\\    assert(false, \"bu29 plant: signals_test.lu runs its own main\")" src/signals_test.lu
sed -n "${n},$((n+2))p" src/signals_test.lu
WOLF_STD=$std $W test > /l/ev/checkplant-$tag-planted.log 2>&1; echo "planted rc=$?"; cat /l/ev/checkplant-$tag-planted.log
cd /; rm -rf "$d"
