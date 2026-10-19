#!/usr/bin/env bash
L=$HOME/lanes/bu28
{
echo "run-pin: $(date -u +%FT%TZ) wolf-toolchain.toml sha256 $(sha256sum $L/boreutils/wolf-toolchain.toml | cut -c1-16), load $(cat /proc/loadavg)"
$L/box.sh bash /l/b151.sh /l/tmp/stdd37/std d37c911
$L/box.sh bash /l/b151.sh /l/arch/x/wolf-0.2.33-x86_64-unknown-linux-gnu/std cceda63
echo "b151 done $(date -u +%FT%TZ)"
} > $L/ev/b151.log 2>&1
T=boreutils $L/gauntlet.sh pin
$L/suites.sh pin
echo RUN-PIN-DONE >> $L/ev/b151.log
