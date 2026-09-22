# bu06 — the flush, and the macOS red

Lane note. Written 2026-09-22, before a line of `tools/difftest` moved.

## Inputs, re-derived against origin (2026-09-22)

| the contract says | origin says | verdict |
|---|---|---|
| trunk `24e786d` | `24e786d96f8ae17d1a5b0e0b3505f88c0829a525` | holds |
| PR #1 `wl34-license`, docs only | head `380c9bb4b5ac44ae9a885c8580b76e586fd4cacc`, OPEN, merge-base `24e786d`, diff `LICENSE-TRAINING-DATA` +30 / `README.md` +3 −1, no code | holds |
| run 35668278241 red on `gauntlet (macos-latest, g)`, exit 141, no other output, attempts 1 and 2 | attempt 1 job 106558768066 (23:45:32Z–23:46:18Z), attempt 2 job 106566644290 (00:12:25Z–00:13:12Z); both end `##[error]Process completed with exit code 141.` with nothing between `Run tools/difftest` and the error | holds |
| ubuntu and the field leg pass | jobs 106566644884 and 106566643000, both success | holds |
| trunk green on the identical job at `24e786d` on 2026-09-18 | run 35392257581, job 105753052795, success; `difftest: 1259 passed, 0 failed, 29 skipped` | holds |
| boreutils#10 open | open | holds |

## Drift found: the contract's §2 *reason* is wrong, and the logs say so

The contract reasons that "something **outside the repo** moved between
09-18 and 09-21 on the macOS runner (image, brew, the oracle fetch)".
Quoted side by side, **nothing outside the repo moved**:

| | green 105753052795 (09-18) | red 106566644290 (09-22) |
|---|---|---|
| runner | `Current runner version: '2.337.0'` | `Current runner version: '2.337.0'` |
| provisioner | `Version: 20260828.587` | `Version: 20260828.587` |
| OS | `macOS` / `26.6.2` / `25G83` | `macOS` / `26.6.2` / `25G83` |
| image | `Image: macos-26-arm64` / `Version: 20260907.0351.1` | `Image: macos-26-arm64` / `Version: 20260907.0351.1` |
| brew | `Pouring coreutils--9.11.arm64_tahoe.bottle.1.tar.gz` / `443 files, 12.6MB` | `Pouring coreutils--9.11.arm64_tahoe.bottle.1.tar.gz` / `443 files, 12.6MB` |
| oracle cache key | `gnu-oracle-macOS-ARM64-5f6a5939e15d615b48ae5757cd122d9d043fe80744e2772ea65e62515c99fefc` (miss) | the same key (miss) |
| oracle fetch | `fetch-oracle: the host already ships the oracle of record (GNU coreutils 9.11)` | the same line |
| region | `Azure Region: westus` | `Azure Region: westus` |

Same image, same OS build, same bottle revision, same oracle. The
difference between the two eras is **two documentation files and the
wall clock**, which is why the red has to be explained from inside the
harness rather than from the runner.

## Prediction, committed before the work

**One pick: it is the harness's own defect, and it is a RACE rather than
a drift.** `tools/difftest` sets `SIGPIPE` to `SIG_DFL` in the **parent**
(line 367) and then writes a case's `stdin` to the child on two paths
that `subprocess.communicate()` does not cover — the `stdout_closed`
branch and the `stdout_bytes` branch. A child started with descriptor 1
closed exits at its first write, before it reads a byte of stdin; the
parent's `proc.stdin.write(data)` then lands on a pipe with no reader,
takes SIGPIPE at `SIG_DFL`, and dies at 141 with its block-buffered
report unwritten. Whether the parent wins that write is a race with the
child's exit, so two greens on 09-18 and two reds on 09-21 are the same
code meeting the same machine and losing twice.

**Falsifiers, each sufficient on its own.**
1. The flushed macOS run prints a `FAIL` line whose `bore` and `gnu`
   sides genuinely differ — then it is a real divergence, not the
   harness.
2. Its header names a GNU that is not `9.11` — then the oracle drifted
   after all.
3. The partial report's last line sits somewhere the stdin-write path
   cannot reach — then the diagnosis above is wrong about *where*.

**The number.** With the harness fixed, the macOS gauntlet over PR #1's
tree reports **`difftest: 1259 passed, 0 failed, 29 skipped`** — byte for
byte the 09-18 green's count. Any other triple falsifies the prediction.
And the partial report the *planted* red leaves will end inside `tr`,
the first utility in sorted order whose closed-descriptor cases carry
inline `stdin`.
