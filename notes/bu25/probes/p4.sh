#!/bin/bash
# bu25 probe p4: the filters appended to their own input, at three sizes: where does each stop?
B=$1; cd /w || exit 9
for n in 8 5000 300000; do
  for line in "tail -c +1 <f" "nl f" "cut -c1- f" "tr a b <f" "fold f" "expand f" "uniq <f" "head -c 100000000 <f" "cat -n f" "paste f" "tac f"; do
    rm -rf /w/c; mkdir /w/c; cd /w/c
    head -c "$n" /dev/zero | tr '\0' 'x' | fold -w 7 > f 2>/dev/null; s0=$(wc -c < f)
    timeout 3 bash -c "$B/$line >> f" 2>/dev/null; rc=$?
    echo "n=$s0 [$line >> f] rc=$rc size=$(wc -c < f)"
  done
done
