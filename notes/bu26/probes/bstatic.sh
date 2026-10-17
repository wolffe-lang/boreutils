#!/usr/bin/env bash
# bu26 (inside box.sh): build the named utilities static on both tiers into /l/bin/<tag>/{release,dev}/.
# usage: bstatic.sh TAG UTIL...
set -u
tag=$1; shift
mkdir -p /l/tmp/ccs
printf '#!/bin/sh\nexec %s -static "$@"\n' "$(command -v cc)" > /l/tmp/ccs/cc; chmod +x /l/tmp/ccs/cc
export PATH=/l/tmp/ccs:$PATH WOLF_STD=/l/boreutils/.wolf-bin/std
for tier in release dev; do
  mkdir -p "/l/bin/$tag/$tier"
  fl=; [ $tier = release ] && fl=--release
  for u in "$@"; do
    /l/boreutils/.wolf-bin/wolf build $fl --no-cache --deny-warnings "src/$u.lu" -o "/l/bin/$tag/$tier/$u"; rc=$?
    echo "build $tier $u rc=$rc"
  done
done
