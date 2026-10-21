# bu29 — the pin at 0.2.34 (boreutils on wolf 0.2.34 / lupin 0.1.55 / wolf-std `e036bec`)

Lane note. **Class:** short (boreutils), **Opus**. **Crawl:** 54, the 0.2.34
downstream round. Branch `bu29` off boreutils `cc64f68` (bu28). Contract:
`sprints/boreutils/23-the-pin-0234/bu29-the-pin-0234.md` (planning
`f9b9d00`). §1–§3 are committed before the pin moves and before anything is
measured at the new pin (r39's measurement is read, not re-run); §3 is scored
in place later (§3a), never rewritten.

One deliverable: boreutils pinned to wolf 0.2.34 / lupin 0.1.55 with the
bundled std `e036bec` (its own commit); difftest and the suites green on both
tiers, the counts against r39's measurement of this same trunk on the
published 0.2.34; the field leg's advisory as it stands. No program changes.
boreutils#44 (`timeout` calling `os_core_off()` before it re-raises) waits on
0.2.35, whose `os_core_off()` (s253, wolf-lang#847) it needs; nothing here
touches it.

## 1. Forbidden

- **No implementation's source is read**: never GNU coreutils' (the licence
  grant; boreutils' rule 1), nor any other utility's, libc's, shell's or
  kernel's. GNU 9.11 is bu25's build of the oracle tarball by digest, run as
  binaries only (copied from kasumi `~/lanes/bu28/gnu/`, its `timeout` and
  `kill` digests checked against bu28's note).
- **No line of `src/`, `tests/`, `tools/`, `ci/` or `.github/` changes.** The
  pin's commit changes `wolf-toolchain.toml` alone. If the pin moves a verdict
  away from GNU, the lane stops and reports (bu26's rule); it does not fix.
- Signals, group sends and faults only inside the suites' own throwaway
  `--network none` containers; every container this lane makes runs
  `--ulimit core=0:0`; kasumi's host core store is counted before and after.
- Toolchains from the release archives by digest, each read twice. No build
  on nomad-1. kasumi: `bash -c`, `setsid -f` with a pid file for long jobs,
  killed by recorded pid only; one tree, pruned at the end; host ports 8080
  and 8088 never used; no package installed.
- Strict evidence (wolf-lang#571): `wolf build` exit 2 is a compile error;
  SKIP lines counted over the full output; `wolf test` at 0.2.34 has no
  `--nocapture`, so the unit tests' stdout is counted where they print;
  the kill and timeout suites under `--cpus 0-3` (asserted inside the
  container). No "seen red" without a run id. A plant runs the smallest run
  that shows it; no other lane's run is cancelled. Waits are inline and print.
- No merge, no tag, no issue filed or closed; no attribution trailer; no
  `git add -A`; the branch asserted before every commit; nothing under
  `~/.claude`.

## 2. Inputs, verified (2026-10-21: origin, the release API, the archives)

| input | origin says | verdict |
|---|---|---|
| boreutils trunk `cc64f68` | `origin/trunk` `cc64f687…` (bu28, PR #43); 47 utilities (`//! member: false`), 9 unit-test files; pin wolf 0.2.33 / lupin 0.1.54 / std `cceda63`; open issues: #44 alone; 0 open PRs | holds |
| wolf 0.2.34 is `v0.2.34` at `9da7bdcf` | annotated tag naming `9da7bdcf2aea…`; release 419552903, published 2026-10-21 12:58:10Z | holds |
| the wolf archives | fetched on kasumi, each read twice, both reads equal to the API's digest (`ev/archives.log`): linux x86-64 `88a9dd3d…` (80,433,878 B), linux aarch64 `ca5cadf9…` (76,212,750 B), macOS arm64 `29c8331f…` (18,925,363 B), windows `77bb8403…` (15,911,654 B; read, never pinned: boreutils has no windows row). `_wolf` `a368c8ec…` in all three pinned archives (the file since 0.2.25); `std/STD-REV` `e036bec3…` in all three, 54 `.lu` files, 69 members each. `wolf --version`: `wolf 0.2.34 (wolfgang, pin 9da7bdc)` / `paired with lupin 0.1.55 (reference interpreter), pin 294d626`. `wolf` `2bfaf7b8…`, `libwolf_rt.a` `cc058247…`: r39's | holds |
| lupin 0.1.55 is `v0.1.55` at `e642f26` | annotated tag naming `e642f263…`; release 418932753; linux x86-64 `1152abc0…`, linux aarch64 `5854ab26…`, macOS arm64 `2eac1ccc…`, each read twice, equal to the API; `lupin 0.1.55 (wolf-interp, reference interpreter at pin 294d626)`; `lupin` `ad52ee96…`: r39's | holds |
| the bundled std is wolf-std `e036bec` | `STD-REV` in the archives; the commit exists on wolf-std. wolf-std trunk has since moved to `3bacc5f` (sc69, merged 2026-10-21: "the next STD-PIN", 0.2.35's); the contract names the bundle, so trunk is no candidate here | B151: `cceda63` (the old pin) against `e036bec` |
| the 0.2.34 CHANGELOG | "**boreutils, muzzle:** the pin." Seven new prelude names and the mark `busy`: `src/` declares and calls none (`grep`; r39's downstream grep says so too). The mode int's bits 5–7 and the restore at exit: no `os_term_` call in `src/`. #799 (`wolf test` runs a test file's own `test_*`): `src/`'s package members are the 9 test files alone (every utility is `member: false`), each with a `main` and no `test_*`, so no plain file sorts before a test. `os_signal_wait_fds`'s hub before `main`: no utility names it. The std moves `cceda63` → `e036bec`: under `std/` only `process`, `signal`, `net` and `os/users` change; `src/bore/signals.lu` and `src/timeout.lu` `use std.signal`, which imports `std.process` and `std.fs`, so every utility reaches two of the four changed files | holds |
| r39's STOP 3 (`crawl-54.md`) and its evidence row (planning branch `r39`, `07e9814`) | `cc64f68` against the published 0.2.34 + 0.1.55 in a throwaway px12-ubuntu box, `wolf-toolchain.toml`'s two `version_line`s and std `rev` edited locally: builds rc 0 on both tiers (47 each); **difftest release 6,668 / 0 / 120, dev 6,668 / 0 / 120, verdict list `dcdb32cb0d7a5e25` on both**; the control (its own 0.2.33 pin) the same counts and list | the number of record this lane must equal |
| bu28's note and report (`crawl-54.md`, "s248 and bu28 merged") | at `18a6490` (`cc64f68`'s source): gauntlet 6,668 / 0 / 120 both tiers, list `dcdb32cb0d7a5e25`, killprobe 240,578 alike on `-l` and `-t` both tiers; killtest 365 / 0 / 0 and timeouttest 150 / 0 / 13 under `--cpus 0-3`; at `ac543c9` (the same suites' code) inouttest 104 / 0 / 0, idtest 1,098 / 0 / 28 | the suites' baseline |
| CI at `cc64f68` | bu28's labelled `tier full` 39371558222 (logs read): ubuntu `wolf test` 9 passed, difftest 6,675 / 0 / 113, roottest 178 / 0, killprobe alike (4 lines), killtest 365 / 0 / 0, timeouttest 162 / 0 / 1, idtest 1,098 / 0 / 28, inouttest 104 / 0 / 0; macOS difftest 6,481 / 0 / 307, killprobe alike, killtest 298 / 0 / 67, timeouttest 126 / 0 / 37, idtest 28 / 0 / 1,098, inouttest 52 / 0 / 52; field 5,649 / 42 / 1,097 against ubuntu's 9.4, `field-verdict: ADVISORY`. The latest nightly 39617412624 (2026-10-21) green, field 5,649 / 42 / 1,097 ADVISORY | CI's baseline |
| boreutils#44 | open: at the 0.2.35 pin `timeout` calls `os_core_off()` and the three `design` rows of its own core go | waits on 0.2.35 |
| hosts | kasumi: 16 cpus, load 2.3, `/home` 29 G free (97 % used); podman with `localhost/px12-ubuntu` and `ubuntu:24.04`; GNU 9.11 at `~/lanes/bu28/gnu/` (`timeout` `735f79ee…`, `kill` `a78a3c72…`, 103 programs, as bu28's note) | copied to `~/lanes/bu29/gnu/` |

## 3. Prediction (committed before the pin moves and before anything is measured at it)

1. **B151.** `cceda63` and `e036bec` each build all 47 utilities under 0.2.34
   with `--deny-warnings` on both tiers: 94 builds each, 0 failed, 0 warning
   lines. Most of the 94 binaries differ between the two (every utility
   reaches `std.signal` and `std.process` through `bore`; at bu28's B151 a
   std change of the same reach moved 86 of 94).
2. **The pin builds clean.** No diagnostic on either tier; all 94 binaries
   differ from trunk's at 0.2.33 (the runtime archive moved); `tools/check-fmt`
   rc 0; `tools/check-test` 9 passed, 0 failed. A failure planted in the
   last-sorted test file (`signals_test.lu`) fails exactly that file's row at
   both pins (each file runs its own `main`; #799 cannot reach this layout).
3. **The difftest of record** (kasumi, a throwaway px12-ubuntu box, no
   network, GNU 9.11): **release 6,668 / 0 / 120, dev 6,668 / 0 / 120, the
   verdict list `dcdb32cb0d7a5e25` on both: r39's.** The selftests
   (`difftest-selftest`, `difftest-evidence`, `field-verdict-selftest`) rc 0;
   killprobe 240,578 numbers alike on `-l` and `-t`, both tiers. Falsified by
   any verdict that moves.
4. **The suites** (kasumi, `ubuntu:24.04`, one throwaway container a case, GNU
   9.11 beside both tiers): killtest **365 / 0 / 0** and timeouttest
   **150 / 0 / 13** under `--cpus 0-3`, idtest **1,098 / 0 / 28**, inouttest
   **104 / 0 / 0**, roottest **178 / 0**; every selftest rc 0. The host's
   core store holds the same count after as before, none of this lane's.
5. **Why nothing moves:** no case reaches what 0.2.34 changes. The fork, the
   editor's calls, the mode bits and the restore are never called; the std's
   new functions are wrappers no utility calls (`kill` and `timeout` call the
   builtins directly). Bytes change, verdicts do not.
6. **CI.** `tier pr` at the head: ubuntu as at `cc64f68` (difftest 6,675 / 0 /
   113, killprobe alike, roottest 178 / 0, killtest 365 / 0 / 0, timeouttest
   162 / 0 / 1, idtest 1,098 / 0 / 28, inouttest 104 / 0 / 0, `wolf test` 9);
   the field leg 5,649 / 42 / 1,097 with its standing `ADVISORY` (lane-audit's
   one WARN). The labelled `tier full` adds macOS: difftest 6,481 / 0 / 307,
   killtest 298 / 0 / 67, timeouttest 126 / 0 / 37, idtest 28 / 0 / 1,098,
   inouttest 52 / 0 / 52.
7. **The plant** (the gate the pin leans on: identity, not only the digest).
   The 0.2.34 digests with 0.2.33's `version_line`, on a plant branch, a
   dispatch `-f tier=pr`: red on both legs at the first tool that sources
   `tools/lib-toolchain.sh` (the gauntlet at `wolf fmt --check`, the field leg
   at `build (release)`) with `toolchain: REFUSED — wolf identity: have "wolf
   0.2.34 (wolfgang, pin 9da7bdc)", pin wants "wolf 0.2.33 (wolfgang, pin
   85dab5d)"`, and green at the pin.

## 3a. The prediction, scored

§3 above is as committed (`30f56a1`), before the pin moved and before
anything was measured at it. Scored in place, by line. "kasumi" is a fresh
`--network none` container: `localhost/px12-ubuntu` for B151, the check-test
plant and the gauntlet (`box.sh`, `--ulimit core=0:0`), `ubuntu:24.04` for
the suites (one container a case, the suites' own). GNU is bu25's build of
9.11 (`~/lanes/bu29/gnu/`, copied from bu28's: `timeout` `735f79ee…`, `kill`
`a78a3c72…`). The `ev/` paths are committed under `notes/bu29/ev/`.

| # | predicted | measured | verdict |
|---|---|---|---|
| 1 | B151: `cceda63` and `e036bec` each 94 builds, 0 failed, 0 warnings; most binaries differ between them | **94 builds, 0 failed, 0 warning lines, 0 error lines, each** (`ev/b151.log`); **70 of 94 differ** (all 47 dev, 23 release), 24 alike; the archive's bundled `std/` and the tree fetched at `e036bec` differ only by the bundle's `LICENSE` and `LICENSE-EXCEPTION` | right |
| 2 | no diagnostic; all 94 differ from 0.2.33's; fmt rc 0; check-test 9 / 0; the plant in `signals_test.lu` fails that row alone at both pins | no diagnostic on either tier (`grep -c` 0 in both build logs); **0 of 94 alike** against bu28's build of the same source at 0.2.33 (`bins-head-18a6490.txt`); the pin's 94 are byte-identical to B151's `e036bec` builds (the build repeats); fmt rc 0; `wolf test` **9 passed, 0 failed** (`ev/check-test-pin.log`); planted, **8 passed, 1 failed, `signals_test.lu::main ... FAILED (trap(assert))`, at 0.2.33 and at 0.2.34** (`ev/checkplant.log`) | right |
| 3 | difftest 6,668 / 0 / 120 both tiers, list `dcdb32cb0d7a5e25`; selftests rc 0; killprobe alike | **release 6,668 / 0 / 120, dev 6,668 / 0 / 120, list `dcdb32cb0d7a5e25` on both** (`ev/gauntlet-pin.log`); stronger than predicted: both whole difftest logs are **byte-identical** to r39's own of the published 0.2.34 (`difftest-{release,dev}-pub-0234.log` on kasumi `~/lanes/r39/bu/ev/`, sha256 `e28fc7cf…` and `4774a352…`) and to its 0.2.33 control; `difftest-selftest`, `difftest-evidence`, `field-verdict-selftest` rc 0; killprobe 240,578 numbers alike on `-l` and `-t`, both tiers | right |
| 4 | killtest 365 / 0 / 0, timeouttest 150 / 0 / 13 under `--cpus 0-3`, idtest 1,098 / 0 / 28, inouttest 104 / 0 / 0, roottest 178 / 0; selftests rc 0; core store unmoved by the lane | **killtest 365 / 0 / 0, timeouttest 150 / 0 / 13** (both "every case under taskset -c 0-3 (Cpus_allowed_list 0-3, read inside)"), **idtest 1,098 / 0 / 28, inouttest 104 / 0 / 0, roottest 178 / 0**; every selftest rc 0 (`ev/suites-pin.log`). Every case line of killtest, timeouttest, idtest and inouttest (name, verdict, SKIP reason) equal to bu28's at `18a6490` / `ac543c9`. The store went 161 → 167, all six `core.threads.1000…` of px57's probe (`~/lanes/px57/…/threads`, 18:26 and 18:29 EDT); this lane's timeouttest rows left 204 journal entries (`sleep`, `dash`, both tiers' `timeout`, the container's uid) with COREFILE `none`, nothing stored (`ev/coredumps-during-bu29.txt`, `ev/corestore-after.txt`) | right |
| 5 | nothing moves: no case reaches 0.2.34's changes | so: every verdict, every SKIP reason and both difftest logs byte for byte; only the bytes of the binaries moved | right |
| 6 | CI `tier pr` ubuntu as at `cc64f68`, field 5,649 / 42 / 1,097 ADVISORY; `tier full` adds macOS as at `cc64f68` | scored at the PR's runs (§4) | — |
| 7 | the plant red on both legs at the first tool that sources `lib-toolchain.sh`, `toolchain: REFUSED — wolf identity …` | **red as predicted**: branch `bu29-plant` `99a5a45`, dispatch `-f tier=pr`, run **39683548043**: `gauntlet (ubuntu-latest)` job 119511893621 at `wolf fmt --check`, the field job 119511893615 at `build (release)`, both after the two digests read OK, both `toolchain: REFUSED — wolf identity: have "wolf 0.2.34 (wolfgang, pin 9da7bdc)", pin wants "wolf 0.2.33 (wolfgang, pin 85dab5d)"`; `tier pr` 119512108967 red (`ev/ci-39683548043-plant.txt`) | right |

## 4. Evidence index

Committed, `notes/bu29/ev/`: `archives.log` (seven archives, two reads each
against the release API's digests; `_wolf`, `STD-REV`, member counts, both
version lines, the staged binaries' digests); `b151.log`,
`b151-bins-{cceda63,e036bec}.txt`; `checkplant.log` and its four
`checkplant-*.log` (0.2.33's archive read twice against trunk's digest
`4f955e8d…` first); `gauntlet-pin.log` (fetch by digest, identity, build,
fmt, test, both difftests and the verdict list's digest, the selftests,
killprobe, the core store) with `build-*-pin.log`, `check-test-pin.log`,
`bins-pin.txt`, `difftest-{release,dev}-pin.log` (whole), `selftest-pin.log`,
`evidence-pin.log`, `field-verdict-selftest-pin.log`, `killprobe-pin.log`;
`suites-pin.log` with each suite's and selftest's own log; the core store
(`corestore-after.txt`, `coredumps-during-bu29.txt`); the plant's CI extract
`ci-39683548043-plant.txt`. Probes: `notes/bu29/probes/` (`archives.sh`,
`box.sh`, `b151.sh`, `run-b151.sh`, `checkplant.sh`, `run-checkplant.sh`,
`gauntlet.sh`, `suites.sh`, `run-pin.sh`; bu28's shapes with this lane's
paths, `suites.sh` adding roottest).

**The difftest of record** (kasumi, px12-ubuntu) at the pin `626efc5`:
**6,668 / 0 / 120 on both tiers, list `dcdb32cb0d7a5e25`**: r39's, and
bu28's at `18a6490`. Nothing moved.

**CI.** The plant: run 39683548043 (§3a line 7). The PR's `tier pr` and
`tier full` runs are named in the PR.

**Not built here:** static binaries for PAX (the contract: PAX's `user/*`
pins move in px57 and after); the bench (no program changed).

## 5. Findings, and what was not verified

- **Nothing moved.** At wolf 0.2.34 / lupin 0.1.55 / std `e036bec` every
  differential verdict, every suite's case lines and both whole difftest logs
  are what they were at 0.2.33; only the binaries' bytes changed (the runtime
  archive). No issue to file from this lane.
- **#799 cannot reach this layout**, measured rather than argued: the nine
  test files are the package's only members, and a failure planted in the
  last-sorted one fails its own row at both pins.
- **boreutils#44 waits on 0.2.35** (`os_core_off()`, s253, wolf-lang#847):
  the three `design` rows of `timeout`'s own core stay at this pin.
- **The field leg's advisory stands** as at `cc64f68`: ubuntu's own GNU 9.4,
  information, not a verdict (B98).
- **Not verified here:** the macOS pin (`29c8331f…` / `2eac1ccc…`), measured
  only by CI's `tier full`; linux aarch64 (pinned by digest, read twice, never
  run); no build on nomad-1 by rule.

**Housekeeping.** kasumi `~/lanes/bu29/` (the archives, the extracted
toolchains, the two std trees, GNU's copy, the tree and its `target/`) is
removed at hand-back once the logs above are committed. The branch
`bu29-plant` stays on origin: §3a cites it.
