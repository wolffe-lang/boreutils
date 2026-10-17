#!/usr/bin/env bash
# bu25: one THROWAWAY px12-ubuntu container: no network, a 16 MiB tmpfs at /w (the only writable place a case uses),
# GNU 9.11 at /g, the probes at /p and our programs at /b, all read-only. usage: cbox.sh root|nobody CMD...
L=$HOME/lanes/bu25
u=$1; shift
case $u in root) U=0:0;; nobody) U=65534:65534;; *) echo "cbox: bad user $u" >&2; exit 2;; esac
exec podman run --rm --network none --user "$U" --tmpfs /w:size=16m,mode=1777 \
  -v "$L/gnu:/g:ro" -v "$L/probes:/p:ro" -v "$L/bin:/b:ro" ${CBOX_EXTRA:-} localhost/px12-ubuntu "$@"
