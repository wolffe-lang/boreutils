# bu15 — the seek (boreutils#19) and the pin at 0.2.22

Lane note and contract. **Class:** medium (boreutils), **Opus**. **Wave:**
53. Contract: planning `wolffe-lang/wolf`
`sprints/boreutils/09-the-seek/bu15-the-seek.md` at planning trunk
`b25d8a8`. Branch `bu15` off boreutils `010f3144`. §1–§3 were committed
as `a5e617d` before the first change; this file restates them with the
evidence.

## 1. Forbidden

No `rm` outside `~/lanes/bu15/` and this lane's worktree; no
`git add -A`; nothing under `~/.claude`; no build on nomad-1 (every
build, difftest and bench ran on kasumi); no merge, tag or attribution
trailer; no "seen red" without a run id, sha, path or digest; the pin
from the release archives by digest only; GNU coreutils source never
read (GNU's behaviour here is the 9.11 oracle binary, run and
`strace`d).

## 2. Inputs, verified (2026-10-04)

| the contract says | origin says | verdict |
|---|---|---|
| boreutils trunk `010f3144` | `010f3144`, bu14's evidence commit | holds |
| wolf 0.2.22 = `8e36bc1a`, release 402696856, linux x86-64 `df0f2fea…`, aarch64 `64e35e43…`, macOS `19606e1e…`, windows `a302e134…` | tag object `173a3ef9` → `8e36bc1a`; the release API's digests are those four | holds |
| lupin 0.1.45 = `9f4e4a17`, release 402670966, `907cfb1a…`, `d4bf3432…`, `08b1de12…`, windows zip `9b5e5836…` | tag object `25c7932d` → `9f4e4a17`; digests match | holds |
| s199's bench log `7a38e4fc…` | kasumi `~/lanes/s199/evidence/tail-variant-bench.log` sha256 `7a38e4fc…` | holds |
| the calls are wolf-std 0.2.22's | they are compiler BUILTINS (`spec/11-os.md` at v0.2.22); wolf-std `6a0df5e` wraps them in `std/fs/fs.lu` | drift, harmless |
| ruling #34 (s208) moves `bore.put`/`put_byte`/`sink_push` at this pin | wolf-lang#559 is OPEN; 0.2.22's CHANGELOG names no #34 | **drift**: not in this pin |

Found before any change, both measured on kasumi against the oracle:

- **The stdin offset (linux).** `-` is reached by reopening `/dev/stdin`,
  which on linux is `/proc/self/fd/0`: a FRESH open file description at
  offset 0. A standard input the shell had read into was read from byte
  0, and descriptor 0's offset never moved. 108 of 216 probe rows
  differed from GNU (`ev/gnu-stdin-offset.log` `14831f89…` against
  `ev/bore-trunk-stdin-offset.log` `9c106d01…`). macOS's `/dev/stdin`
  duplicates descriptor 0 and shares its offset, so this was linux's.
- **A size that lies.** `/sys/kernel/mm/transparent_hugepage/enabled`
  reports 4096 and holds 23 bytes; `/proc/version` reports 0 and holds
  144. Trunk `wc -c` said 4096 and 0 (GNU 23 and 144); `tail -c 20`
  wrote 0 bytes of the first and all 144 of the second (GNU 20 and 20);
  `head -c -5` wrote 23 (GNU 18).

## 3. Prediction, scored

| predicted | measured | verdict |
|---|---|---|
| all 27 build at 0.2.22, nothing refused or warned | 27 × `rc=0 errors=0 warnings=0 ice=0` at std `14f0ab2` and at `6a0df5e` (`ev/stdtry.log` `38740588…`) | right |
| std moves to `6a0df5e` | both build; `14f0ab2..6a0df5e` is 21 commits touching only `std/fs/fs.lu`, which nothing imports; moved | right |
| verdict list at the pin byte-identical to `8d354b9b…` | `verdicts-pin-df842f7.txt` `8d354b9b…`, 2642 / 0 / 32 | right |
| kw03's trapping casts hit no site | none did (every variable cast is of an in-range value; `echo`/`printf` octal is `% 256`) | right |
| `tail -n 10` FILE ~0.4 ms | 0.312 ms (GNU 0.207), hyperfine 50 | right, better |
| `tail -c 10` FILE ~0.4 ms | 0.298 ms (GNU 0.207) | right, better |
| `tail -n 100000` short lines ~3 ms | 1.55 ms (GNU 0.69) | right, better |
| `head -n -1` FILE ~35 ms | 37.3 ms (GNU 29.4) | right |
| `head -c -1024 < FILE` ~35 ms | 37.6 ms (GNU 30.3) | right |
| `wc -c < FILE` ~0.5 ms | 0.433 ms (GNU 0.389) | right |
| every pipe row unchanged | `tail` A/B equal; **`head -n -1` through a pipe was 8% slower** until the window stopped threading a `mut sent: int` (`ev/bench2/ab.log` `d88e6dd8…`, fixed in `9f8fd48`, A/B `ab3.log` `bdce887c…`: 303.4 against 303.3 ms) | wrong, then fixed |
| `-c +K` reads forward from a seek in `from_end` | GNU `lseek`s past K − 1 even on a 100-byte file and reads to EOF, and leaves the offset at offset + K − 1 on an empty one; `tail -c +K` now does that for anything with an offset | wrong in shape, found by the offset probe |

