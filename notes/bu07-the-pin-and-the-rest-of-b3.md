# bu07 — the pin at 0.2.16, and the rest of B3

Lane note. Written 2026-09-24, before a line of `wolf-toolchain.toml`,
`gnu-oracle.toml` or `src/` moved.

## 2. Inputs, re-derived against origin (2026-09-24)

Every row was re-derived from the thing itself — origin, the GitHub
release API, the release archive, the case files — not copied from the
contract.

| the contract says | origin says | verdict |
|---|---|---|
| boreutils trunk `b8258ab` | `b8258abd9709277df8a5842821ef7f0ae2576d95`, `README: point the licence section at LICENSE-TRAINING-DATA` | holds |
| pins wolf **0.2.14** / lupin **0.1.36** | `wolf-toolchain.toml` `[wolf] version = "0.2.14"`, `[lupin] version = "0.1.36"` | holds |
| fifteen utilities landed | `src/*.lu` minus `bore/` and `bore_test.lu`: basename cat cut dirname echo false head nl seq tail tr true uniq wc yes — fifteen | holds |
| 1,288 differential cases | `grep -c '^\[\[case\]\]' tests/cases/*.toml` sums to **1,288** | holds |
| wolf **0.2.16** = tag `v0.2.16` = `93a5fe50` | annotated tag `014dc68c` dereferences to commit `93a5fe504593ca7642b78ba83b4986e7a03cfe71`; `wolf --version` line 1 from the archive is `wolf 0.2.16 (wolfgang, pin 93a5fe5)` | holds |
| release 395302343, four assets | `gh api repos/wolffe-lang/wolf-lang/releases/tags/v0.2.16` → `id 395302343`, draft false, assets darwin-arm64 / linux-arm64 / linux-x64 / windows-x64 | holds |
| darwin-arm64 `b0431056…`, linux-arm64 `fe1966a4…`, linux-x64 `84e30c05…` | downloaded and hashed: `b04310568d…`, `fe1966a42a…`, `84e30c05e5…` | holds |
| lupin **0.1.38** = `ba357aa`, release 393623352, five assets | annotated tag `a9f07425` → commit `ba357aa6a2e32040d4f089d2cefe05bab86c4f86`; `id 393623352`, draft false, five assets | holds |
| lupin pinned on the released line, `2e4ca769` an ancestor of v0.2.15 | `lupin --version` line 1 from the archive is `lupin 0.1.38 (wolf-interp, reference interpreter at pin 2e4ca76)` | holds |
| boreutils#10 CLOSED | closed | holds |
| B98 open; the `field` leg's `continue-on-error` hides a signal death | `.github/workflows/ci.yml` `field:` carries `continue-on-error: true`; BACKLOG B98 open | holds |
| B73 open; two 9.11 builds disagree on `tail +3` | `tests/cases/tail.toml:298` is the skipped case, `gnu-oracle.toml` `[oracle] version = "9.11"` and nothing else identifies a build | holds |

### Drift found, reported not absorbed

1. **`README.md` says "1,272 differential cases, 0 failing, 16
   skipped".** The tree holds **1,288 cases**; a run on kasumi at
   trunk and the old pin answers `1271 passed, 0 failed, 17 skipped`.
   Two things are wrong in one sentence: the headline calls the
   *passing* count the *case* count, so the sixteen (now seventeen)
   skips are subtracted from the corpus rather than named inside it,
   and the skip count is one release of the corpus stale. Both are
   the shape wave 46's §4 forbids — a figure with no artifact behind
   it. Corrected in this branch from a run, not from arithmetic, and
   the sentence is rewritten to state the corpus and the run
   separately so the next reader cannot repeat it.

2. **The contract's §2 does not mention `[std]`, and the pin has a
   third section.** `wolf-toolchain.toml` pins `wolf-std` by commit
   (`2d1021996da6cde7b14c41ee4ef9d10125182e13`, the same rev lobo
   pinned at ws35). wolf-std's trunk is 69 commits past it at
   `070884c`. **This lane does not move it**, and the reason is the
   contract's own shape: the deliverable is "the pin, BOTH halves",
   the two halves are the two release archives, and a bump that moves
   the compiler two releases and the standard library sixty-nine
   commits in one commit cannot say which half a red belongs to. The
   std rev is re-verified green against 0.2.16 rather than advanced.

3. **`gnu-oracle.toml`'s field table is stale in one cell.** It records
   "ubuntu-latest 9.4" as of 2026-09-18. That is still what the field
   leg reports (run ids in the report), so the cell holds — but the
   file dates it and nothing re-checks the date, which is the same
   drift shape B44 exists to prevent one level up. Item 2 below puts
   a machine-checked identity in its place.

## 3. Prediction, committed before the measurement

Written before the pin moved, before a differential case for the four
new utilities existed, and before `tools/bench` was run on any of them.

### 3a. Which existing cases move at 0.2.16

