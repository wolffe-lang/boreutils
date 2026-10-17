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

## 3a. The prediction, scored

§3 above is as it was committed (`87fa8e2`), before GNU's `kill` was run
by this lane on any number and before the first change. Scored in place,
by line. "kasumi" is a fresh `--network none` container a case of
`ubuntu:24.04` (killtest, podman, `--cpus 0-3` asserted inside) or of
`localhost/px12-ubuntu` (the gauntlet and killprobe, `probes/box.sh`);
"GNU" is bu25's build of 9.11 copied to `~/lanes/bu26/gnu/`
(`kill` `a78a3c72…`, `env` `2f5617c0…`). The CI runs are one-job
dispatches of the new `kill` job (`only: kill-macos` / `kill-ubuntu`).

| # | predicted | measured | verdict |
|---|---|---|---|
| 1 | the cause is each side's own pid, nothing in `kill` | right. Every red line of the five runs is `placing: {pid0} -l` with the two sides on different numbers; the retired case, counted in each dispatch (it never gates), is red in 13 / 30 (39075023384) and 10 / 30 (39077061677) on macOS and 5 / 30 on ubuntu (39077031801), and every one of those reds names two different signals or one signal and `invalid` — never ours wrong about one number (§#34) | right |
| 2 | one fixed number both sides share; outside a container one that names no process; a small one only in a container | right, and one thing not predicted. Four cases replace the one: `2147483647 -l` and `4294967305 -l` (both `kill: 'N': invalid signal`, status 1, on both hosts), `9 -l` and `265 -l` (`KILL`, container only). **Not predicted:** the first version kept a target "to be left alone", and on ubuntu GNU's target was pid 9 twice in twenty runs, so the reader wrote GNU's `'4294967305'` as `'{w:0}'` (2^32 + its pid) and ours, whose target was another pid, as the number (39075042695, 2 of 23 runs red). The cases now name no target (`8e2b506`), and killtest gained the rule that made the fix safe: a signal's number (`{n:…}`, `{x:…}`) where a process id stands is a literal number, refused outside a container (`4aab3d7`; `tests/kill/refuse-number.toml`, gated by the selftest) | right, one collision found and fixed |
| 3 | 0 red at the fix; the old case red on macOS in 2–5 of 10, rarely on ubuntu | at the fix: 0 of 23 killtest runs red in each of 39075023384 (macOS, `86d952f`), 39077061677 (macOS, `8e2b506`), 39077031801 (ubuntu, `8e2b506`) and in the earlier macOS run 39073021758 (`1dc2381`, 23 of 23 green before its retired step stopped at `bash -e`, fixed in `86d952f`); kasumi: killtest 338 / 0 / 0 (`ev/killtest-full-86d952f.log`), and there the old case was green 20 of 20 (`ev/killtest-old-x20.log`: podman hands both sides the same small pids). The old case: macOS 13 / 30 and 10 / 30 (4.3 and 3.3 in 10), ubuntu **5 / 30** (1.7 in 10, not "rarely": the docker pids differ by one or more often enough) | right on macOS, wrong on ubuntu's rate |
| 4 | #34 is #36's shadow: GNU and ours agree on every N 0..140,000 and a sample above | **right.** `tools/killprobe` on macos-latest (Darwin arm64; 39073021758, 39075023384, 39077061677, the same numbers each time): 240,578 numbers, `-l` and `-t`, both tiers: 237,775 alike and 2,803 by design (GNU names `EMT`, `IO`, `INFO` and their exit-status forms, which wolf has no meaning for), 0 parted. GNU names a signal for 30,176 of them. No line of `src/` changes | right |
| 5 | (if 4 were wrong) the fix in the exit-status reading | not reached | — |
| 6 | linux agrees for every N 0..140,000 | right: kasumi (`ev/killprobe-linux-trunk.log`) and ubuntu-latest (39075042695, 39077031801): 206,533 alike, 34,045 by design (`STKFLT`, `POLL`, `PWR`, `32`, `33`, the real-time names and their exit-status forms), 0 parted, on both tiers and both flags | right |
| 7 | the pin to 0.2.31 / 0.1.54 / std `d37c911` moves no verdict | **WRONG — the pin was not moved.** The archives are as the release API says (each hashed twice, kasumi `~/lanes/bu26/ev/archives.log`; `_wolf` `a368c8ec…` in all three), and on the release tier the difftest list is trunk's (`4644afb15f38b6d3`, 6,383 / 0 / 262). On the **dev tier five cases fail** (`ev/gauntlet-pin-0231.log`, list `0b39c06054e54b11`, 6,378 / 5 / 262): `cat` and `wc` with descriptor 1 closed (`>&-`) no longer see it closed. Cause, measured (`notes/bu26/probes/`): at 0.2.31 a dev-tier program that imports `std.signal` — every boreutils utility, through `bore` — makes the runtime's signal hub before `main` (s243), and the hub's pipes take the lowest free descriptors, so a closed 1 is a pipe by the time `main` runs (`fd 1: open … fs_fstat(1): ok`); the release tier and 0.2.30 do not (`probe-0230.log`), and the old std `fd6bcdc` under 0.2.31 does the same (`probe-0231-stdfd6.log`), so it is the compiler's runtime, not the std. The contract's rule "no regression in the existing 46 utilities' cases" decides it: **boreutils stays on 0.2.30 / 0.1.53 / `fd6bcdc`**, and the finding is for wolf-lang (§5) | wrong: the bump would regress five dev-tier cases |
| 8 | CI green at the head; killtest's count moves only by this lane's cases | the PR's run is named in the PR. killtest 335 → 338 (one case out, four in), 338 / 0 / 0 on ubuntu, 278 / 0 / 60 on macOS (two more container-only skips) | see the PR |
| seen red | the old case restored, red on macOS by dispatch | **red**: plant `c0c4322` on `bu26-plant-pid` (the old case back beside the four), run 39077060088 (macOS, one job): killtest 9 of 23 runs red, every red line `placing: {pid0} -l` (`dev stdout: 'TTOU\n', gnu ''`, `release stdout: 'USR1\n', gnu ''`, …), the job failed. The killtest rule (`4aab3d7`) seen red on kasumi: the old `tools/killtest` under the new selftest refuses nothing for `{n:HUP}` and the selftest says `REFUSED — tests/kill/refuse-number.toml was not refused (status 0)` (`ev/plantB-selftest.log`; in a container, where that case's `kill -s TERM 1` reached only the container's own first process) | red, both |

