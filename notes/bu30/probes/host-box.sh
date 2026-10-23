#!/usr/bin/env bash
export PATH=$HOME/lanes/hasu-env/bin:$HOME/lanes/hasu-env/profile/bin:$PATH
L=$HOME/lanes/bu30
exec podman run --rm --userns keep-id --memory 12g --ulimit core=0:0 -v "$L:/l" -w /l/boreutils -e PATH=/l/boreutils/.gnu-bin/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin -e HOME=/l/tmp -e TMPDIR=/l/tmp -e BORE_SCRATCH_ROOT=/l/scratch localhost/bu30-ubuntu taskset -c 0-5 "$@"
