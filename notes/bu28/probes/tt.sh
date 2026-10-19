#!/usr/bin/env bash
# bu28: timeouttest (plain, then taskset -c 0-3) at the dev tree. usage: tt.sh TAG
L=$HOME/lanes/bu28; tag=$1; cd $L/dev || exit 9
{
echo "tt: $(date -u +%FT%TZ) at $tag (dev tree, $(git status --short | wc -l) changed vs $(git rev-parse --short HEAD)), load $(cat /proc/loadavg); host store $(ls /var/lib/systemd/coredump | wc -l)"
tools/timeouttest-selftest --engine podman --image ubuntu:24.04 --gnu $L/gnu/bin > $L/ev/timeouttest-selftest-$tag.log 2>&1; echo "selftest rc=$?"
tools/timeouttest --engine podman --image ubuntu:24.04 --gnu $L/gnu/bin > $L/ev/timeouttest-$tag-plain.log 2>&1; echo "plain rc=$?"; tail -1 $L/ev/timeouttest-$tag-plain.log
tools/timeouttest --engine podman --image ubuntu:24.04 --gnu $L/gnu/bin --cpus 0-3 --bin target/timeouttest > $L/ev/timeouttest-$tag-cpus.log 2>&1; echo "cpus rc=$?"; tail -1 $L/ev/timeouttest-$tag-cpus.log
echo "host store $(ls /var/lib/systemd/coredump | wc -l); load $(cat /proc/loadavg)"; date -u +%FT%TZ; echo TT-DONE
} > $L/ev/tt-$tag.log 2>&1