## 4. Evidence index

kasumi `~/lanes/bu26/` (prune list in §5):

- `ev/archives.log` — the six 0.2.31 / 0.1.54 archives, each hashed
  twice, sizes, `_wolf`, the version lines, `std/STD-REV` `d37c911`.
- `ev/gauntlet-trunk-1dc2381.log` — the gauntlet at 0.2.30 on this
  branch's `src/` (= trunk's; the tree was `87fa8e2` plus the killtest
  files as later committed): 6,383 / 0 / 262 both tiers, `4644afb1…`.
- `ev/gauntlet-pin-0231.log`, `difftest-dev-pin-0231.log` — the pin
  tried: release `4644afb1…`, dev 5 FAIL (§3a line 7).
- `ev/fd1/` and `notes/bu26/probes/probe-*.log` — the descriptor 1
  witness at 0.2.30, at 0.2.31, and at 0.2.31 with std `fd6bcdc`.
- `ev/killprobe-linux-trunk.log` — killprobe on linux, both tiers.
- `ev/killtest-placing-w1.log`, `killtest-record-placing.log`,
  `killtest-old-x20.log`, `killtest-full-86d952f.log` (338 / 0 / 0),
  `killtest-selftest-w1.log`, `plantB-selftest.log`.

CI (`kill` job, one a dispatch): 39073021758 (macOS `1dc2381`; probe
and 23 killtest runs green, the retired step stopped at `bash -e`),
39075023384 (macOS `86d952f`, green), 39075042695 (ubuntu `86d952f`,
red on the `{w:0}` collision), 39077031801 (ubuntu `8e2b506`, green),
39077061677 (macOS `8e2b506`, green), 39077060088 (macOS, the plant,
red). The PR's runs, and the repeated dispatches at the PR's head, are
listed in the PR.

## 5. Findings, and what was not verified

**For wolf-lang (not filed: a lane files nothing).** *0.2.31: on the dev
tier the signal hub is made before `main` in any program that imports
`std.signal`, and its descriptors take a closed 0, 1 or 2.* Witness
`notes/bu26/probes/fd1s.lu` (imports `std.signal`, calls
`signal.terminate()`, lists `/proc/self/fd/0..7` and `fs_fstat(1)`), run
with `>&-`: release tier `fd 1` not open, `fs_fstat(1): io`; dev tier
`fd 1`, 3, 4, 5 open pipes, `fs_fstat(1): ok`. 0.2.30 neither. Two
asks: the hub (and the readiness set) never land on 0–2 (a duplicate at
3 or more), and the dev tier decides "names `os_signal_wait`" by what is
reached, as release does. Until then boreutils cannot take 0.2.31: its
closed-standard-output rule (`bore.stdout()`, GNU's `standard output:
Bad file descriptor`) is wrong on the dev tier for every utility.

**For boreutils.**
- The `macos-suite` dispatch job (bu25) counts its red runs under the
  runner's `bash -e`, which stops at the first red, so "N of 10 runs
  red" can never print a number above 0 (the same bug this lane's `kill`
  job had, `86d952f`). One line, `set +e`.
- killtest's reader writes `{pidN}` and `{w:N}` over any matching digits
  in a case's output; a case about a fixed number now names no target,
  and CLAUDE.md says why, but the tool does not refuse a literal that
  could collide. Left as written.
- wolf-std `d37c911` has `std.os.users` (wolf-std#65 landed); boreutils'
  own `/etc/passwd` reader (`src/bore/ids.lu`) can move to it at the
  0.2.31-or-later pin.

**Issues.** #36: fixed here (the case, and killtest's rule). #34: no
fault — measured equal on both hosts over 240,578 numbers; it was #36's
two-pid comparison. Both close at merge, by hand.

**Not verified.** killprobe's sample above 140,000 is 100,000 numbers
(seed 34) and the edges, not all 2^31; linux aarch64; the retired case's
red rate on ubuntu beyond 30 runs; the pin bump on macOS (stopped on
linux's dev tier first); whether 0.2.31's release tier makes the hub
early in a program that REACHES a wait (boreutils has none).

**Housekeeping.** kasumi `~/lanes/bu26/` keeps `ev/` (cited), `gnu/`
(bu25's build, 33 M), `bin/trunk/` (static `kill`, both tiers, 28 M) and
`probes/`; the archives, the `fd6bcdc` std clone, every `target/` and the
probe binaries were removed, and the lane's clone (`boreutils/`, 365 M
with its staged toolchain) is removed at hand-back. Branch
`bu26-plant-pid` is kept on origin: §3a cites it.
