#!/usr/bin/env bash
# bu29: B151 at 0.2.34 — the old std pin and the bundle, each staged as tools/fetch-toolchain stages a rev.
L=$HOME/lanes/bu29
{
echo "run-b151: $(date -u +%FT%TZ) on $(hostname) at $(git -C $L/boreutils rev-parse --short HEAD), load $(cat /proc/loadavg)"
for rev in cceda63151430eac07df895fdfffddfa4a0b92c1 e036bec318ad81ecd5a025612bc2c2adb17527f3; do
  d=$L/std/${rev:0:7}; rm -rf "$d"; mkdir -p "$d"; g=$(mktemp -d $L/tmp/bu29-stdgit.XXXXXX)
  git init -q "$g"; git -C "$g" fetch -q --depth 1 https://github.com/wolffe-lang/wolf-std "$rev"
  git -C "$g" archive FETCH_HEAD std | tar -x -C "$d"; git -C "$g" rev-parse FETCH_HEAD > "$d/std/STD-REV"; rm -rf "$g"
  echo "std ${rev:0:7}: $(find $d/std -name '*.lu' | wc -l) .lu files, STD-REV $(cat $d/std/STD-REV)"
done
echo "the bundle against the e036bec tree: $(diff -r $L/arch/x/wolf-0.2.34-x86_64-unknown-linux-gnu/std $L/std/e036bec/std | grep -v '^Only in .*: LICENSE' | wc -l) differing lines beyond the archive's LICENSE files"
diff -r $L/arch/x/wolf-0.2.34-x86_64-unknown-linux-gnu/std $L/std/e036bec/std
$L/box.sh bash /l/b151.sh /l/std/cceda63/std cceda63
$L/box.sh bash /l/b151.sh /l/std/e036bec/std e036bec
echo "binaries alike between the two: $(join -j2 <(sort -k2 $L/ev/b151-bins-cceda63.txt) <(sort -k2 $L/ev/b151-bins-e036bec.txt) | awk '$2==$3' | wc -l) of $(wc -l < $L/ev/b151-bins-e036bec.txt)"
echo "differ: $(join -j2 <(sort -k2 $L/ev/b151-bins-cceda63.txt) <(sort -k2 $L/ev/b151-bins-e036bec.txt) | awk '$2!=$3{print $1}' | tr '\n' ' ')"
echo "b151 done $(date -u +%FT%TZ)"
} > $L/ev/b151.log 2>&1
echo RUN-B151-DONE >> $L/ev/b151.log