The paths, as shipped (the README's table):

| | a regular file | stdin that is a regular file | a pipe |
|---|---|---|---|
| `tail -n K` | walk back 8 KiB blocks from the verified end (`bore.line_cut`), positional copy | the same from descriptor 0's offset; offset left at the end | forward, window |
| `tail -c K` | positional copy of `[end - K, end)` | the same from the offset | forward, window |
| `tail -c +K` | seek past K − 1, copy | the same | read and discard |
| `tail -n +K` | forward | forward from the offset | forward |
| `head -n -K` / `-c -K` | copy the first `cut` / `end - K` bytes | the same from the offset; offset left past the output | window |
| `head -n K` / `-c K` | forward, stop | forward; offset put back past the output | forward, stop |
| `wc -c` | size | size − offset; offset left at the end | read |
| any | a size that cannot be verified (0, or more than the file holds): the pipe's path | | |

## 4. Evidence index

Every path is under kasumi `~/lanes/bu15/ev/`.

- Base at 0.2.20 (`010f3144`): `gauntlet-base-0.2.20.log`, verdict list
  `8d354b9b…`, 2642 passed / 0 failed / 32 skipped.
- The archives and members: `archives.log` `72f2d259…`; `_wolf` hashes
  `2d1e4801…` in all three wolf archives. Members:

  | member | darwin-arm64 | linux-x64 | linux-arm64 |
  |---|---|---|---|
  | `wolf` | `ae08b6aa…` | `56f90a92…` | `267c3bb7…` |
  | `libwolf_rt.a` | `7e68da45…` | `dbf8ccb5…` | `cf042ddb…` |
  | `wolf-cimport-worker` | `a3596280…` | `2437fe56…` | `a6774e91…` |
  | `_wolf` | `2d1e4801…` | `2d1e4801…` | `2d1e4801…` |
  | `lupin` | `cfeb45f1…` | `6b88de73…` | `b236f67b…` |

  Identity: `wolf 0.2.22 (wolfgang, pin 8e36bc1)` / `paired with lupin
  0.1.45 (reference interpreter), pin dfcc2f1`; `lupin 0.1.45
  (wolf-interp, reference interpreter at pin dfcc2f1)`.
- The pin (`df842f7`): `gauntlet-pin-df842f7.log`, verdict list
  `8d354b9b…`, identical to the base.
- Head (`9f8fd48`): `gauntlet-head-9f8fd48.log`, 2749 passed / 0 failed
  / 32 skipped, verdict list `f39559c9…`. Against the pin: no verdict
  changed; 107 cases added, all `ok` (tail 53, head 38, wc 13, cat 3).
- The new cases against trunk's binaries: 47 of them FAIL there
  (`trunkbin-difftest-a.log` `4207bccd…`), every one an offset or a
  lying size.
- The offset probe (216 rows, 18 commands × 3 files × 4 offsets) at head
  is byte-identical to GNU's: `bore-dev2-stdin-offset.log` and
  `gnu-stdin-offset.log` both `14831f89…`.
- **The plant**: `a4ff47a` makes `bore.line_cut` skip the first byte of
  every block (`while k > 0`), an off-by-one at the seek boundary.
  Local: 16 FAIL (`plant-local.log` `559d6e44…`). **CI run
  37170858202, ubuntu job 111343353469: `difftest: 2731 passed, 16
  failed, 32 skipped`**, the same 16 by name, e.g. `FAIL tail: seek: n
  312 across the block boundary` (`ci-37170858202-ubuntu.log`
  `32eb15bd…`). Reverted in `7d3bd81`. The run's macOS leg was
  cancelled by this lane once the ubuntu red was in hand.
- The selftest gate on the new `offset` field: its first plant (`head
  -c 0` against GNU `cat`) PASSED, because GNU `cat` refused `-c` and
  never read — and this lane's own dev script piped the selftest through
  `tail`, so the red was invisible there (the gauntlet script, which
  does not pipe, would have shown it). Replanted as `head -` against
  `cat -`; it fails by name.
- Benchmarks: `bench/` (tail, head, wc; head and trunk; 20 runs; load
  5.3–9.3: `bench/host.txt`), `bench2/` (tail and head three ways —
  trunk at 0.2.20, the pin without the seek, head — 20 runs, load
  5.3–8.2; `seek-rows.json` `6198428e…` and `seek-stdin.json`
  `d4572336…`, hyperfine 50 runs), `bench3/` (head at `9f8fd48`, 20
  runs, load 4.2–5.7), `bench2/strace-summary.txt` `a9848e88…`.
  kasumi has clang 23.1.1 since the 2026-10-02 upgrade, for both the
  "before" (rebuilt here) and "after" binaries.

## 5. Done-when

Branch `bu15`; PR #20 open, unmerged; CI green at head; worktree and
kasumi trees removed. To close (by the orchestrator, not this lane):
boreutils#19.

## Findings for upstream

- A `mut sent: int` parameter threaded through `head`'s window loop
  cost ~8% (299 against 327 ms, 256 MiB through a pipe) though it is
  touched once per 256 KiB chunk; a local plus one write at the end
  costs nothing. Reported to the orchestrator as a wolf-lang
  performance candidate, not filed by this lane.
