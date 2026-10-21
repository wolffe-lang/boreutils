#!/usr/bin/env bash
# bu29: the container suites at a kasumi tree (killtest, inouttest, idtest, timeouttest, roottest and their
# selftests; bu28's suites.sh plus roottest). usage: suites.sh TAG [WHICH...] (kill inout id timeout root)
L=$HOME/lanes/bu29; tag=$1; shift; cd "$L/${T:-boreutils}" || exit 9
which=${*:-kill inout id timeout root}
G=$L/gnu/bin; log=$L/ev/suites-$tag.log
{
  echo "suites: $(date -u +%FT%TZ) at $tag ($(git rev-parse --short HEAD) + $(git status --short | wc -l) changed), load $(cat /proc/loadavg); $which"
  echo "core store before: $(ls /var/lib/systemd/coredump | wc -l)"
  .wolf-bin/wolf --version | head -1; cat .wolf-bin/std/STD-REV
  for w in $which; do case $w in
  kill)
  tools/killtest-selftest --engine podman --image ubuntu:24.04 --gnu $G > $L/ev/killtest-selftest-$tag.log 2>&1; echo "killtest-selftest rc=$?"
  tools/killtest --engine podman --image ubuntu:24.04 --gnu $G --cpus 0-3 > $L/ev/killtest-$tag.log 2>&1; echo "killtest rc=$?"; tail -1 $L/ev/killtest-$tag.log ;;
  inout)
  tools/inouttest-selftest --engine podman --image ubuntu:24.04 --gnu $G > $L/ev/inouttest-selftest-$tag.log 2>&1; echo "inouttest-selftest rc=$?"
  tools/inouttest --engine podman --image ubuntu:24.04 --gnu $G > $L/ev/inouttest-$tag.log 2>&1; echo "inouttest rc=$?"; tail -1 $L/ev/inouttest-$tag.log ;;
  id)
  tools/idtest-selftest --engine podman --image ubuntu:24.04 --gnu $G > $L/ev/idtest-selftest-$tag.log 2>&1; echo "idtest-selftest rc=$?"
  tools/idtest --engine podman --image ubuntu:24.04 --gnu $G > $L/ev/idtest-$tag.log 2>&1; echo "idtest rc=$?"; tail -1 $L/ev/idtest-$tag.log ;;
  timeout)
  tools/timeouttest-selftest --engine podman --image ubuntu:24.04 --gnu $G > $L/ev/timeouttest-selftest-$tag.log 2>&1; echo "timeouttest-selftest rc=$?"
  tools/timeouttest --engine podman --image ubuntu:24.04 --gnu $G --cpus 0-3 > $L/ev/timeouttest-$tag.log 2>&1; echo "timeouttest rc=$?"; tail -1 $L/ev/timeouttest-$tag.log ;;
  root)
  tools/roottest --engine podman --image ubuntu:24.04 --gnu $G > $L/ev/roottest-$tag.log 2>&1; echo "roottest rc=$?"; tail -1 $L/ev/roottest-$tag.log ;;
  esac; done
  echo "core store after: $(ls /var/lib/systemd/coredump | wc -l)"
  echo "load: $(cat /proc/loadavg)"; date -u +%FT%TZ; echo SUITES-DONE
} > "$log" 2>&1
