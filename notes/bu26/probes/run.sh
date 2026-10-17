#!/usr/bin/env bash
# bu26: inside box.sh. Build each probe on both tiers and run it with descriptor 1 closed.
cd /l/probes/fd1 || exit 9
W=/l/boreutils/.wolf-bin/wolf; export WOLF_STD=${STD:-/l/boreutils/.wolf-bin/std}
$W --version | head -1
echo "std: $WOLF_STD $(cat "$WOLF_STD/STD-REV" 2>/dev/null || git -C "$WOLF_STD/.." rev-parse HEAD 2>/dev/null)"
for p in "$@"; do
  $W build --release "$p.lu" -o "$p-rel" > "$p-rel.build" 2>&1; echo "$p build release rc=$?"
  $W build "$p.lu" -o "$p-dev" > "$p-dev.build" 2>&1; echo "$p build dev rc=$?"
  for t in rel dev; do echo "== $p $t, descriptor 1 closed"; "./$p-$t" >&-; done
done
