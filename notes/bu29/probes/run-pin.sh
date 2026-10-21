#!/usr/bin/env bash
# bu29: the gauntlet, then the suites, at the pin.
L=$HOME/lanes/bu29
T=boreutils $L/gauntlet.sh pin
$L/suites.sh pin
echo RUN-PIN-DONE > $L/ev/run-pin.done
