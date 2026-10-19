#!/usr/bin/env bash
# bu28: one THROWAWAY px12-ubuntu container: no network, `ulimit -c 0`, a 16 MiB tmpfs at /w (the only writable
# place), GNU 9.11 at /g, the probes at /p and our programs at /b, all read-only. usage: cbox.sh CMD...
L=$HOME/lanes/bu28
exec podman run --rm --network none --ulimit core=0:0 --user 65534:65534 --tmpfs /w:size=16m,mode=1777 \
  -v "$L/gnu:/g:ro" -v "$L/probes:/p:ro" -v "$L/bin/p4:/b:ro" localhost/px12-ubuntu "$@"
