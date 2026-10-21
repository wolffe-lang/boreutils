#!/usr/bin/env bash
# bu29: the release archives on kasumi, each read twice against the release API's digests.
set -u
L=$HOME/lanes/bu29; A=$L/arch; mkdir -p "$A" "$L/ev"; cd "$A" || exit 9
log=$L/ev/archives.log
{
echo "archives: $(date -u +%FT%TZ) on $(hostname)"
while read -r tag name want; do
  url="https://github.com/wolffe-lang/$tag/$name"
  [ -f "$name" ] || curl -sSfL --retry 3 --retry-delay 5 -o "$name" "$url" || { echo "FETCH FAILED $name"; continue; }
  r1=$(sha256sum "$name" | cut -d' ' -f1); r2=$(sha256sum "$name" | cut -d' ' -f1)
  v=MISMATCH; [ "$r1" = "$want" ] && [ "$r2" = "$want" ] && v=OK
  echo "$v $name $(stat -c %s "$name") B read1 $r1 read2 $r2 api $want"
done <<'LIST'
wolf-lang/releases/download/v0.2.34 wolf-0.2.34-x86_64-unknown-linux-gnu.tar.gz 88a9dd3da1c9a0e38c08eb6e2de9c1ef04d1ed93dcf51024d8dbbb76890c1821
wolf-lang/releases/download/v0.2.34 wolf-0.2.34-aarch64-unknown-linux-gnu.tar.gz ca5cadf936dc0d4396e92733fc65e953d549f3b61f0aa354e7be2e78ea8c3ad0
wolf-lang/releases/download/v0.2.34 wolf-0.2.34-aarch64-apple-darwin.tar.gz 29c8331f5d188b00c4580bc7677b1238891c5734d00b0512df10c60eab236ee3
wolf-lang/releases/download/v0.2.34 wolf-0.2.34-x86_64-pc-windows-msvc.tar.gz 77bb8403aeeae9f0ebd5a461f3a71d6360acb4be60194307993245d0ff1e2f07
wolf-interp/releases/download/v0.1.55 lupin-0.1.55-x86_64-unknown-linux-gnu.tar.gz 1152abc0bef65d334b94bc881a26463fac345919cc2ca07a291796e6048a8a38
wolf-interp/releases/download/v0.1.55 lupin-0.1.55-aarch64-unknown-linux-gnu.tar.gz 5854ab268a835bb75749bce7601441858ac342351906a0838e8602e4edbd45d7
wolf-interp/releases/download/v0.1.55 lupin-0.1.55-aarch64-apple-darwin.tar.gz 2eac1cccdc8a5bec5831787604098982a7ac42e41561a037c3b5ccf0ac21741a
LIST
mkdir -p x
for t in x86_64-unknown-linux-gnu aarch64-unknown-linux-gnu aarch64-apple-darwin; do
  tar -xzf wolf-0.2.34-$t.tar.gz -C x
  d=x/wolf-0.2.34-$t
  echo "wolf $t: _wolf $(find $d -name _wolf -exec sha256sum {} \; | cut -c1-64)  STD-REV $(cat $d/std/STD-REV)  std files $(find $d/std -name '*.lu' | wc -l)  members $(find $d -type f | wc -l)"
done
tar -xzf lupin-0.1.55-x86_64-unknown-linux-gnu.tar.gz -C x
w=x/wolf-0.2.34-x86_64-unknown-linux-gnu/wolf; l=$(find x/lupin-0.1.55-x86_64-unknown-linux-gnu -name lupin -type f | head -1)
echo "--- $w --version"; $w --version
echo "--- $l --version"; $l --version
echo "wolf sha256 $(sha256sum $w | cut -c1-64)  libwolf_rt.a $(sha256sum $(dirname $w)/libwolf_rt.a | cut -c1-64)  lupin $(sha256sum $l | cut -c1-64)"
echo "--- archive member list (x86-64 wolf)"; tar -tzf wolf-0.2.34-x86_64-unknown-linux-gnu.tar.gz | grep -v '/std/' 
echo "done $(date -u +%FT%TZ)"
} > "$log" 2>&1
echo ARCHIVES-DONE >> "$log"
