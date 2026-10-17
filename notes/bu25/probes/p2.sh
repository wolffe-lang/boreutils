#!/bin/bash
# bu25 probe p2: the other reading-and-writing utilities with an input that is their output.
B=$1; cd /w || exit 9
T="timeout 3"
fresh() { rm -rf /w/c; mkdir /w/c; cd /w/c; printf 'one\ntwo\n' > f; }
run() { fresh; echo "## $1"; shift; eval "$T $*" > out 2> err; rc=$?; sed 's/^/  err: /' err | head -3; echo "  rc=$rc size=$(wc -c < f) outsize=$(wc -c < out)"; }
run "tee -a f <f"        '$B/tee -a f < f > /dev/null'
run "tee f <f"           '$B/tee f < f > /dev/null'
run "tac f >>f"          '$B/tac f >> f'
run "tac <f >>f"         '$B/tac < f >> f'
run "head f >>f"         '$B/head f >> f'
run "head -c 100 <f >>f" '$B/head -c 100 < f >> f'
run "tail f >>f"         '$B/tail f >> f'
run "tail -c +1 <f >>f"  '$B/tail -c +1 < f >> f'
run "sort -o f f"        '$B/sort -o f f'
run "sort f >>f"         '$B/sort f >> f'
run "uniq f f"           '$B/uniq f f'
run "nl f >>f"           '$B/nl f >> f'
run "cut -c1 f >>f"      '$B/cut -c1 f >> f'
run "paste f >>f"        '$B/paste f >> f'
run "tr <f >>f"          '$B/tr a b < f >> f'
run "fold f >>f"         '$B/fold f >> f'
run "expand f >>f"       '$B/expand f >> f'
run "wc f >>f"           '$B/wc f >> f'
run "cp f f"             '$B/cp f f'
run "uniq <f >>f"        '$B/uniq < f >> f'
