#!/usr/bin/env bash
# bu29: checkplant at both pins. 0.2.33's archive fetched by trunk's digest and read twice.
L=$HOME/lanes/bu29; A=$L/arch
{
echo "run-checkplant: $(date -u +%FT%TZ) on $(hostname), load $(cat /proc/loadavg)"
n=wolf-0.2.33-x86_64-unknown-linux-gnu.tar.gz; want=4f955e8dfe6eaafa441903eeba43c009c4ec2b45a8da09fe13431e8b12340af8
[ -f $A/$n ] || curl -sSfL --retry 3 -o $A/$n https://github.com/wolffe-lang/wolf-lang/releases/download/v0.2.33/$n
r1=$(sha256sum $A/$n | cut -c1-64); r2=$(sha256sum $A/$n | cut -c1-64)
echo "$n read1 $r1 read2 $r2 pin $want $([ $r1 = $want ] && [ $r2 = $want ] && echo OK || echo MISMATCH)"
[ $r1 = $want ] || exit 1
tar -xzf $A/$n -C $A/x
$L/box.sh bash /l/checkplant.sh /l/arch/x/wolf-0.2.33-x86_64-unknown-linux-gnu/wolf /l/std/cceda63/std 0233
$L/box.sh bash /l/checkplant.sh /l/arch/x/wolf-0.2.34-x86_64-unknown-linux-gnu/wolf /l/std/e036bec/std 0234
echo "done $(date -u +%FT%TZ)"
} > $L/ev/checkplant.log 2>&1
echo RUN-CHECKPLANT-DONE >> $L/ev/checkplant.log
