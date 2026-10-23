#!/usr/bin/env bash
set -euo pipefail
exec 9>"$HOME/lanes/hasu-A.lock"
until flock -w 120 9; do echo "waiting for block A: $(date -u +%FT%TZ)"; done
L=$HOME/lanes/bu30
"$L/box" python3 -c 'import os, pathlib, subprocess, tempfile; gnu=pathlib.Path.cwd()/".gnu-bin/bin/mktemp"; t=tempfile.TemporaryDirectory(prefix="bu30-mktemp-perm."); p=pathlib.Path(t.name); (p/"d").mkdir(mode=0); print("uid",os.geteuid(),flush=True); [(print(args,flush=True), print(subprocess.run(["mktemp"]+args,executable=str(gnu),cwd=p,capture_output=True,timeout=2,env={"LC_ALL":"C","PATH":"/usr/bin:/bin"}),flush=True)) for args in [["-u","-p","d","fXXX"],["-uq","-p","d","fXXX"]]]; (p/"d").chmod(0o700); t.cleanup()'
echo MKTEMP-PROBE-DONE
