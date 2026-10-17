#!/usr/bin/env bash
# bu25: run probe $1 against program dir $2 (as seen inside), tag $3, as root and nobody; logs in ev/.
cd "$HOME/lanes/bu25" || exit 9
for u in root nobody; do
  ./cbox.sh "$u" bash "/p/$1.sh" "$2" > "ev/probe-$1-$3-$u.log" 2>&1; echo "$u rc=$?"
done
if diff <(tail -n +2 "ev/probe-$1-$3-root.log") <(tail -n +2 "ev/probe-$1-$3-nobody.log") > /dev/null; then echo "root and nobody SAME"; else echo "root and nobody DIFFER"; fi
