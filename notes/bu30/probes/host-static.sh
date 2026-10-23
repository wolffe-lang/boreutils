#!/usr/bin/env bash
set -euo pipefail
echo $$ > ~/lanes/bu30/static.pid
exec 9>"$HOME/lanes/hasu-A.lock"
until flock -w 120 9; do echo "waiting for block A: $(date -u +%FT%TZ)"; done
L=$HOME/lanes/bu30
"$L/box" python3 -c 'import runpy; from pathlib import Path; out="/l/boreutils/target/suite"; Path(out).mkdir(parents=True,exist_ok=True); [(print("static build",tool,flush=True), runpy.run_path("tools/"+tool)["build"](out,True)) for tool in ["killtest","timeouttest","idtest","inouttest"]]; runpy.run_path("tools/roottest")["build_static"](out)'
echo STATIC-DONE
