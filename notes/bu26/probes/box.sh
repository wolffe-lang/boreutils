#!/usr/bin/env bash
# bu26: run a command in a THROWAWAY px12-ubuntu container: no network, nothing of the host mounted but
# ~/lanes/bu26 (at /l) and GNU 9.11 (at /g, read-only), as this user. usage: [T=tree] box.sh CMD...
L=$HOME/lanes/bu26
exec podman run --rm --network none --userns=keep-id -v "$L:/l" -v "$L/gnu:/g:ro" -w "/l/${T:-boreutils}" \
  -e PATH=/g/bin:/usr/local/bin:/usr/bin:/bin -e BORE_GNU_PREFIX= -e BORE_SCRATCH_ROOT=/l/scratch -e TMPDIR=/l/tmp \
  -e HOME=/l/tmp -e CARGO_INCREMENTAL=0 ${BOX_EXTRA:-} localhost/px12-ubuntu "$@"
