# bu26 — the kill cases

Lane note. **Class:** long (boreutils), **Opus**. **Crawl:** 54.
Branch `bu26` off boreutils `8f0bbb1` (bu25). Contract:
`sprints/boreutils/20-the-kill-cases/bu26-the-kill-cases.md` (planning
`37decac`). §1–§3 are committed before this lane has run GNU's `kill`
on any number and before any line of `src/`, `tools/`, `tests/` or CI
changes; §3 is scored in place later, never rewritten.

Two `kill` issues. **boreutils#36**: killtest's case `placing: {pid0}
-l` asks `kill -l` about each side's OWN target pid, so GNU and ours
answer about different numbers. **boreutils#34**: on macOS `kill -l N`
was seen to name a signal for some N past 255 where GNU said invalid.

## 1. Forbidden

bu25's contract's "Forbidden / rules", word for word, except as bu26
changes it: trunk `8f0bbb1` or later; wolf 0.2.31 / lupin 0.1.54 once
their archives exist; signals only to processes the test started.

- **No implementation's source is read**: not GNU coreutils', not
  procps', not util-linux's, not any shell's `kill`. GNU's behaviour
  comes from `kill --help`, the info manual and black-box runs of
  coreutils 9.11's OWN `kill`, built from the oracle tarball by digest
  with `--enable-install-program=kill`.
- **Signals only to processes the test started.** A `-l`/`-t` probe
  sends nothing; every sending case is killtest's, in a fresh
  `--network none` container on linux and on the throwaway CI runner on
  macOS, every target the case's own child. A process is ended by its
  recorded pid only, never by name, pattern or group.
- No `rm` outside `~/lanes/bu26/` (kasumi) and this worktree; no `git
  add -A`; nothing under `~/.claude`; no merge, tag, or issue filed or
  closed; no attribution trailer; the branch asserted before every
  commit. No build on nomad-1. kasumi's login shell is fish (`bash
  -c`); `setsid` with a pid file. `/home` on kasumi is 98% full (28 G
  free): prune as I go.
- Strict evidence (wolf-lang#571): `wolf build` exit 2 is a compile
  error; SKIP lines counted over the full output; no "seen red" without
  a run id. CI dispatches name one job; no other lane's run is
  cancelled. Waits inline, printing at least every five minutes.

## 2. Inputs, verified (2026-10-17)

| input | origin says | verdict |
|---|---|---|
| boreutils trunk `8f0bbb1` | `origin/trunk` `8f0bbb1` (bu25); 0 open PRs; open issues #34, #36, #37; `tests/kill/cases.toml` 335 cases, `tests/cases/kill.toml` 868 | holds. **Trunk's own push run 39046841635 at `8f0bbb1` is red** on macOS, killtest 276 / 1 / 58, the one case #36 names (`release stdout: '', gnu 'TRAP\n'`; ours `'{pid0}': invalid signal`) |
| #36's runs | 39039975911 attempts 1–3 (macOS: `release exit 0, gnu 1`; `release exit 1, gnu 0`; `dev exit 0, gnu 1`), 39032969326 attempt 1 (ubuntu, in a container: `release stdout: 'KILL\n', gnu 'FPE\n'`, i.e. our target was pid 9 and GNU's pid 8) | the shape #36 states: each side's own pid, in both directions |
| #34's witness | bu24's run 38751387617 attempt 1: the same case, the same two-pid comparison | **#34 was inferred from #36's case**, so it may be #36's shadow; only a one-number measurement can say |
| the toolchain | `v0.2.31` → `f4faf59d` (release published 2026-10-17 21:33Z, archives for linux x86-64, linux arm64, macOS arm64); `v0.1.54` → `0e536e8` (16:48Z, the same three); 0.2.31's bundled std is wolf-std `d37c911` (its release notes) | the archives exist, so the pin moves (contract) |
| the oracle | gnu-oracle.toml: 9.11, `394024ed…`, `--enable-install-program=kill`; bu25's linux build at kasumi `~/lanes/bu25/gnu/` | holds |
| the rule as implemented | `src/bore/signals.lu`: a number past the host's last signal is an exit status: `v > 255` → `v & 255`, else `v & 127`, and the result must be a signal of the table; "measured for every number from 0 to 700"; bu24 says linux agrees with GNU 0 … 140,000 | holds on linux; unmeasured on macOS past difftest's sample (0–69, 120–199, 250–329 and a dozen more) |

## 3. Prediction

**boreutils#36.**

1. The cause is the one #36 names and nothing else: each side runs its
   own script and so its own target, and `kill PID -l` (options
   permute) is `kill -l PID`, an answer about that number. Nothing in
   `kill` is at fault in any of the five red runs.
2. The fix keeps what the case is for (an option after an operand is
   still read, so the operand becomes a SIGNAL and no target is sent
   anything) and hands both sides one number: a fixed operand. Outside
   a container the operand must be one no process can have (killtest's
   own rule: 2147483647 or more), so if a `kill` ever stopped permuting
   it would signal nothing; a small, valid signal number (`9 -l`, which
   names `KILL`) runs only as `container = true`. Both answers are
   GNU's, measured, on both hosts.
3. Repeated one-job dispatches at the fix: 0 red of the new cases in
   every run on both hosts. The old case, run in the same dispatches,
   reddens some of them: on macOS in 2 to 5 of 10 (pids past 255, a
   signal named for about 1 low byte in 8), on ubuntu rarely (container
   pids are small and close, so the two sides' pids differ by 0 or 1
   and the answers agree unless one is a signal and the next is not).

**boreutils#34.**

4. Measured on CI's macOS runner, with one number handed to both sides
   in one process each (`kill -l N1 N2 …`, nothing sent): GNU's `kill
   -l N` and ours agree for every N from 0 to 140,000 and on a sample of
   the C `int` range above it, edges included (2147483647, 2147483648).
   **#34 is #36's shadow**: the "N past 255" it saw was two different
   N. Then no line of `src/` changes, and the measurement stays as a
   probe a dispatch can run on either host.
5. If 4 is wrong (some N parts), the parting is in the exit-status
   reading with macOS's numbering (its last signal is 31, linux's 64),
   and `entry_for_number` changes to GNU's measured rule on macOS only,
   linux's answers unmoved; the probe and new difftest cases at the
   parted numbers are the gate.
6. On linux the same probe agrees for every N 0 … 140,000 (bu24's
   result, re-run here against the pinned 0.2.31 build).

**The pin, 0.2.31 / 0.1.54, std `d37c911`.**

7. No verdict moves: the difftest list on both tiers in a kasumi
   container is trunk's at `8f0bbb1` (bu25's `4644afb1…` plus bu25's
   own cases), killtest 335 / 0 / 0, inouttest and idtest unchanged. No
   W0304 from 0.2.31's new prelude names (`src/` declares none of
   them). The shift rule changes nothing here: s237's census found one
   plain shift in boreutils and no new trap.
8. CI green on both hosts at the head, with killtest's case count
   changed only by the cases this lane adds and removes.

**Seen red.** A plant restores the pid-per-side comparison (the old
case) and a dispatch shows it red on macOS; and, if 5 holds, a plant of
the old number rule shows the probe red on macOS.
