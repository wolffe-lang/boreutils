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

## What it turned out to be, with the artifacts

**The macOS red is `tools/difftest` killing itself, and it is not a
macOS bug.** The harness set `SIGPIPE` to `SIG_DFL` for the whole
process. Every case with an inline standard input has its parent write
that input to a child that may already have exited — a usage error, a
bad option, an invalid style all exit before reading a byte — and a
write to a pipe whose only reader is gone is EPIPE. With `SIG_DFL` the
signal killed difftest where Python would otherwise have raised
`BrokenPipeError` and `communicate()` would have swallowed it. **It is a
scheduling race, decided per run**, which is why the same commit was
green on 09-18 and red on 09-21.

**Not the runner, not brew, not the oracle, and not the two docs
files.** The table above quotes image, OS build, bottle and oracle
identical across the two eras. The docs files are excluded by
construction: `bu06-probe-unfixed` (`40e1ac2`) carries a tree
**byte-identical to PR #1's head** — `git rev-parse` gives
`5b0255d5f221597665363ee6aeb3eb036e2befc1` for both — and with the
**unfixed** harness its macOS gauntlet **passed**, `difftest: 1259
passed, 0 failed, 29 skipped` (run 35673565877, job 106575197320).
The same unfixed harness on the trunk tree also passed on macOS
(run 35672284587, job 106571201793), same triple. The failure is
outside the repository's content.

**And it is not macOS-only; macOS is only where the evidence dies.** In
that same run 35673565877 the **linux** `field` leg took the identical
`Process completed with exit code 141` (job 106575197103) — and because
linux's pipe block is 4096 bytes it left a partial report ending
`ok   head: a write error on a live descriptor`, so the death is in the
next few dozen cases. That leg is `continue-on-error`, so this has been
an ANNOUNCED ADVISORY on linux rather than a red, which is why only
macOS reds were ever noticed.

**Reproduced off CI, deterministically.** On kasumi (16 cores) the
unfixed harness wins the race 5 of 5. Pinned to one core with
`taskset -c 0`, as a loaded runner effectively is, it exits **141 three
times out of three**, each inside `nl`, after
`nl: the section carries, and -f a shows it`,
`nl: a bad option alone is still an error` and
`nl: an invalid footer style` — the neighbourhood the linux field leg
died in, and where the macOS deaths sit too (9.4 s of a 19 s run). `nl`
is simply where the corpus concentrates cases whose child exits at once.
Every inline standard input in the corpus is 204 bytes or smaller, far
under any pipe buffer, so the write can only fail against a child that
is **already gone** — a race, never a size.

## The prediction, scored

**Right on the pick and on the number.** It is the harness's own defect
and a race, not a drift; and with the harness fixed the macOS gauntlet
over PR #1's tree reports **`difftest: 1259 passed, 0 failed, 29
skipped`**, the 09-18 triple exactly (run 35672665977, job
106572395096). None of the three falsifiers fired: no `FAIL` line, the
header still reads `GNU coreutils 9.11`, and the death is squarely on
the stdin-write path.

**Wrong on where.** The prediction named `tr` as the utility the partial
report would end in, reasoning from `tr`'s closed-descriptor cases being
the only ones carrying inline standard input on the two branches
`communicate()` does not cover. The real path is `communicate()` itself
— which handles EPIPE perfectly well and never got the chance, because
the signal killed the process first — and the real utility is `nl`.

## The gate this lane nearly shipped, and the audit that caught it

`tools/difftest-evidence`'s second check first asserted only that a
killed run had left *something*. Run against the harness with the flush
reverted, **it passed** — because block buffering is not "nothing until
exit", it is "nothing until the block fills", and on linux the block is
4096 bytes, so 57015 bytes of report reached the reader anyway. That is
wave 45's fourteenth shape: a test that models the bug instead of gating
it. The check now requires the first verdict to arrive in **under one
4096-byte block**, the smallest block any host in the matrix gives a
pipe, which no buffer can deliver and only a per-line write can. Each
half of the fix was then reverted separately against the corrected gate:
flush reverted → check 2 refuses; `SIG_DFL` and the unguarded write
restored → check 1 refuses at signal 13.

**The buffering asymmetry, measured.** Unfixed, the same 1288 verdict
lines reach ubuntu's log spread over 2.3 seconds in 35 distinct
hundredth-second buckets (job 106571201815) and macOS's inside a single
40 ms burst at exit (job 106571201793; the 09-18 green, job
105753052795, is the same shape). Python sizes stdout's buffer from the
pipe's `st_blksize`, measured here at 4096 on linux and 16384 on macOS.
So linux deaths leave most of a report and macOS deaths leave none —
the whole reason boreutils#10 reads as a macOS defect.