**Zero. Not one of the 1,288 existing cases changes its verdict, and
the exit-status change is the interesting half of the reason.**

`[conf.exit]` at s169 makes the *compiler* exit 2 for a rejected
program and 4 for a refusal, where it used to exit 1. That moves a
`run(exit=1)` fence in a conformance corpus. It cannot move a
boreutils case, because **no boreutils differential case ever runs the
compiler**: `tools/difftest` execs `target/release/<util>`, a native
binary built ahead of time by `tools/build`, and compares its status
against GNU's. The compiler's own exit status is observed exactly
once in this repository — by `tools/build`, through `set -eu`, where
any non-zero status fails the build identically. So the change is
invisible to the corpus by construction, and 2 rather than 1 from a
failed `tools/build` is the same red.

The other four movers are read the same way and none of them reaches a
case either: `move` on a `Copy` place recording the move (s177/#444) is
a *fix* for a silent wrong answer, and boreutils has exactly one
`move`-shaped site — it has none; `Scope`/`Proc[T]`, pools and
`handle T` (s170/s173) are surfaces no utility uses; the place model
(s168) is a spec clarification; `[type.list.lit.elem]` saying
`List[i32]` (s175) is about list *literals*, which this repository does
not use at all (lupin 0.1.36 refused them, so every list here is
`List[T]()` and pushes).

**The falsifier is one line.** If the difference between the before and
after `difftest` totals is anything but `0 passed / 0 failed / 0
skipped` at identical corpus content, the prediction is wrong, and the
report names every case that moved.

A second, weaker prediction: **`wolf fmt --check` and `--deny-warnings`
are where a two-release bump actually bites**, not the corpus. If
anything reds at the bump it is a new lint or a formatter change over
`src/`, and it will be visible before a single case runs.

### 3b. Per utility: case count and speed against GNU

Case counts are what this lane intends to write, each falsified by the
committed file.

| utility | predicted cases | predicted vs GNU, and why |
|---|---:|---|
| `tac` | 90–110 | **0.3x–0.6x** on a file. GNU seeks to the end and walks backwards; wolf 0.2.14 has no seek (wolf-lang#426), so `tac` reads the whole stream forward into memory and writes it back. That is the same wall `tail` hit, and `tac` cannot even use a bounded window: it owes the *whole* input reversed, so peak memory is the input, and this is the one utility in the set whose memory is NOT flat. Through a pipe GNU buffers the whole input too, and there I predict **0.6x–0.9x**. |
| `paste` | 80–100 | **0.5x–0.8x** serial (`-s`), **0.3x–0.6x** parallel. The parallel form reads N files a line at a time, which is N open streams and a line-assembly per output record; the per-byte work is a copy. |
| `fold` | 70–90 | **0.5x–0.9x** for `-b` (byte counting, a pure scan) and **0.25x–0.5x** for the default column mode, which has to interpret tab, backspace and carriage return per byte. `-s` (break at a space) adds a backwards scan per line and should be the worst row. |
| `expand` | 60–80 | **0.4x–0.7x**. Per-byte column arithmetic and a run of spaces written out; a tab-heavy input is the best case because one input byte becomes many output bytes and the loop amortizes. |
| `unexpand` | 60–80 | **0.3x–0.6x**, worse than `expand`, because it must buffer a run of blanks before deciding whether the run becomes a tab, and that decision is per blank rather than per tab. |

**Aggregate falsifier:** the four utilities together add **360–460**
cases. Fewer than 360 means the corpus is thinner than the transform
set's standard (`tr` alone has 146); more than 460 is not a failure but
is worth saying.

**Speed falsifier:** a measured ratio outside the band above is a wrong
prediction and is published as one. On the evidence of bu03 and bu04 —
where three of four `tr`/`seq`/`nl` predictions missed, and `seq`
missed in *both* directions — I expect at least one of these five bands
to be wrong. The one I am least sure of is `tac`: if GNU's pipe path
buffers to a temporary file rather than to memory, the pipe row could
go either way by an order of magnitude.

### 3c. B73 and B98, predicted

- **B73.** I expect to find that `gnu-oracle.toml` **can** carry a build
  identity for the *staged* oracle (the tarball is pinned by digest
  already, so a build from it is reproducible up to the toolchain that
  built it) and **cannot** carry one for a *host* oracle, which is
  where the disagreement actually lives: Homebrew's 9.11 and Arch's
  9.11 are two third-party builds of one tarball and neither publishes
  an identity boreutils could pin in advance. The prediction is
  therefore that the honest answer is **half a mechanism and half a
  stated reason**, not one or the other.
- **B98.** I expect a planted signal death on the `field` leg to be
  **invisible today**: `continue-on-error: true` turns the step's
  failure into an annotation and the job's conclusion into `success`,
  whatever the exit code was. The ruling is that a *signal* death is
  loud and a *verdict* difference is not, and the falsifier is that
  after the change the planted signal reds the leg while a planted
  verdict divergence still does not.
