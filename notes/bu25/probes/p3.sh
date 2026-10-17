#!/bin/bash
# bu25 probe p3: where the output's offset stands when an earlier operand has been written (buffering), and the edges.
export C=$1/cat
cd /w || exit 9
fresh() { rm -rf /w/c; mkdir /w/c; cd /w/c; printf 'one\ntwo\n' > f; printf A > a; head -c 200000 /dev/zero | tr '\0' x > big; }
in_at() { python3 -c "import os; os.lseek(0, $1, 0)"; }
out_at() { python3 -c "import os; os.lseek(1, $1, 0)"; }
export -f in_at out_at
run() {
  fresh; echo "## $1"; shift
  timeout 5 bash -c "$*" 2> err; rc=$?
  sed 's/^/  err: /' err
  echo "  rc=$rc size=$(wc -c < f) f=$(od -An -c f | head -c 60 | tr -s ' ' | tr '\n' '|')"
}
run "rw a f (no option)"        '$C a f 1<> f'
run "rw -n a f"                 '$C -n a f 1<> f'
run "rw -v a f"                 '$C -v a f 1<> f'
run "rw -u a f"                 '$C -u a f 1<> f'
run "rw big f"                  '$C big f 1<> f'
run "rw -n big f"               '$C -n big f 1<> f'
run "rw in 8 out 9"             '{ in_at 8; out_at 9; $C; } < f 1<> f'
run "rw in 7 out 8"             '{ in_at 7; out_at 8; $C; } < f 1<> f'
run "rw in 9 out 10 (in past end)" '{ in_at 9; out_at 10; $C; } < f 1<> f'
run "append in past end"        '{ in_at 9; $C; } < f >> f'
run "rw - - in 0 out 0 (stdin twice)" '$C - - < f 1<> f'
run "rw f f out 0"              '$C f f 1<> f'
run "append - a <f >>f"         '$C a - < f >> f'
run "fifo out"                  'mkfifo p; (cat p > /dev/null &) ; $C f > p'
run "rw /dev/stdin in 3 out 1"  '{ in_at 3; out_at 1; $C /dev/stdin; } < f 1<> f'
