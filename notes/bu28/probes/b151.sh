#!/usr/bin/env bash
# bu28 (inside box.sh): B151 — build all 47 on both tiers under the staged 0.2.33 with a given std tree.
# usage: b151.sh STDDIR TAG
std=$1; tag=$2; W=/l/arch/x/wolf-0.2.33-x86_64-unknown-linux-gnu/wolf
cd /l/boreutils || exit 9
n=0; bad=0
for f in src/*.lu; do
  grep -q '^//! member: false' "$f" || continue
  u=$(basename "$f" .lu)
  for tier in release dev; do
    fl=; [ $tier = release ] && fl=--release
    mkdir -p /l/tmp/b151-$tag/$tier
    WOLF_STD=$std $W build $fl --no-cache --deny-warnings "$f" -o /l/tmp/b151-$tag/$tier/$u > /l/tmp/b151-$tag/$u-$tier.out 2>&1; rc=$?
    n=$((n+1)); [ $rc -eq 0 ] || { bad=$((bad+1)); echo "FAIL $u $tier rc=$rc"; head -20 /l/tmp/b151-$tag/$u-$tier.out; }
  done
done
echo "b151 $tag: std $(cat $std/STD-REV 2>/dev/null || echo "$std"): $n builds, $bad failed, $(cat /l/tmp/b151-$tag/*.out | grep -c -i 'warning') warning lines"
(cd /l/tmp/b151-$tag && sha256sum release/* dev/*) > /l/ev/b151-bins-$tag.txt
