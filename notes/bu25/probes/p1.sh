#!/bin/bash
# bu25 probe p1: cat with an input that is its output. $1 = dir of the programs. Runs in /w (a small tmpfs).
# Every line runs under `timeout 5` in its own bash; `rc` is cat's own status ($? of the line's last command).
export C=$1/cat
cd /w || exit 9
fresh() { rm -rf /w/c; mkdir /w/c; cd /w/c; printf 'one\ntwo\n' > f; printf A > a; printf B > b; }
export -f fresh
in_at() { python3 -c "import os; os.lseek(0, $1, 0)"; }   # move stdin's shared offset
out_at() { python3 -c "import os; os.lseek(1, $1, 0)"; }  # move stdout's shared offset
export -f in_at out_at
run() {
  fresh; echo "## $1"; shift
  timeout 5 bash -c "$*" 2> err; rc=$?
  sed 's/^/  err: /' err
  echo "  rc=$rc size=$(wc -c < f) f=$(od -An -c f | head -c 80 | tr -s ' ' | tr '\n' '|')"
}
echo "id: $(id -u)"
run "append f>>f"              '$C f >> f'
run "stdin <f >>f"             '$C < f >> f'
run "dash <f >>f"              '$C - < f >> f'
run "devstdin <f >>f"          '$C /dev/stdin < f >> f'
run "hardlink"                 'ln f h; $C h >> f'
run "symlink"                  'ln -s f s; $C s >> f'
run "trunc f>f"                '$C f > f'
run "trunc stdin <f >f"        '$C < f > f'
run "empty append"             ': > f; $C f >> f'
run "empty append stdin"       ': > f; $C < f >> f'
run "append, in at 3"          '{ in_at 3; $C; } < f >> f'
run "append, in at end"        '{ in_at 8; $C; } < f >> f'
run "rw in 0 out 0 (operand)"  '$C f 1<> f'
run "rw in 0 out 0 (stdin)"    '$C < f 1<> f'
run "rw in 3 out 0"            '{ in_at 3; $C; } < f 1<> f'
run "rw in 8 out 0"            '{ in_at 8; $C; } < f 1<> f'
run "rw in 0 out 2"            '{ out_at 2; $C; } < f 1<> f'
run "rw in 0 out 2 (operand)"  '{ out_at 2; $C f; } 1<> f'
run "rw in 3 out 3"            '{ in_at 3; out_at 3; $C; } < f 1<> f'
run "rw in 3 out 4"            '{ in_at 3; out_at 4; $C; } < f 1<> f'
run "rw in 0 out 8"            '{ out_at 8; $C; } < f 1<> f'
run "rw in 8 out 8"            '{ in_at 8; out_at 8; $C; } < f 1<> f'
run "rw in 0 out 9 (past end)" '{ out_at 9; $C; } < f 1<> f'
run "w in 0 out 2 (no trunc, no append)" '{ out_at 2; $C f; } 1<> f'
run "pipe out"                 '$C f f | wc -c'
run "devnull"                  '$C f > /dev/null'
run "a f b >>f"                '$C a f b >> f'
run "f a >>f"                  '$C f a >> f'
run "-n f>>f"                  '$C -n f >> f'
run "-A f>>f"                  '$C -A f >> f'
run "-s f>>f"                  '$C -s f >> f'
run "-u f>>f"                  '$C -u f >> f'
run "f twice >>f"              '$C f f >> f'
run "other file >>f"           '$C a >> f'
run "fd 3 is f, out not"       'exec 3>> f; $C f > g'
run "devnull operand >>f"      '$C /dev/null >> f'
run "- twice <f >>f"           '$C - - < f >> f'
run "dir"                      'mkdir d; $C d >> f'
run "missing then f"           '$C nope f >> f'
run "--help >>f"               '$C --help >> f'
run "bad option >>f"           '$C -Q f >> f'
