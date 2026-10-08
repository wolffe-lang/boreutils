# bu17 — the pin at wolf 0.2.25 / lupin 0.1.48

Lane note and contract. **Class:** medium (boreutils), **Opus**. **Wave:**
53. Contract: planning `wolffe-lang/wolf`
`sprints/boreutils/11-the-pin-0225/bu17-the-pin-0225.md` at planning
trunk (fetched 2026-10-07). Branch `bu17` off boreutils `2f15585`.
§1–§3 were committed as `f7d60b7` (and pushed) before any archive was
fetched; this file restates them with the evidence.

## 1. Forbidden

No `rm` outside `~/lanes/bu17/` and this lane's worktree; no
`git add -A`; nothing under `~/.claude`; no build on nomad-1 (every
build, difftest and bench ran on kasumi); no merge, tag or attribution
trailer; no "seen red" without a run id, sha, path or digest; the pin
from the release archives by digest only; GNU coreutils source never
read (GNU's behaviour is the 9.11 oracle, staged by `tools/fetch-oracle`
because kasumi ships 9.12). Strict evidence (wolf-lang#571): every count
below is read from the full output, stderr included; this repository
has no cargo gate, and `tools/difftest` prints its SKIP lines to stdout.
Nothing here spawns or runs concurrently, so no row needed `taskset`.

## 2. Inputs, verified (2026-10-07)

| the contract says | origin says | verdict |
|---|---|---|
| boreutils trunk `2f155851`, 0.2.23 / 0.1.46 | the same; std `6a0df5e` | holds |
| wolf 0.2.25 = `6710f9e0`, release 406122367, `9d91f533…` / `6b0bb90d…` / `202c8d6c…` / windows `9debee73…` | tag object `90f1c11e` → `6710f9e0`; the release API's four digests are those | holds |
| lupin 0.1.48 = `531bf058`, release 405340127, `81cfd77a…` / `a5c30957…` / `27d86060…` / zip `9e4ea090…` / `lupin.exe` `6a6eb6e9…` | tag object `469352f5` → `531bf058`; all five match | holds |
| what 0.2.25 changes: #598/#601 reloads, #600, no new prelude name | the CHANGELOG says so | holds, and **0.2.24 is crossed too** (never pinned here): `fence` in the prelude, #589, #585, #583, `libwolf_rt_none.a` |
| s214 measured 2781/2781 | 2749 passed + 32 skipped on ubuntu (bu16's CI run 37229323186) | the same corpus |
| s200's byte surface is not in 0.2.25 | no `bytes_count`/`fs_copy_chunk` in `wolf prelude --json` (124 names) | holds; bu18 after r31 |
| — | wolf-std trunk moved to `2f389a7` (sc54); sc55 not merged | the std pin moves (B151, below) |

## 3. Prediction, scored

| predicted (`f7d60b7`) | measured | verdict |
|---|---|---|
| all 27 build on both tiers under `--deny-warnings`, at std `6a0df5e` and `2f389a7`, nothing refused, warned or ICE'd | `errors=0 warnings=0 ice=0 built=27` on release and dev, at the pin (`596f37f`, std `6a0df5e`), at std `2f389a7`, and at head | right |
| std: the two candidates give byte-identical binaries; the pin moves to trunk `2f389a7` | release: `bins-release-stdtry-2f389a7.sha256` = `bins-release-pin-596f37f.sha256` (`b9d6fb80…`); dev, built in one tree at both std roots: 27 identical (`678189b6…` both) | right; moved in `013f398` |
| all 27 differ on both tiers, from the version's crate hash and #598/#601's reloads | 27/27 differ on each tier, raw and after `objcopy --strip-debug --remove-section .note.gnu.build-id` (the orchestrator's method note: the native tier writes the compiler version into DWARF). `--emit=wir` at 0.2.23 and 0.2.25 differs in all 27 ONLY by `load` (+8 to +159), `icmp`, `ptr.off`, one `agg` (head, nproc, tee) and one `zext` (printf); no call, store or branch count moved (`wir-opcode-moves.txt` `7d671295…`) | right. The stripped compare cannot attribute the move by itself: `libwolf_rt.a` differs too (`5af08d0e…` → `6ac563e7…`, 0.2.24's #570 pool fix and the crate hash); the WIR is the attribution |
| the utilities' own code grows (loads), never shrinks | in the functions the compiler emits (`_W*` symbols, runtime excluded): **dev** grows in all 27 (+1 to +255 instructions); **release** SHRINKS in 18 of 27 (−7 to −31) and its loads fall in head, seq, tail and wc (`own-*.txt`) | **wrong for release**: LLVM re-optimises around the added loads (block layout and inlining move: `head` 33→34 fns, `tac` 26→25, `sleep` 16→17, `wc` 30→31). The lowering only grows; the release machine code does not follow it one for one |
| #600 moves no binary on its own | the WIR shows no opcode class #600 could account for; s214 measured zero binaries moved by #600 | right (by the WIR) |
| verdict list byte-identical to 0.2.23's (2749 / 0 / 32) | base `2f15585` and pin `596f37f`: `443e432e…` both, 2749 / 0 / 32, on the release AND the dev binaries (`tools/difftest --bin target/dev`); the two difftest logs differ only in the line naming the tree | right |
| the restatement moves 8 SKIP reasons and the `tee` binary only | head `d84db8f`: `6f8d7f2d…`; the base list with `wolf 0.2.23` → `wolf 0.2.25` substituted hashes `6f8d7f2d…` too; release `pin → head` moves `tee` alone | right |
| selftest, `wolf test`, `wolf fmt --check` green; fmt moves nothing | green at base, pin, std try and head | right |
| lupin identity only; the archives gain `libwolf_rt_none.a`, staged unused | `lupin 0.1.48 (wolf-interp, reference interpreter at pin 294d626)`; `libwolf_rt_none.a` in every 0.2.25 archive | right |
| `_wolf` keeps `2d1e4801…` unless the completion script changed | it changed: `a368c8ec…` in all three wolf archives, one line longer (0.2.24's `prelude` subcommand) | the hedge fired; the one-build cross-check holds on the new hash |
| bench within noise of 0.2.23, no row past ±5% on a repeat | the full `tools/bench` (179 rows, both binary sets, GNU beside each) flagged 36 rows past 5% against GNU, mostly from host load (8–28 during the first hour). An A/B with both versions and GNU in one hyperfine call each, at load ~1, cleared all of them except four `unexpand` rows (+6% to +60%), `paste -s` (−5.6%) and `cut -f1` on short lines (−5.5%). A 50-run repeat and `perf stat` instruction counts cleared `printf`, `head`, `cat` and `tee` (instructions within 0.1%) | **wrong for `unexpand`**: 1.51× slower on ordinary lines (+14% instructions, +63% cycles), with identical IR for its hot function. The cause is the release partition moving `flush_run` into `one`'s unit. Filed as **wolf-lang#624** with the witness. `paste` and `cut` are faster by cycles at equal instructions (layout). Everything else is right |
| CI: ubuntu 2749 / 0 / 32, macOS 2709 / 0 / 72, field 2692 / 15 / 74; no macOS ICE | run 37701381298 at `88a0bed`: exactly those, first attempt, no ICE | right |
| no `src/` change beyond the restatement | none | right |

### The bench

The bench was taken on kasumi (linux x86-64, 16 cpus) with hyperfine
1.20.0 and the release tier, against GNU 9.11 (`.gnu-bin`), at full
scale. Each utility ran `tools/bench` twice, once from the 0.2.23 tree
and once from the 0.2.25 tree, sharing one input directory, from
23:07Z to 04:29Z (`bench/host.txt`). The machine was not quiet: other
lanes held the load at 8–28 for the first hour and about 1 from then on.

The **move** column below compares each version against GNU in its own
run, `(b25/g25)/(b23/g23) − 1`, because GNU's own time moved by as much as 71% (`cat` to /dev/null)
between the two runs of the noisy first hour. Rows under 1 ms show
`--`.

Every row past 5% went to an A/B (`ab.py`): ONE hyperfine call with
three commands (0.2.23, 0.2.25, GNU), 10 runs, at load about 1
(`ab-table.md`):

| util | bench | 0.2.23 mean / min ms | 0.2.25 mean / min ms | move (mean) | move (min) | GNU mean ms | GNU / 0.2.25 |
|---|---|---:|---:|---:|---:|---:|---:|
| cat | a large file to /dev/null | 120.0 / 116.9 | 120.3 / 117.0 | +0.3% | +0.0% | 6.0 | 0.05 |
| cat | a large file to a file | 644.0 / 617.0 | 706.0 / 629.6 | +9.6% | +2.0% | 34.8 | 0.05 |
| cat | -n over short lines, to /dev/null | 675.1 / 668.2 | 671.4 / 666.6 | -0.6% | -0.2% | 212.6 | 0.32 |
| cut | -c1-10, UTF-8, where it is not | 5306.7 / 5281.2 | 5328.6 / 5296.5 | +0.4% | +0.3% | 1342.7 | 0.25 |
| cut | -n -b1-10, UTF-8, the partial-character rule | 5844.4 / 5824.2 | 5845.1 / 5818.8 | +0.0% | -0.1% | 2066.0 | 0.35 |
| cut | -f1,3 -d' ', C | 1684.0 / 1672.1 | 1684.6 / 1660.7 | +0.0% | -0.7% | 887.4 | 0.53 |
| cut | -f2- -d' ' --output-delimiter=:, C | 6543.8 / 6507.0 | 6660.7 / 6598.8 | +1.8% | +1.4% | 3592.4 | 0.54 |
| cut | --complement -b1-10, C | 1497.5 / 1481.1 | 1497.8 / 1487.0 | +0.0% | +0.4% | 417.7 | 0.28 |
| cut | -f1 -d' ' on very short lines, C | 466.6 / 460.1 | 439.7 / 434.7 | -5.8% | -5.5% | 289.9 | 0.66 |
| cut | -b1-10 on binary noise, C | 135.2 / 134.1 | 135.6 / 134.7 | +0.3% | +0.4% | 40.3 | 0.30 |
| expand | a tab-heavy input, which is the amortized case | 11855.4 / 11767.7 | 11836.3 / 11777.9 | -0.2% | +0.1% | 11916.5 | 1.01 |
| fold | -b, ordinary lines at the default width | 3125.0 / 3100.0 | 3127.9 / 3114.2 | +0.1% | +0.5% | 2876.7 | 0.92 |
| fold | the default column mode, ordinary lines | 3643.9 / 3623.1 | 3646.9 / 3633.6 | +0.1% | +0.3% | 4721.2 | 1.29 |
| fold | -c in the C locale, which is bytes | 3129.6 / 3101.2 | 3127.8 / 3105.2 | -0.1% | +0.1% | 3657.3 | 1.17 |
| fold | the column mode under UTF-8, which decodes and looks up a width | 5921.5 / 5905.8 | 5919.8 / 5906.4 | -0.0% | +0.0% | 4911.7 | 0.83 |
| head | -n 100000 of short lines | 4.5 / 2.8 | 7.1 / 3.0 | +59.6% | +6.6% | 7.8 | 1.09 |
| head | -c 100000000, a bulk copy | 12.5 / 9.5 | 9.9 / 9.6 | -20.7% | +1.0% | 12.0 | 1.21 |
| head | -n -1 of short lines | 11.3 / 7.3 | 11.2 / 6.7 | -0.5% | -8.7% | 17.4 | 1.55 |
| paste | -s, ordinary lines | 2857.9 / 2843.5 | 2696.4 / 2685.6 | -5.7% | -5.6% | 1211.8 | 0.45 |
| paste | -s with a two-item delimiter list | 2859.4 / 2843.8 | 2696.4 / 2685.5 | -5.7% | -5.6% | 1205.4 | 0.45 |
| printf | %d over 10,000 integers | 8.0 / 5.7 | 20.3 / 7.8 | +154.5% | +37.8% | 20.3 | 1.00 |
| printf | %x over 10,000 integers | 18.2 / 9.4 | 13.1 / 6.3 | -27.9% | -33.0% | 12.1 | 0.92 |
| printf | %s over 10,000 words | 3.9 / 3.1 | 3.7 / 3.1 | -3.2% | +0.5% | 24.7 | 6.61 |
| printf | %.6f over 10,000 decimals | 27.0 / 25.5 | 28.8 / 25.3 | +6.7% | -0.7% | 28.6 | 1.00 |
| printf | %g over 10,000 decimals | 37.8 / 35.5 | 36.8 / 34.5 | -2.6% | -2.8% | 10.4 | 0.28 |
| seq | a million integers | 72.5 / 71.4 | 73.3 / 72.7 | +1.1% | +1.8% | 5.6 | 0.08 |
| seq | a million integers, a comma separator | 72.6 / 72.1 | 73.9 / 72.9 | +1.8% | +1.1% | 8.0 | 0.11 |
| seq | a million integers of six digits | 72.7 / 71.2 | 73.7 / 72.3 | +1.3% | +1.5% | 7.6 | 0.10 |
| sort | binary noise | 1930.8 / 1918.0 | 1902.5 / 1871.0 | -1.5% | -2.5% | 313.4 | 0.16 |
| tee | to a file and /dev/null | 642.6 / 613.0 | 683.0 / 600.4 | +6.3% | -2.1% | 809.5 | 1.19 |
| tee | to two files and /dev/null | 2786.3 / 1382.9 | 1468.3 / 1388.4 | -47.3% | +0.4% | 1590.1 | 1.08 |
| unexpand | ordinary lines, single spaces, nothing to convert | 2593.6 / 2578.1 | 4182.4 / 4132.9 | +61.3% | +60.3% | 5902.6 | 1.41 |
| unexpand | very short lines | 286.4 / 278.7 | 311.4 / 307.0 | +8.7% | +10.1% | 622.3 | 2.00 |
| unexpand | the default, leading runs only | 834.1 / 806.7 | 889.4 / 885.0 | +6.6% | +9.7% | 1550.2 | 1.74 |
| unexpand | binary noise | 685.5 / 670.9 | 721.1 / 710.5 | +5.2% | +5.9% | 5981.2 | 8.29 |
| yes | 1 GiB of `y` into head -c | 180.6 / 174.7 | 181.8 / 176.7 | +0.7% | +1.1% | 112.4 | 0.62 |

A/B rows: 36; past 5% by both mean and min: 10

The rows under 30 ms and the file-writing rows were re-run at 50 runs
(`ab50-table.md`) and counted with `perf stat` (user instructions, 5–100
runs):

| row | instructions:u | cycles:u |
|---|---:|---:|
| `printf '%d'` over 10,000 integers | +0.09% | +2.8% |
| `printf '%x'` over 10,000 integers | +0.07% | +0.1% |
| `cat` 256 MiB to a file | −0.00% | −3.2% |
| `tee` 256 MiB to a file | −0.00% | −0.1% |
| `head -n -1` of short lines | +0.01% | +2.8% |
| `unexpand`, ordinary lines (256 MiB) | **+14.4%** | **+63.0%** |
| `unexpand`, very short lines | **+14.5%** | **+9.9%** |
| `unexpand` on binary noise | **+13.8%** | **+9.9%** |
| `paste -s` (256 MiB) | −0.00% | −5.9% |
| `cut -f1 -d' '` on short lines | −0.28% | −5.4% |

**`unexpand` is the one real regression, and it is not the reloads.**
- `@one` (`unexpand`'s pass over a chunk, 96–97% of its time under
  `perf`) is identical at both versions: the same WIR (422 lines), and
  the same LLVM IR (1608 lines) with every metadata node resolved.
- Each unit's IR was captured through a `WOLF_CLANG` wrapper. At 0.2.23
  `_Wone`'s unit defines `_Wone` and `_Wbore.wide`; at 0.2.25 it also
  defines `_Wflush_run`.
- The partition's affinity pass fused the caller and callee because
  unrelated functions grew (`bore.parse`, `rewrite_obsolete`).
- Declaring `_Wflush_run` instead of defining it in 0.2.25's unit
  makes clang 23.1.1 emit `_Wone` instruction for instruction as 0.2.23
  does (`ae529a8a…` both).
- Filed as wolf-lang#624, with the witness in
  `perf/witness-unexpand/`. Nothing in this repository works around it:
  the partition is the compiler's, and a source change to move a fn
  between units would be pinning around it. The README states the loss.

The bench of record, every row:

| util | bench | 0.2.23 ms | 0.2.25 ms | move | GNU ms (base run / pin run) | move against GNU | GNU / 0.2.25 |
|---|---|---:|---:|---:|---:|---:|---:|
| basename | one path | 0.7 ± 0.3 | 0.3 ± 0.0 | (<1 ms) | 0.2 / 0.2 | -- | -- |
| basename | 50 paths with -a | 0.5 ± 0.1 | 0.7 ± 0.1 | (<1 ms) | 0.7 / 0.8 | -- | -- |
| cat | a large file to /dev/null | 304.7 ± 64.7 | 169.7 ± 11.6 | -44.3% | 24.0 / 6.9 | +93.7% ** | 0.04 |
| cat | a large file to a file | 1063.9 ± 71.7 | 503.8 ± 76.0 | -52.6% | 102.5 / 41.5 | +17.0% ** | 0.08 |
| cat | -n over short lines, to /dev/null | 957.1 ± 168.9 | 818.8 ± 17.3 | -14.4% | 244.8 / 245.3 | -14.6% ** | 0.30 |
| cat | 64 operands, to /dev/null | 631.9 ± 36.1 | 590.4 ± 21.8 | -6.6% | 18.6 / 18.1 | -4.0% | 0.03 |
| cut | -b1-10, C | 944.5 ± 4.8 | 914.5 ± 7.5 | -3.2% | 444.4 / 439.1 | -2.0% | 0.48 |
| cut | -c1-10, C, where a character is a byte | 946.6 ± 8.1 | 859.5 ± 21.7 | -9.2% | 441.4 / 410.3 | -2.3% | 0.48 |
| cut | -c1-10, UTF-8, where it is not | 7393.1 ± 895.8 | 5776.7 ± 78.2 | -21.9% | 2106.2 / 1564.0 | +5.2% ** | 0.27 |
| cut | -n -b1-10, UTF-8, the partial-character rule | 9229.7 ± 1950.7 | 7054.2 ± 370.6 | -23.6% | 2349.8 / 2213.6 | -18.9% ** | 0.31 |
| cut | -f1 -d' ', C | 1216.5 ± 19.6 | 1147.3 ± 12.9 | -5.7% | 566.5 / 557.3 | -4.1% | 0.49 |
| cut | -f1,3 -d' ', C | 1891.5 ± 62.2 | 2180.9 ± 627.5 | +15.3% | 1005.3 / 987.5 | +17.4% ** | 0.45 |
| cut | -f2- -d' ' --output-delimiter=:, C | 7756.2 ± 354.8 | 8409.8 ± 297.8 | +8.4% | 3948.9 / 4066.4 | +5.3% ** | 0.48 |
| cut | --complement -b1-10, C | 1634.8 ± 36.4 | 1739.7 ± 23.7 | +6.4% | 478.0 / 537.8 | -5.4% ** | 0.31 |
| cut | -b1-10 on very short lines, C | 373.3 ± 3.9 | 375.1 ± 4.7 | +0.5% | 222.2 / 225.7 | -1.1% | 0.60 |
| cut | -f1 -d' ' on very short lines, C | 526.0 ± 5.9 | 565.6 ± 10.0 | +7.5% | 324.3 / 329.5 | +5.8% ** | 0.58 |
| cut | -b1-10 on binary noise, C | 150.7 ± 2.9 | 171.9 ± 1.6 | +14.1% | 42.7 / 59.4 | -18.0% ** | 0.35 |
| echo | one short string | 0.4 ± 0.2 | 0.4 ± 0.5 | (<1 ms) | 0.2 / 0.2 | -- | -- |
| echo | 200 arguments with escapes | 0.6 ± 0.2 | 0.6 ± 0.2 | (<1 ms) | 0.5 / 0.5 | -- | -- |
| expand | start-up, no input | 0.7 ± 0.4 | 0.4 ± 0.1 | (<1 ms) | 0.4 / 0.3 | -- | -- |
| expand | ordinary lines with no tab in them | 2900.4 ± 17.2 | 2604.8 ± 16.5 | -10.2% | 8787.7 / 8164.5 | -3.3% | 3.13 |
| expand | very short lines with no tab in them | 276.6 ± 2.4 | 271.8 ± 1.6 | -1.7% | 916.8 / 868.5 | +3.7% | 3.20 |
| expand | -t 4, a denser stop list | 2857.6 ± 14.2 | 2670.2 ± 10.3 | -6.6% | 8738.0 / 8260.3 | -1.2% | 3.09 |
| expand | -t 3,7, two explicit stops and a single space past them | 2846.3 ± 18.6 | 2794.3 ± 17.8 | -1.8% | 8709.2 / 8411.4 | +1.6% | 3.01 |
| expand | -t 3,/5, a repeat past the last stop | 2888.3 ± 47.1 | 2688.1 ± 45.1 | -6.9% | 9061.0 / 8374.8 | +0.7% | 3.12 |
| expand | -i, which stops at the first non-blank of each line | 2889.1 ± 14.8 | 2693.1 ± 24.9 | -6.8% | 6559.9 / 6168.7 | -0.9% | 2.29 |
| expand | under UTF-8, where every character is decoded | 2853.0 ± 36.7 | 2652.7 ± 16.1 | -7.0% | 8866.0 / 8273.0 | -0.4% | 3.12 |
| expand | a tab-heavy input, which is the amortized case | 12826.6 ± 176.7 | 12399.2 ± 63.9 | -3.3% | 12119.5 / 12370.0 | -5.3% ** | 1.00 |
| expand | a tab-heavy input at -t 1, where a tab is one space | 12096.6 ± 108.7 | 12363.9 ± 82.8 | +2.2% | 12145.1 / 12340.6 | +0.6% | 1.00 |
| expand | binary noise | 659.5 ± 2.7 | 661.2 ± 2.2 | +0.3% | 5825.6 / 5796.3 | +0.8% | 8.77 |
| fold | start-up, no input | 0.7 ± 0.1 | 0.8 ± 0.1 | (<1 ms) | 0.4 / 0.4 | -- | -- |
| fold | -b, ordinary lines at the default width | 3244.3 ± 31.1 | 3235.3 ± 40.4 | -0.3% | 3110.8 / 2891.2 | +7.3% ** | 0.89 |
| fold | -b, a width that breaks every line | 3271.5 ± 45.8 | 3133.6 ± 20.7 | -4.2% | 3301.7 / 3082.7 | +2.6% | 0.98 |
| fold | the default column mode, ordinary lines | 3750.3 ± 15.7 | 3656.3 ± 23.9 | -2.5% | 5304.2 / 4710.0 | +9.8% ** | 1.29 |
| fold | the default column mode, a width that breaks every line | 3817.0 ± 59.1 | 3657.7 ± 10.9 | -4.2% | 4945.4 / 4969.6 | -4.6% | 1.36 |
| fold | -c in the C locale, which is bytes | 3170.0 ± 68.4 | 3141.9 ± 22.9 | -0.9% | 4006.3 / 3624.3 | +9.6% ** | 1.15 |
| fold | -c under UTF-8, which decodes | 4215.2 ± 133.2 | 3976.4 ± 136.5 | -5.7% | 4041.4 / 3664.9 | +4.0% | 0.92 |
| fold | the column mode under UTF-8, which decodes and looks up a width | 6201.3 ± 71.4 | 5969.7 ± 141.4 | -3.7% | 5152.5 / 5407.8 | -8.3% ** | 0.91 |
| fold | -s at a width that breaks every line | 4812.2 ± 39.7 | 4743.8 ± 28.0 | -1.4% | 8131.4 / 8144.7 | -1.6% | 1.72 |
| fold | -s -b at the same width | 4073.3 ± 18.0 | 4087.9 ± 13.5 | +0.4% | 5890.1 / 5888.6 | +0.4% | 1.44 |
| fold | -w 1, the worst break rate there is | 484.2 ± 34.2 | 475.5 ± 4.5 | -1.8% | 586.2 / 583.4 | -1.3% | 1.23 |
| fold | very short lines, where nothing breaks | 363.5 ± 4.3 | 364.0 ± 4.9 | +0.1% | 427.2 / 427.7 | +0.0% | 1.18 |
| fold | binary noise, one enormous line | 769.1 ± 4.2 | 774.9 ± 9.6 | +0.8% | 3777.3 / 3723.5 | +2.2% | 4.81 |
| head | -n 1 of a whole GiB, which must not read a GiB | 0.4 ± 0.1 | 0.4 ± 0.1 | (<1 ms) | 0.2 / 0.2 | -- | -- |
| head | -c 1 of the same | 0.3 ± 0.0 | 0.3 ± 0.0 | (<1 ms) | 0.2 / 0.2 | -- | -- |
| head | -n 10, the default | 0.4 ± 0.0 | 0.4 ± 0.0 | (<1 ms) | 0.2 / 0.2 | -- | -- |
| head | -n 1 through a pipe, where neither side may seek | 0.6 ± 0.0 | 0.6 ± 0.0 | (<1 ms) | 0.4 / 0.4 | -- | -- |
| head | -n 100000 of short lines | 1.4 ± 0.1 | 1.3 ± 0.1 | -7.1% | 1.2 / 4.4 | -74.7% ** | 3.38 |
| head | -c 100000000, a bulk copy | 12.5 ± 0.8 | 13.1 ± 5.3 | +4.8% | 11.3 / 9.6 | +23.4% ** | 0.73 |
| head | -c -1024, which a trusted end turns into a bulk copy | 117.8 ± 4.0 | 114.9 ± 1.4 | -2.5% | 98.5 / 98.0 | -2.0% | 0.85 |
| head | -c -1024 through a pipe, where the window is the only way | 912.7 ± 16.7 | 918.0 ± 13.8 | +0.6% | 119.9 / 119.9 | +0.6% | 0.13 |
| head | -n -1, all but the last line: a walk back, then a copy | 122.0 ± 3.8 | 118.8 ± 1.2 | -2.6% | 98.7 / 100.2 | -4.1% | 0.84 |
| head | -n -1 of short lines | 15.1 ± 4.6 | 11.2 ± 2.8 | -25.8% | 13.1 / 12.7 | -23.5% ** | 1.13 |
| head | -c -1024 of standard input that is a file | 119.6 ± 1.7 | 119.5 ± 4.9 | -0.1% | 97.4 / 97.4 | -0.1% | 0.82 |
| head | -n -1 of standard input that is a file | 123.6 ± 1.2 | 124.3 ± 1.6 | +0.6% | 99.8 / 99.6 | +0.8% | 0.80 |
| head | -n -1 through a pipe, where the window is the only way | 1123.9 ± 14.2 | 1148.2 ± 14.0 | +2.2% | 301.4 / 301.1 | +2.3% | 0.26 |
| nl | start-up, no input | 4.3 ± 0.8 | 4.3 ± 0.8 | +0.0% | 4.7 / 4.6 | +2.2% | 1.07 |
| nl | very short lines | 879.1 ± 1.6 | 889.7 ± 2.6 | +1.2% | 858.3 / 866.2 | +0.3% | 0.97 |
| nl | very short lines, every one numbered | 1012.0 ± 15.0 | 1018.4 ± 7.9 | +0.6% | 1002.0 / 991.5 | +1.7% | 0.97 |
| nl | very short lines, zero filled | 1787.7 ± 15.1 | 1842.2 ± 11.0 | +3.0% | 900.9 / 905.8 | +2.5% | 0.49 |
| nl | ordinary lines | 2191.8 ± 24.6 | 2208.6 ± 15.6 | +0.8% | 1890.4 / 1899.5 | +0.3% | 0.86 |
| nl | ordinary lines, no numbers at all | 2215.0 ± 40.4 | 2279.1 ± 42.6 | +2.9% | 1164.8 / 1166.8 | +2.7% | 0.51 |
| nl | ordinary lines, a regular expression per line | 4476.3 ± 23.7 | 4554.0 ± 31.3 | +1.7% | 2543.1 / 2542.3 | +1.8% | 0.56 |
| nproc | the schedulable count | 0.2 ± 0.0 | 0.3 ± 0.0 | (<1 ms) | 3.7 / 0.2 | -- | -- |
| nproc | --all, the installed count | 1.5 ± 0.1 | 0.3 ± 0.0 | -80.0% | 1.2 / 0.2 | -- | -- |
| paste | start-up, no input | 0.7 ± 0.1 | 0.7 ± 0.1 | (<1 ms) | 0.3 / 0.3 | -- | -- |
| paste | -s, ordinary lines | 2859.4 ± 23.4 | 2694.0 ± 15.0 | -5.8% | 1204.8 / 1213.6 | -6.5% ** | 0.45 |
| paste | -s, very short lines | 429.6 ± 8.6 | 429.8 ± 10.2 | +0.0% | 244.4 / 243.7 | +0.3% | 0.57 |
| paste | -s with a two-item delimiter list | 2855.8 ± 22.2 | 2693.9 ± 12.8 | -5.7% | 1202.9 / 1206.0 | -5.9% ** | 0.45 |
| paste | one file, which is a copy with a record terminator | 2809.4 ± 22.6 | 2731.8 ± 25.3 | -2.8% | 1088.3 / 1086.5 | -2.6% | 0.40 |
| paste | two files side by side | 5641.1 ± 45.6 | 5618.7 ± 333.4 | -0.4% | 2303.8 / 2304.9 | -0.4% | 0.41 |
| paste | two files of very short lines | 761.1 ± 12.4 | 768.6 ± 7.3 | +1.0% | 354.9 / 354.9 | +1.0% | 0.46 |
| paste | four files side by side | 11259.7 ± 97.6 | 11017.0 ± 50.1 | -2.2% | 4466.5 / 4471.9 | -2.3% | 0.41 |
| paste | two files with a delimiter list | 5672.2 ± 40.6 | 5503.8 ± 34.6 | -3.0% | 2282.7 / 2282.1 | -2.9% | 0.41 |
| paste | two files with no delimiter at all | 5688.8 ± 31.0 | 5528.3 ± 42.3 | -2.8% | 2247.5 / 2253.8 | -3.1% | 0.41 |
| paste | a pipe paired with itself, which reads one stream twice | 448.1 ± 7.9 | 457.9 ± 11.4 | +2.2% | 232.8 / 235.4 | +1.1% | 0.51 |
| printenv | one variable | 0.2 ± 0.0 | 0.2 ± 0.1 | (<1 ms) | 3.4 / 0.2 | -- | -- |
| printenv | the whole environment | 2.4 ± 0.1 | 0.4 ± 0.0 | -83.3% | 2.1 / 0.3 | -- | -- |
| printf | start-up, a plain format | 0.4 ± 0.0 | 0.4 ± 0.1 | (<1 ms) | 0.3 / 0.4 | -- | -- |
| printf | %d over 10,000 integers | 16.7 ± 6.4 | 12.6 ± 6.8 | -24.6% | 21.3 / 5.0 | +221.4% ** | 0.40 |
| printf | %x over 10,000 integers | 12.8 ± 7.8 | 18.5 ± 8.4 | +44.5% | 20.2 / 21.6 | +35.2% ** | 1.17 |
| printf | %s over 10,000 words | 23.0 ± 4.3 | 19.3 ± 8.6 | -16.1% | 24.8 / 19.4 | +7.3% ** | 1.01 |
| printf | %.6f over 10,000 decimals | 26.9 ± 0.8 | 26.2 ± 1.2 | -2.6% | 14.6 / 18.8 | -24.4% ** | 0.72 |
| printf | %g over 10,000 decimals | 37.9 ± 1.7 | 37.4 ± 2.8 | -1.3% | 9.6 / 20.1 | -52.9% ** | 0.54 |
| printf | %e over 10,000 decimals | 37.6 ± 3.5 | 31.5 ± 1.5 | -16.2% | 21.2 / 17.4 | +2.1% | 0.55 |
| pwd | the physical directory | 0.2 ± 0.0 | 0.2 ± 0.0 | (<1 ms) | 3.3 / 0.2 | -- | -- |
| pwd | -L through $PWD | 1.4 ± 0.6 | 0.3 ± 0.0 | -78.6% | 0.4 / 0.2 | -- | -- |
| seq | start-up, one number | 0.2 ± 0.0 | 0.2 ± 0.0 | (<1 ms) | 0.2 / 0.2 | -- | -- |
| seq | a million integers | 74.9 ± 1.3 | 75.1 ± 0.5 | +0.3% | 10.4 / 4.9 | +112.8% ** | 0.07 |
| seq | a million integers, equal width | 119.9 ± 0.4 | 119.0 ± 0.4 | -0.8% | 149.7 / 150.9 | -1.5% | 1.27 |
| seq | a million integers, a comma separator | 74.3 ± 1.0 | 75.1 ± 0.6 | +1.1% | 6.4 / 10.3 | -37.2% ** | 0.14 |
| seq | a million thousandths | 74.5 ± 1.0 | 75.3 ± 1.3 | +1.1% | 137.2 / 137.4 | +0.9% | 1.82 |
| seq | a million integers through a format | 114.0 ± 0.4 | 114.0 ± 1.3 | +0.0% | 144.1 / 142.6 | +1.1% | 1.25 |
| seq | a million integers of six digits | 75.2 ± 1.6 | 76.5 ± 2.3 | +1.7% | 12.6 / 8.2 | +56.3% ** | 0.11 |
| sleep | start-up, sleep 0 | 0.2 ± 0.0 | 1.9 ± 0.1 | (<1 ms) | 0.2 / 1.6 | -- | 0.84 |
| sleep | sleep 0.1 | 104.3 ± 0.1 | 101.7 ± 0.1 | -2.5% | 104.1 / 101.5 | +0.0% | 1.00 |
| sleep | sleep 0.0105, between two milliseconds | 12.7 ± 0.1 | 12.7 ± 0.1 | +0.0% | 11.9 / 11.9 | +0.0% | 0.94 |
| sort | start-up, no input | 5.7 ± 0.3 | 0.9 ± 0.1 | -84.2% | 3.3 / 0.4 | -- | -- |
| sort | whole lines, a file operand | 17810.3 ± 47.9 | 18897.4 ± 344.7 | +6.1% | 3445.3 / 3602.9 | +1.5% | 0.19 |
| sort | whole lines, through a pipe | 17882.9 ± 55.6 | 18749.8 ± 196.7 | +4.8% | 3414.5 / 3449.1 | +3.8% | 0.18 |
| sort | whole lines, one thread each (--parallel=1) | 17849.2 ± 56.1 | 18406.0 ± 114.7 | +3.1% | 6876.7 / 7066.7 | +0.3% | 0.38 |
| sort | very short lines | 7070.8 ± 19.0 | 7420.5 ± 91.6 | +4.9% | 1718.8 / 1763.6 | +2.3% | 0.24 |
| sort | binary noise | 1927.9 ± 6.2 | 1992.3 ± 13.1 | +3.3% | 313.7 / 240.7 | +34.7% ** | 0.12 |
| sort | -r | 17925.5 ± 39.3 | 18080.0 ± 367.8 | +0.9% | 3458.9 / 3447.1 | +1.2% | 0.19 |
| sort | -u | 18762.1 ± 58.6 | 18767.9 ± 57.9 | +0.0% | 3469.0 / 3498.9 | -0.8% | 0.19 |
| sort | -f | 26999.4 ± 148.4 | 27951.7 ± 608.0 | +3.5% | 4101.2 / 4165.6 | +1.9% | 0.15 |
| sort | -n (text, so every line is zero and the last resort decides) | 26086.6 ± 38.0 | 26386.7 ± 461.0 | +1.2% | 4670.6 / 4668.4 | +1.2% | 0.18 |
| sort | -t ' ' -k2,2, a one-field key | 44657.1 ± 743.8 | 44166.3 ± 67.7 | -1.1% | 3977.1 / 3948.1 | -0.4% | 0.09 |
| sort | -k2, a key to the end of the line | 36385.8 ± 66.1 | 36530.2 ± 62.0 | +0.4% | 3931.7 / 3938.3 | +0.2% | 0.11 |
| sort | -s -k1,1, stable on a short key | 32664.8 ± 313.6 | 32994.9 ± 199.9 | +1.0% | 3807.0 / 3706.2 | +3.8% | 0.11 |
| sort | the external merge, -S 10M | 14716.7 ± 323.6 | 14456.6 ± 67.6 | -1.8% | 6771.2 / 6673.0 | -0.3% | 0.46 |
| tac | start-up, no input | 0.5 ± 0.1 | 4.6 ± 0.9 | (<1 ms) | 0.3 / 4.6 | -- | 1.00 |
| tac | ordinary lines, a file operand | 2918.8 ± 24.4 | 2967.1 ± 15.3 | +1.7% | 549.6 / 550.5 | +1.5% | 0.19 |
| tac | ordinary lines, through a pipe | 2928.7 ± 20.5 | 2955.6 ± 25.0 | +0.9% | 551.4 / 549.0 | +1.4% | 0.19 |
| tac | very short lines, a file operand | 335.4 ± 2.9 | 333.4 ± 3.3 | -0.6% | 208.4 / 207.5 | -0.2% | 0.62 |
| tac | very short lines, through a pipe | 336.2 ± 3.2 | 334.2 ± 4.1 | -0.6% | 206.2 / 206.3 | -0.6% | 0.62 |
| tac | -b, the separator before its record | 2928.7 ± 18.4 | 3080.3 ± 141.0 | +5.2% | 530.0 / 552.7 | +0.9% | 0.18 |
| tac | -s, a one-character separator that is not a newline | 4423.2 ± 55.6 | 4529.2 ± 38.6 | +2.4% | 2213.3 / 2310.2 | -1.9% | 0.51 |
| tac | -s, a separator of several characters | 2982.5 ± 22.3 | 3102.1 ± 36.9 | +4.0% | 617.1 / 645.1 | -0.5% | 0.21 |
| tac | -r, a literal expression | 4891.3 ± 93.4 | 5155.8 ± 42.5 | +5.4% | 10430.6 / 10758.3 | +2.2% | 2.09 |
| tac | -r, a bracket expression with a quantifier | 7303.1 ± 62.8 | 7588.6 ± 43.9 | +3.9% | 15047.5 / 15192.8 | +2.9% | 2.00 |
| tac | binary noise, no separator anywhere near | 700.2 ± 13.1 | 729.2 ± 26.4 | +4.1% | 143.9 / 149.5 | +0.2% | 0.21 |
| tail | -n 10 of a file, read back from the end | 0.3 ± 0.0 | 0.3 ± 0.1 | (<1 ms) | 0.2 / 0.2 | -- | -- |
| tail | -c 10 of a file, a positional read of ten bytes | 0.3 ± 0.0 | 0.3 ± 0.0 | (<1 ms) | 0.2 / 0.2 | -- | -- |
| tail | -n 10 of standard input that is a file | 0.4 ± 0.0 | 0.4 ± 0.0 | (<1 ms) | 0.4 / 0.3 | -- | -- |
| tail | -c 10 of standard input that is a file | 0.4 ± 0.0 | 0.4 ± 0.0 | (<1 ms) | 0.3 / 0.4 | -- | -- |
| tail | -n 10 through a pipe, where neither side may seek | 435.2 ± 2.5 | 422.1 ± 6.4 | -3.0% | 275.4 / 276.2 | -3.3% | 0.65 |
| tail | -c 10 through a pipe | 111.5 ± 1.0 | 112.4 ± 1.7 | +0.8% | 109.5 / 110.8 | -0.4% | 0.99 |
| tail | -n 10 of short lines through a pipe | 127.7 ± 3.2 | 132.3 ± 0.5 | +3.6% | 76.1 / 75.2 | +4.8% | 0.57 |
| tail | -n +1, the whole file, which is a copy | 120.7 ± 3.0 | 121.6 ± 1.6 | +0.7% | 101.9 / 103.4 | -0.7% | 0.85 |
| tail | -c +100000000, a skip and then a copy | 108.2 ± 1.4 | 111.2 ± 2.6 | +2.8% | 91.8 / 90.6 | +4.1% | 0.81 |
| tail | -n 100000 of short lines, a walk back a hundred thousand lines | 1.6 ± 0.0 | 1.7 ± 0.0 | +6.2% | 0.8 / 0.9 | -- | -- |
| tee | to /dev/null, no file | 120.6 ± 2.0 | 124.0 ± 4.1 | +2.8% | 87.1 / 88.3 | +1.4% | 0.71 |
| tee | to a file and /dev/null | 468.3 ± 12.4 | 694.6 ± 70.8 | +48.3% | 788.9 / 768.0 | +52.4% ** | 1.11 |
| tee | to two files and /dev/null | 1145.5 ± 32.6 | 1521.4 ± 208.8 | +32.8% | 1427.2 / 1585.2 | +19.6% ** | 1.04 |
| tr | start-up, no input | 0.4 ± 0.0 | 0.4 ± 0.1 | (<1 ms) | 0.3 / 0.3 | -- | -- |
| tr | translate a range | 1065.2 ± 11.8 | 1072.8 ± 26.7 | +0.7% | 357.9 / 346.8 | +3.9% | 0.32 |
| tr | translate a class pair | 1063.1 ± 10.9 | 1072.4 ± 7.7 | +0.9% | 350.5 / 356.2 | -0.7% | 0.33 |
| tr | delete one character | 1542.2 ± 24.0 | 1585.2 ± 8.5 | +2.8% | 691.1 / 711.4 | -0.1% | 0.45 |
| tr | delete the complement of a class | 2773.6 ± 71.9 | 2701.6 ± 24.4 | -2.6% | 1775.7 / 1754.2 | -1.4% | 0.65 |
| tr | squeeze spaces | 1725.0 ± 19.0 | 1636.1 ± 6.0 | -5.2% | 1492.5 / 1439.9 | -1.7% | 0.88 |
| tr | translate then squeeze | 1735.7 ± 8.6 | 1659.2 ± 6.0 | -4.4% | 6288.6 / 6102.0 | -1.5% | 3.68 |
| tr | delete over binary noise | 598.5 ± 16.9 | 559.4 ± 7.2 | -6.5% | 366.9 / 347.3 | -1.3% | 0.62 |
| unexpand | start-up, no input | 0.3 ± 0.0 | 4.3 ± 1.2 | (<1 ms) | 0.2 / 4.6 | -- | 1.07 |
| unexpand | ordinary lines, single spaces, nothing to convert | 2629.9 ± 51.0 | 4212.4 ± 15.5 | +60.2% | 5980.7 / 5919.2 | +61.8% ** | 1.41 |
| unexpand | very short lines | 279.5 ± 2.3 | 309.0 ± 4.3 | +10.6% | 616.4 / 617.1 | +10.4% ** | 2.00 |
| unexpand | -a over single spaces, which is the run-of-one rule at full rate | 4435.0 ± 13.9 | 4455.5 ± 9.2 | +0.5% | 11537.3 / 11465.6 | +1.1% | 2.57 |
| unexpand | -a over long runs of blanks | 1253.9 ± 13.5 | 1243.9 ± 9.9 | -0.8% | 1261.0 / 1249.9 | +0.1% | 1.00 |
| unexpand | -t 4 over long runs of blanks | 1255.5 ± 7.4 | 1244.5 ± 17.9 | -0.9% | 1253.2 / 1251.8 | -0.8% | 1.01 |
| unexpand | -t 3,7 over long runs, where the list ends | 1246.3 ± 9.9 | 1251.5 ± 8.6 | +0.4% | 1251.9 / 1245.6 | +0.9% | 1.00 |
| unexpand | the default, leading runs only | 806.7 ± 3.6 | 888.7 ± 17.4 | +10.2% | 1520.9 / 1534.5 | +9.2% ** | 1.73 |
| unexpand | under UTF-8, where every character is decoded | 4565.8 ± 156.2 | 4541.4 ± 4.9 | -0.5% | 11557.8 / 11499.1 | -0.0% | 2.53 |
| unexpand | binary noise | 878.8 ± 650.8 | 713.9 ± 3.3 | -18.8% | 5961.7 / 6087.2 | -20.4% ** | 8.53 |
| uniq | start-up, no input | 0.6 ± 0.1 | 0.4 ± 0.0 | (<1 ms) | 0.4 / 0.3 | -- | -- |
| uniq | very short lines | 399.4 ± 7.3 | 374.8 ± 4.9 | -6.2% | 358.4 / 352.3 | -4.5% | 0.94 |
| uniq | very short lines, counted | 1545.2 ± 15.7 | 1548.6 ± 12.8 | +0.2% | 922.1 / 924.5 | -0.0% | 0.60 |
| uniq | ordinary lines | 2647.9 ± 23.7 | 2516.3 ± 26.0 | -5.0% | 1107.1 / 1092.2 | -3.7% | 0.43 |
| uniq | ordinary lines, a field skipped | 3118.6 ± 27.3 | 2943.0 ± 45.2 | -5.6% | 1470.8 / 1454.7 | -4.6% | 0.49 |
| uniq | ordinary lines, case folded | 2601.0 ± 36.2 | 2441.6 ± 15.0 | -6.1% | 1097.6 / 1072.6 | -3.9% | 0.44 |
| uniq | every line of every repeating group | 285.2 ± 2.1 | 278.1 ± 2.2 | -2.5% | 299.3 / 288.2 | +1.3% | 1.04 |
| wc | -c on a file, C (fstat against fstat) | 0.3 ± 0.0 | 0.3 ± 0.1 | (<1 ms) | 0.2 / 0.2 | -- | -- |
| wc | -c through a redirect, C (an fstat and a tell on both sides) | 0.4 ± 0.0 | 0.5 ± 0.1 | (<1 ms) | 0.3 / 0.3 | -- | -- |
| wc | -m, C (bytes, so an fstat) | 0.3 ± 0.0 | 0.3 ± 0.0 | (<1 ms) | 0.2 / 0.2 | -- | -- |
| wc | -m, UTF-8 (the decoder) | 3207.7 ± 11.0 | 3266.2 ± 13.5 | +1.8% | 2359.0 / 2352.6 | +2.1% | 0.72 |
| wc | -l, C | 435.5 ± 1.0 | 434.3 ± 1.1 | -0.3% | 74.0 / 73.7 | +0.1% | 0.17 |
| wc | -l, UTF-8 | 436.1 ± 3.8 | 434.7 ± 1.0 | -0.3% | 74.7 / 73.6 | +1.2% | 0.17 |
| wc | -w, C | 1863.7 ± 18.6 | 1949.0 ± 11.0 | +4.6% | 1866.6 / 1867.1 | +4.5% | 0.96 |
| wc | -w, UTF-8 | 3205.7 ± 8.5 | 3266.9 ± 10.4 | +1.9% | 2360.3 / 2352.9 | +2.2% | 0.72 |
| wc | -L, C | 3243.3 ± 41.2 | 3311.4 ± 12.4 | +2.1% | 1866.4 / 1866.1 | +2.1% | 0.56 |
| wc | -L, UTF-8 | 3211.3 ± 16.6 | 3273.3 ± 15.8 | +1.9% | 2351.9 / 2351.9 | +1.9% | 0.72 |
| wc | the default counts, C | 1858.3 ± 17.2 | 1946.2 ± 10.5 | +4.7% | 1865.3 / 1868.3 | +4.6% | 0.96 |
| wc | the default counts, UTF-8 | 3202.9 ± 8.1 | 3266.4 ± 6.2 | +2.0% | 2354.2 / 2354.8 | +2.0% | 0.72 |
| wc | the default counts on very short lines, C | 202.3 ± 1.1 | 205.8 ± 1.0 | +1.7% | 197.6 / 197.8 | +1.6% | 0.96 |
| wc | -l on very short lines, C | 125.1 ± 0.2 | 126.2 ± 0.3 | +0.9% | 5.5 / 5.8 | -4.3% | 0.05 |
| wc | the default counts on binary noise, C | 414.3 ± 7.2 | 423.1 ± 3.4 | +2.1% | 368.5 / 368.8 | +2.0% | 0.87 |
| wc | the default counts on binary noise, UTF-8 | 1976.0 ± 1.1 | 1986.4 ± 9.6 | +0.5% | 2018.5 / 2019.0 | +0.5% | 1.02 |
| wc | -L on binary noise, C | 1446.3 ± 10.8 | 1457.8 ± 6.6 | +0.8% | 368.5 / 368.6 | +0.8% | 0.25 |
| yes | 1 GiB of `y` into head -c | 180.6 ± 3.0 | 189.8 ± 6.0 | +5.1% | 111.2 / 107.9 | +8.3% ** | 0.57 |
| yes | 1 GiB of a 40-byte line into head -c | 207.7 ± 5.0 | 207.2 ± 4.8 | -0.2% | 113.2 / 113.6 | -0.6% | 0.55 |

## 4. Evidence index

Every path below is under kasumi `~/lanes/bu17/ev/` (kept; the build
trees are pruned), except the CI logs, which are on nomad-1 at
`~/lanes/bu17/ci-*.log`.

- **The archives:** `archives.log` `537d7b2b…`. It covers the six unix
  archives at 0.2.25 / 0.1.48 and the 0.2.23 linux one, every member
  hashed by name.

  | member | darwin-arm64 | linux-x64 | linux-arm64 |
  |---|---|---|---|
  | `wolf` | `833a4ad8…` | `8373b0cd…` | `1b1d5669…` |
  | `libwolf_rt.a` | `ac8d26e6…` | `6ac563e7…` | `4d074d98…` |
  | `libwolf_rt_none.a` (new) | `33df207b…` | `110f062a…` | `110f062a…` |
  | `wolf-cimport-worker` | `555a3c5d…` | `9c423c74…` | `40e40919…` |
  | `_wolf` | `a368c8ec…` | `a368c8ec…` | `a368c8ec…` |
  | `wolf.fish` | `180de0ec…` | `180de0ec…` | `180de0ec…` |
  | `lupin` | `4cb677f0…` | `734caee6…` | `823358ee…` |

  Identity: `wolf 0.2.25 (wolfgang, pin 6710f9e)` / `paired with lupin
  0.1.48 (reference interpreter), pin 294d626`; `lupin 0.1.48
  (wolf-interp, reference interpreter at pin 294d626)`. 0.2.23's linux
  `libwolf_rt.a` was `5af08d0e…`.
- **The prediction:** `f7d60b7`, pushed before `archives.sh` ran.
- **Gauntlets.** Each runs fetch, build on both tiers, `wolf test`, fmt,
  selftest and difftest, and every log is the full output:
  - base `2f15585` (0.2.23): `gauntlet-base-2f15585.log` `d13eff2b…`
  - pin `596f37f`: `gauntlet-pin-596f37f.log` `1af3792f…`
  - std try (`2f389a7` on `596f37f`): `gauntlet-stdtry-2f389a7.log`
    `76a2ba01…`
  - head `d84db8f`: `gauntlet-head-d84db8f.log` `36c6cb97…`
- **The dev tier's difftest:** `devdiff-base-2f15585.log` `8c428c26…`,
  `devdiff-pin-596f37f.log` `96cfa4c4…`, `devdiff-head-d84db8f.log`
  `27f32c4b…`.
- **Verdict lists:** `443e432e…` at base and pin, on both tiers;
  `6f8d7f2d…` at head, on both tiers.
- **Binaries:**
  - `bins-{release,dev}-{base-2f15585,pin-596f37f,head-d84db8f}.sha256`
  - stripped: `stripped/{base,pin}-{release,dev}.sha256`, `8bda47b6…`
    and `b5a1408d…` for release, `2c304866…` and `5917c553…` for dev
  - B151 on dev: `bins-dev-head-d84db8f-std6a0df5e.sha256` =
    `bins-dev-head-d84db8f.sha256`, `678189b6…` both
- **WIR:** `wir/{base,pin}/*.wir`, with the opcode moves in
  `wir-opcode-moves.txt` `7d671295…`. Own-code instruction counts:
  `own-{release,dev}-*.txt`.
- **Bench:**
  - `bench/*.md` (48 reports; concatenated `a4d032b2…`), `bench/host.txt`
    `36c60009…`, `bench-move-table.md` `479baa6c…`
  - the A/B: `ab-table.md` `4a45d802…` (`ab/rows.json` `15dc06bf…`) and
    `ab50-table.md` `173c8553…`
  - the regression's witness: `perf/witness-unexpand/`, every file listed
    in wolf-lang#624
- **CI:**
  - the planted red: run **37700540352** at `de8d3e2` (`version_line`
    names 0.2.23 over the 0.2.25 archives). All three legs are red by
    name: `toolchain: REFUSED — wolf identity: have "wolf 0.2.25
    (wolfgang, pin 6710f9e)", pin wants "wolf 0.2.23 (wolfgang, pin
    8edac3e)"` (ubuntu job 113062667859, macOS 113062667754, field
    113062667579; failed-log `d8198dcb…`). Reverted in `88a0bed`.
  - green at `88a0bed`: run **37701381298**, first attempt. ubuntu job
    113065375952: 2749 / 0 / 32 (log `9107311a…`, 32 SKIP lines).
    macOS 113065376225: 2709 / 0 / 72 (`e40ddf4f…`, 72 SKIP lines).
    Field 113065376255: 2692 / 15 / 74 (`f38c8d1e…`, 74 SKIP lines).
  - CI at head: in the PR.


## 5. Done-when

Branch `bu17`; PR boreutils#22 open, unmerged; CI green at head;
worktree and kasumi build trees removed, `ev/` kept. Close nothing.
Filed wolf-lang#624.
