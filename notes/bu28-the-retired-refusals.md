# bu28 — the retired refusals (boreutils on wolf 0.2.33: the pin, #41, #37's record)

Lane note. **Class:** long (boreutils), **Opus**. **Crawl:** 54, batch 10.
Branch `bu28` off boreutils `43ee185` (bu27). Contract:
`sprints/boreutils/22-the-retired-refusals/bu28-the-retired-refusals.md`
(planning `73e7c1d`). §1–§3 are committed before any line of `src/`,
`tools/`, `tests/`, CI, the README or the pins changes, and before GNU's
`timeout` or `kill` has run any case this lane adds (GNU's answers bu27
recorded are read, not re-run); §3 is scored in place later (§3a), never
rewritten.

One deliverable, in order: boreutils pinned to wolf 0.2.33 / lupin 0.1.54
/ wolf-std `cceda63` (its own commit), the difftest of record on both
tiers no worse than `43ee185`'s 6,664 / 0 / 120; then boreutils#41's four
refusals retire, GNU 9.11 the oracle, each its own commit with its cases:
(1) `timeout -s SEGV`, `-s RTMIN` and `-s` a host number without
`--foreground` (`os_signal_ignore_one`, ruling #88 R1); (2) a command
dead of a fault leaves timeout dead of the same signal
(`os_exit_signal`, R2), not exit 139; (3) GNU's "dumped core" line
(`os_wait_poll_core`, R3 = D), measured with cores on and off; (4)
killprobe's 912 by-design rows a tier for signal 0 (`os_signal_text(0)`).
Then #37's record (ruling #87): a README "differences from GNU" entry, no
refusal. Static binaries for PAX and their calls; a plant per retired
refusal, red in CI.

## 1. Forbidden

- **No implementation's source is read**: not GNU coreutils', procps',
  util-linux's, busybox's, uutils', toybox's, any shell's, any libc's,
  systemd's, nor any kernel's. GNU's behaviour comes from `--help`, the
  info manual's `timeout invocation` and `kill invocation` nodes, POSIX,
  the man pages (`core(5)`, `signal(7)`, `sigaction(2)`, `wait(2)`), and
  black-box runs of the GNU coreutils 9.11 BINARIES bu25 built from the
  oracle tarball by digest (copied to kasumi `~/lanes/bu28/gnu/`).
- **Faults, group sends and core dumps only inside a throwaway container
  or a process tree the test made**, never on a host's real process
  table. Every probe and suite here starts `ulimit -c 0` unless its row
  is a cores-on row. kasumi's `kernel.core_pattern` pipes cores to
  `systemd-coredump` and the container's default `ulimit -c` is
  `unlimited` (§2): a cores-on row there would store a core on the HOST,
  outside the lane's directory, so **no cores-on row runs on kasumi**; it
  runs on CI's throwaway ubuntu runner under a file pattern, where the
  core is a file in the case's own directory inside its container, and is
  skipped by name where the pattern pipes. Core files only under the
  lane's own directory; the host's store is counted before and after.
- Signal meanings named through `std.signal`; no bit and no host number
  written; host signals reached as `-N` from what the host answers.
- No regression in the existing 47 utilities' cases; if the pin regresses
  one, stop and report (bu26's rule), do not bump.
- No `rm` outside `~/lanes/bu28/` (kasumi) and this lane's worktree; no
  `git add -A`; nothing under `~/.claude`; no edit to another lane's file;
  no merge, no tag, no issue filed or closed; no attribution trailer; no
  `2>/dev/null` on a checkout; the branch asserted before every commit.
- Toolchains from the release archives by digest, each read twice. No
  build on nomad-1. kasumi's login shell is fish (`bash -s`/`bash -c`);
  `setsid` with a pid file for long jobs, killed by recorded pid only;
  `/home` there had 22 G free at the start: one tree, pruned as it goes,
  this lane's images removed at the end. Host ports 8080 and 8088 never
  used. No package installed on any host.
- Strict evidence (wolf-lang#571): `wolf build` exit 2 is a compile
  error; SKIP lines counted over the full output; process and signal
  suites also under `taskset -c 0-3` (asserted inside the container);
  SigBlk and SigIgn read before a signal row is called red. No "seen red"
  without a run id. CI dispatches name one job; no other lane's run is
  cancelled. Waits are inline and print at least every five minutes. A
  harness refusal stops the lane and is reported.

## 2. Inputs, verified (2026-10-19, origin and the release archives)

| input | origin says | verdict |
|---|---|---|
| boreutils trunk `43ee185` | `origin/trunk` `43ee185` (bu27); 47 utilities; pin wolf 0.2.32 / lupin 0.1.54 / std `d37c911`; open issues #41 (four refusals retire at 0.2.33) and #37 (ruling #87 owes its README record); 0 open PRs | holds |
| wolf 0.2.33 is `v0.2.33` at `85dab5d7`; lupin 0.1.54 is `v0.1.54` at `0e536e8` | `v0.2.33` is an annotated tag naming commit `85dab5d7e597…` ("CHANGELOG: 0.2.33"); `v0.1.54` names `0e536e8fb451…` | holds |
| the release archives | release 417610226 (wolf, 2026-10-19 18:37Z), 415937354 (lupin, unchanged). Fetched on kasumi, each read twice, both reads equal to the API's digest (`ev/archives.log`): wolf linux x86-64 `4f955e8d…` (80,128,936 B), linux arm64 `24cde9e4…`, macOS arm64 `9152dbd1…`; lupin as pinned (`175df238…`, `5fb15e31…`, `9cd14db7…`). `_wolf` `a368c8ec…` in all three wolf archives (one build; the same file as 0.2.32's). `wolf 0.2.33 (wolfgang, pin 85dab5d)` / `paired with lupin 0.1.54 (reference interpreter), pin 294d626` | holds |
| the bundled std is wolf-std `cceda63` | `std/STD-REV` `cceda631…` in all three archives; wolf-std `origin/trunk` is `cceda63` (sc65; sc66 runs beside this lane, unmerged) | one candidate for `[std]` (B151) |
| the 0.2.33 CHANGELOG's boreutils line | "the toolchain digests; then four refusals retire (boreutils#41) … The 7 `kill 0` cases stay (ruling #86); #37 stays a recorded difference (ruling #87)". Five new prelude names: `os_signal_ignore_one`, `os_signal_default_one`, `os_exit_signal`, `os_wait_status_core`, `os_wait_poll_core`; `src/` declares none (`grep`), so no W0304. "A SEGV or BUS another process sends ends the program" under the default | holds |
| the crawl's "of record" | r38 STOP 2: `43ee185` against the PUBLISHED 0.2.33, 6,664 / 0 / 120 on both tiers, verdict list `2ee3368dc3ce6124` — bu27's head list at 0.2.32 (`notes/bu27/ev/gauntlet-head-17ebb87.log`) | the number this lane must not do worse than; re-measured here (§3 line 1) |
| spec at `v0.2.33` | `[os.signal.disp.one]`: `ignore_one`/`default_one(m)`, one meaning in the sending shape or `-N`; 0, KILL, STOP `invalid`; glibc's 32 and 33 `io` (its `sigaction` refuses them); SEGV and BUS stay the stack guard's, which tells a SENT one from a fault (on macOS by the program's own announced send); "GNU's `timeout` orders the spawn first and the ignore after". `[os.signal.exit]`: `os_exit_signal(m)`, the default, an unblock, a raise; 128 + N if the process lives on; rows `{invalid, unsupported}`. `[os.proc.status]`/`[os.proc.poll]`: `os_wait_poll_core()` answers `-(256 + N)` for an end that dumped core; "a pattern that pipes cores to a program dumps one whatever `RLIMIT_CORE` says (core(5); measured on kasumi, s246)". `[os.signal.text]`: `os_signal_text(0)` is `strsignal(0)`'s words, `Unknown signal 0` (glibc), `Unknown signal: 0` (macOS) | holds |
| rulings #86, #87, #88 | #86: group 1 stays refused (the 7 `kill 0` killtest cases stay `ours`); #87: the self-appending filters are a recorded difference, no refusal; #88: R1 A, R2 A, R3 D | holds |
| s246's witness for cores (`signal_gaps_lanes.rs` at `v0.2.33`) | a cores-on row SKIPs by name where the pattern pipes (it would write the core outside the test's directory); CI's linux job sets a FILE pattern on its throwaway runner and `WOLF_CORE_REQUIRE=1` makes that skip a failure | taken as the shape here (`BORE_CORE_REQUIRE`) |
| bu27's note and suites | §3a: the five design differences; `tests/timeout/cases.toml` 124 cases, 10 `ours` (8 refused `-s` signals, the SEGV 139, GNU's `-s CHLD` hang) and 9 that leave standard error out of the comparison (the `dumped core` line: `--foreground -s SEGV` and the `sent:` QUIT, XCPU, XFSZ, ABRT pairs); `tests/kill/cases.toml` 7 `ours` (group 1); `tests/cases/kill.toml` 84 cases carry the `-t` mask for signal 0's row; killprobe 912 by design a tier. GNU's line, recorded by bu27 (`ev/tprobe-gnu.log`, `tprobe2-gnu.log`): `timeout: the monitored command dumped core`, at the expiry and without it, with `--foreground` too | holds |
| bu25's probes | `ev/probe-p4-gnu.log` `f3a4f2aa…` and `probe-p4-w1rel.log` `2ec931a1…` on kasumi `~/lanes/bu25/ev/` (read: both digests equal bu25's note's prefixes); `notes/bu25/probes/p4.sh` | holds; copied into this lane's evidence |
| pax `notes/px51` | PAX served every call bu27 traced for `kill` and `timeout` (`setpgid`, `kill(-g)`, `socketpair(SOCK_SEQPACKET)`, `vfork`, `clone3`, `tgkill`, `rt_sigsuspend`, `wait4` with `WUNTRACED`); static release `kill` `0f4fb3b7…`, `timeout` `de9104db…` | holds |
| hosts | kasumi: 16 cpus, load 10–12 (other lanes), `/home` 22 G free; podman with `localhost/px12-ubuntu` and `ubuntu:24.04`; `kernel.core_pattern` `\|/usr/lib/systemd/systemd-coredump %P %u %g %s %t %c %h %d %F %I`, the same inside a container; a container's `ulimit -c` is `unlimited` (soft and hard); the host store holds 191 cores at 19:30Z, none this lane's | holds; the reason for §1's cores rule |

## 3. Prediction (committed before the first change, and before GNU runs a case this lane adds)

**The pin (wolf 0.2.33 / lupin 0.1.54 / std `cceda63`).**

1. The difftest of record at the pin, in a throwaway px12-ubuntu
   container on kasumi, is **6,664 / 0 / 120 on both tiers, list
   `2ee3368dc3ce6124`**, r38's. Falsified by any verdict that moves.
2. No diagnostic in either tier's build; every one of the 94 binaries
   differs from trunk's at 0.2.32 (the runtime moved); at the pin with
   `src/` untouched: killtest 365 / 0 / 0, inouttest 104 / 0 / 0, idtest
   1,098 / 0 / 28, timeouttest 124 / 0 / 0, and killprobe still 912 by
   design a tier (the code never asks `os_signal_text(0)`).

**(3) The core line** (taken first: (1) and (2)'s cases need it).

3. GNU on kasumi (a pipe pattern, `ulimit -c 0`): `timeout: the monitored
   command dumped core` on standard error whenever the command's end
   dumped core — at the expiry or not, with `--foreground` or not, with
   `-p` — before timeout ends; every SEGV, QUIT, ABRT, ILL, TRAP, BUS,
   FPE, SYS, XCPU, XFSZ end dumps there under `ulimit -c 0`. On CI's
   ubuntu runner under a file pattern: none under `ulimit -c 0` (no
   line), one core file in the case's directory and the line under
   `ulimit -c unlimited`. With standard error closed, no line and the
   same status. On macOS (`ulimit -c 0`): no line.
4. GNU's timeout, ending by the signal its command died of, **dumps no
   core of its own** (its raw status carries no core bit on either host,
   and a cores-on row leaves one core file, the command's). Ours, ending
   through `os_exit_signal` ("the end is the host's, with a core where it
   writes one"), **carries the core bit** where the host dumps — a new
   difference this lane will have to record, not retire (wolf has no call
   for a process's own core limit). Falsified if GNU's own end carries
   the bit too, or ours does not.
5. After the change, ours prints GNU's line wherever GNU does, so the 9
   cases that leave standard error out compare it again, and timeouttest
   is 0 failed on kasumi (both tiers, plain and `taskset -c 0-3`) and on
   both CI legs, the cores-on rows included on ubuntu.

**(1) The group send of a signal timeout cannot hear.**

6. GNU (bu27's record, re-asserted as `expect` on every run): `-s SEGV`,
   `ILL`, `TRAP`, `BUS`, `FPE`, `SYS`, `RTMIN`, `16` without
   `--foreground` answer 124 at about 0.3 s, and the command's own child
   ends with it (the group). `-p -s SEGV` answers exit 139; `-v` says
   `sending signal SEGV to command 'sleep'`. Not measured by bu27 and
   predicted: `-s 32` and `-s 33` (glibc's own, which `sigaction`
   refuses) end GNU's timeout by that signal (its group send reaches it
   unignored).
7. Ours after the change: every one of those as GNU on both tiers, the 8
   `design:` cases GNU-compared (renamed), the refusal's 125 and its
   message gone; `-s 32`/`-s 33` sent as GNU sends them (the ignore's
   `io` taken, the send made). On macOS the six fault signals and the
   host's own `EMT` to the group answer 124 as GNU's. difftest gains
   `-s SEGV`, `-s RTMIN`, `-s 16` with a command no host can run, 127
   on both sides (ours: 125 before the change).

**(2) The end by the command's fault.**

8. GNU: a command that ends by SEGV (and ILL, ABRT, QUIT, BUS, FPE, TRAP,
   SYS) leaves GNU's timeout dead by the same signal, after the core line
   where the end dumped. Ours after the change: the same status on both
   tiers and both hosts, the 139 gone; the case's `ours` removed.

**(4) Signal 0's words.**

9. `kill -t 0`, `-t EXIT` and the whole tables: ours prints `Unknown
   signal 0` (linux) / `Unknown signal: 0` (macOS) as GNU does; the 84
   masks come out of `tests/cases/kill.toml` with every case passing;
   killprobe **0 by design and 0 parted** over the same 240,578 numbers
   on both tiers, on kasumi (inside px12-ubuntu) and on CI's macOS runner.

**The counts.** By design and refused, before → after:
timeouttest `ours` 10 → 1 or 2 (GNU's `-s CHLD` hang stays; line 4 may
add one), refused by name (125) 8 → 0, standard error left out for the
core 9 → 0; killtest `ours` 7 → 7 (ruling #86); killprobe by design 912
→ 0 a tier; difftest's signal-0 masks 84 → 0.

**#37.** No code: a README "Differences from GNU" entry for the streaming
filters appended onto their own input, citing bu25's `ev/probe-p4-*`
(copied in here), measured again at the head with ours (the same rows
fill the tmpfs at 8 B and 5,000 B; GNU's stop after one pass there).

**For PAX.**

10. Static binaries as `tools/mkboreutils` builds them (`wolf build
    --release --no-cache --deny-warnings`, a `cc` adding `-static`, in
    px12-ubuntu, ET_EXEC and no PT_INTERP), all 47 at the head; `kill`
    and `timeout` move from bu27's `0f4fb3b7…` and `de9104db…`. New calls
    for PAX: timeout's ignore of a host signal is
    `rt_sigaction(SIGRTMIN, SIG_IGN)` (and none for SEGV, whose handler
    stays the guard's); its end by a signal `rt_sigaction(SIG_DFL)`,
    `rt_sigprocmask(SIG_UNBLOCK)` and `tgkill` (or `kill`) of itself; the
    core is read from `wait4`'s status (no new call); `kill -t 0` none.

**Plants.** One branch per refusal put back at the head, each red in a
one-job CI dispatch on the rows it retired: R1 the 125 refusal, R2 the
139, R3 the plain `os_wait_poll` (no line: red only on the cores-on rows
on CI's runner), R4 no words for signal 0 (killprobe's 912 and the
unmasked `-t` cases).

## 3a. The prediction, scored

§3 above is as committed (`be6a9d4`), before the first change and before
GNU ran a case this lane added. Scored in place, by line. "kasumi" is a
fresh `--network none` container a case (`ubuntu:24.04` for the suites,
podman, `--cpus 0-3` asserted inside where named; `localhost/px12-ubuntu`
for the gauntlet and the probes, `--ulimit core=0:0`). GNU is bu25's
build of 9.11 (`~/lanes/bu28/gnu/`, `timeout` `735f79ee…`, `kill`
`a78a3c72…`). The `ev/` paths are committed under `notes/bu28/ev/`.

| # | predicted | measured | verdict |
|---|---|---|---|
| 1 | the pin's difftest 6,664 / 0 / 120 both tiers, list `2ee3368dc3ce6124` | **6,664 / 0 / 120 on both tiers, list `2ee3368dc3ce6124`** (`ev/gauntlet-pin.log`), r38's | right |
| 2 | no diagnostic; 94 binaries differ; killtest 365/0/0, inouttest 104/0/0, idtest 1,098/0/28, timeouttest 124/0/0; killprobe 912 by design | no diagnostic (`grep -c` 0, both tiers); **94 of 94** differ from bu27's head at 0.2.32; killtest **365 / 0 / 0**, inouttest **104 / 0 / 0**, idtest **1,098 / 0 / 28**, killprobe 912 by design a tier (`ev/suites-pin.log`, `ev/gauntlet-pin.log`). timeouttest **123 / 1 / 0**, not predicted: the one row is `no expiry: the command ends by SEGV`, whose `ours` said exit 139, and at 0.2.33 this timeout ends by SEGV as GNU's does — 0.2.33 lets a SEGV a program SENDS itself end it under the default (the CHANGELOG's "A SEGV sent to a program ends it"), and `ended`'s re-raise sends one. A by-design row moving to GNU's answer, not a verdict moving away from it: taken as the pin's (`1111c92` drops the `ours`), not a stop | right but one, which moved toward GNU |
| 3 | GNU's line at every fault end on kasumi, at the expiry or not, `--foreground`, `-p`; none on CI's file pattern under `ulimit -c 0`, one core and the line under `unlimited`; standard error closed: no line; macOS none | each so (`ev/tprobe3-gnu.log`: SEGV, ILL, ABRT, QUIT, BUS, FPE, TRAP, SYS, XCPU, XFSZ ends; `-s SEGV`/`QUIT`/`ABRT` at the expiry; `-p`, `-v`, `--foreground`); on CI's ubuntu runner, set to `core.%p`, the 12 cores-on rows ran and matched their `expect` (one core file, the line), the default rows printed none (PR run 39327635149); macOS printed none. Not predicted: the runner's own pattern is `systemd-coredump`'s, as kasumi's | right |
| 4 | GNU's own end dumps no core; ours carries the core bit — a new difference to record | so: GNU's raw status never carries the core bit, not even on kasumi's pipe (`ev/tprobe3-gnu.log`); ours does (raw 139 = SEGV + core, `ev/tprobe3-r2-release.log`), and under CI's cores-on rows leaves a second core file: 3 `design` rows (`core = "core", cores = 2`) | right |
| 5 | ours prints GNU's line wherever GNU does; timeouttest 0 failed on kasumi (plain and `taskset -c 0-3`) and both CI legs, cores-on rows included | kasumi at `33344d6`'s change: **125 / 0 / 10** plain and `--cpus 0-3` (`ev/tt-r3.log`); at the head **150 / 0 / 13** (`ev/suites-head-ac543c9.log`); CI ubuntu **162 / 0 / 1**, macOS **126 / 0 / 37** (PR run 39327635149) | right |
| 6 | GNU: the 8 refused signals 124 at 0.3 s, the child gone; `-p -s SEGV` 139; `-v`; `-s 32`/`-s 33` end GNU by that signal | each so (`ev/tprobe3-gnu.log`): 124 at 0.3 s for SEGV, ILL, TRAP, BUS, FPE, SYS, RTMIN, RTMAX, RTMIN+5, 16; the child gone for SEGV, RTMIN, 16; `-p -s SEGV` exit 139, `-p -s RTMIN` 162; GNU dies of 32 and of 33. Not predicted: GNU leaves the signal it sent its group ignored after the send (`SigIgn` at 1.0 s holds SEGV, RTMIN, TERM, CONT) and lives through a later SEGV sent to it | right, wider than predicted |
| 7 | ours as GNU on every one, both tiers; `-s 32`/`33` sent; macOS's six and `EMT` 124; difftest's three 127s | every one as GNU on both tiers but **`-s 33`**: this timeout lives (124) where GNU's dies of it — its process holds a handler on 33 it never installed (`SigCgt` bit 32 set on both tiers, static and dynamic; GNU's has none), so its own group send reaches that handler; recorded as one `design` row. `-s 32` ends it as GNU's. macOS: the six and `EMT` 124 (CI). difftest gained four (`-s BUS -k 1` too), 127 on both sides, red at the pin (125) (`ev/difftest-timeout-r1-red-pin.log`) | right but one |
| 8 | GNU's timeout dies of its command's fault; ours the same, the 139 gone | so on both tiers and both hosts (ILL, BUS, FPE, TRAP, SYS, ABRT, SEGV, `-p`, `--foreground`, `-v`). The 139 itself was gone at the pin (line 2); `os_exit_signal` puts the end on the ruled call: a thread-directed raise, the 100 ms sleep gone, and a command dead of glibc's 32 now leaves timeout at **exit 160 as GNU's** (`os_exit_signal` exits 128 + N where the signal ends nothing), where the pin's send-to-self died of 32 | right, plus one row |
| 9 | `kill -t 0` / `EXIT` / the tables with GNU's words; the 84 masks out; killprobe 0 by design, 0 parted, kasumi and macOS | so: kasumi **240,578 alike on `-l` and `-t`, both tiers** (`ev/killprobe-head-ac543c9.log`); CI ubuntu and macOS the same in the gauntlet (PR run 39327635149, macOS `Unknown signal: 0`); `tests/cases/kill.toml` 894 / 0 / 1 without the masks; at the pin the same cases are 10 FAIL and killprobe 912 parted a tier (`ev/difftest-kill-r4-red-pin.log`, `ev/killprobe-r4-red-pin.log`) | right |
| counts | timeouttest `ours` 10 → 1 or 2; refused 8 → 0; standard error left out 9 → 0; killtest 7 → 7; killprobe 912 → 0; masks 84 → 0 | `ours` **10 → 1** (`design: -s CHLD`, GNU's hang) and `design` **0 → 4** (three rows of timeout's own core, one `-s 33`); refused by name (125) **8 → 0**; standard error left out **9 → 0**; killtest `ours` **7 → 7** (ruling #86); killprobe by design **912 → 0** a tier; difftest's signal-0 masks **84 → 0** | right on all but `ours`+`design`: 5, not 1 or 2 |
| #37 | README entry; ours fill the tmpfs at 8 B and 5,000 B where GNU's stop | `fd36833`; p4 again at 0.2.33: ours **byte-identical** to bu25's `probe-p4-w1rel.log` (`2ec931a1…`), GNU's to `probe-p4-gnu.log` (`f3a4f2aa…`) | right |
| 10 | static as mkboreutils; `kill`/`timeout` move; `rt_sigaction(SIG_IGN)` for RTMIN, none for SEGV; the end `rt_sigaction(SIG_DFL)`, `rt_sigprocmask(SIG_UNBLOCK)`, `tgkill`; the core from `wait4`; `kill -t 0` none | pax `d6fbcdc`'s `tools/mkboreutils` with the two pin lines at the head: 47 ET_EXEC, no PT_INTERP; release `kill` `f9357f76…`, `timeout` `ea392120…` at `e55da7d` (both moved from bu27's; §4). Calls (`ev/straces.log`): the SEGV ignore makes no call (the guard's handler stays), RTMIN's is `rt_sigaction(SIGRT_2, SIG_IGN)` (strace's name for 34), the sends `kill(-PGID, SEGV/SIGRT_2)` then `kill(-PGID, CONT)`; the end `rt_sigaction(SIG_DFL)`, `rt_sigprocmask(SIG_UNBLOCK, [SEGV])`, `tgkill(pid, pid, SEGV)`; the core is `wait4`'s `WCOREDUMP`; `kill -t 0` `statx` and `write` only | right |
| plants | each red in a one-job dispatch on the rows it retired | each a branch off `916a55b`, red in a one-job dispatch, every run of it (`ev/ci-<run>-plant-*.txt`): **R1** `370b34c` (`bu28-plant-r1`, the 125 refusal back), run **39327744649**: timeouttest 27, 26, 26 of 163 failed in its 3 runs — the 23 `group send:` rows and the 2 cores-on group rows each time, and 1–2 rows of the double delivery below; **R2** `72cb2b3` (the 139 back for a signal timeout cannot hear), run **39327747898**: 13 in each run — the 10 `no expiry:` fault rows and `core: the command ends by SEGV`, and, by the plant's own reach, the ends by KILL and by RTMIN; **R3** `e5d11b7` (the released poll), run **39327752068**: 11, 10, 11 — the 9 cores-on rows that carry the line each time, and 1–2 double deliveries; **R4** `6604bce` (no words for 0), run **39327755394**: killprobe `PART` 912 of 240,578 on `-t`, each tier (and killtest green) | red, all four |
| — | (not predicted) | **A double delivery, bu27's race, found by the plants' repeated runs**: on CI's 4-cpu runner a command that traps the passed-on or expiry signal now and then printed its trap's line twice (`release stdout: 'got TERM\ngot TERM\n', gnu 'got TERM\n'`): HUP, USR1, USR2, VTALRM, XFSZ, TERM, ABRT, PIPE across runs 39327744649 and 39327752068. Not this lane's change, nor the pin's: the 0.2.32 control (`bu28-control-0232` = trunk `43ee185`, run **39338981129**) shows it too (`expiry: the command traps TERM and exits 3`, 1 of 3 runs), the pin control (`bu28-control-pin` `16b2445`, run 39338984826) none in 3; never on kasumi (16 cpus, nor 2 under `taskset`). The command gets the signal twice, from its own send and from the group's, and between them sat this timeout's ignore; GNU's make only a `sigaction` between them (strace of the binary, `ev/` `gnu-passon.sh`). `e55da7d` puts the ignore first, so the two sends are adjacent (strace: `sigaction(SIG_IGN)`, `kill(pid)`, `kill(-pgid)`); kasumi 150 / 0 / 13 plain and `--cpus 0-3` (`ev/tt-rx.log`); CI: see §4 | a finding, fixed |

## 4. Evidence index

Committed, `notes/bu28/ev/`: `archives.log` (six archives, two reads
each against the release API's digests, `_wolf`, `STD-REV`, the version
lines); `b151.log`, `b151-bins-*.txt` (all 47 on both tiers under 0.2.33
with std `d37c911` and with `cceda63`: 94 builds each, 0 failed, 0
warnings); `gauntlet-pin.log`, `gauntlet-head-ac543c9.log`,
`gauntlet-head-e55da7d.log` (build, fmt, test, difftest both tiers with
the verdict list's digest, the selftests, killprobe); `suites-pin.log`,
`suites-head-ac543c9.log` (killtest 365 / 0 / 0, inouttest 104 / 0 / 0,
idtest 1,098 / 0 / 28, timeouttest 150 / 0 / 13, `--cpus 0-3` for kill
and timeout), `suites-head-e55da7d.log` (timeouttest 150 / 0 / 13 under
`--cpus 0-3`: the reorder touches `timeout` alone) and each suite's own
log;
`tt-r3.log`, `tt-r1.log`, `tt-r2.log`, `tt-rx.log` (timeouttest after each
refusal and the reorder, plain and `--cpus 0-3`); the reds before the
greens: `timeouttest-r3-red-pin.log` (6 of 13: no line at the pin),
`timeouttest-r1-red-pin.log` (23 of 23 `group send:`, 125),
`difftest-timeout-r1-red-pin.log` (4 of 116), `timeouttest-r2-red-0232.log`
(bu27's 0.2.32 build: exit 139), `timeouttest-r2-red-pin.log`,
`difftest-kill-r4-red-pin.log` (10 of 895), `killprobe-r4-red-pin.log`
(912 a tier); `tprobe3-gnu.log` (GNU timeout with a fault, a host signal
and a core, the raw status, the core bit, the dispositions after a send)
and ours at the pin, R3, R1, R2 (`tprobe3-*-{release,dev}.log`, the diffs
`tprobe3-diff-*.txt`); `killprobe-*.log`; `corestore-*.txt` (kasumi's
host store before and after; 193 throughout this lane's runs once the
two other lanes' cores of 15:49 had landed, none this lane's); bu25's
`probe-p4-gnu.log` and `probe-p4-w1rel.log` (`bu25/`) and p4 again
(`probe-p4-head-release.log`, `probe-p4-gnu-again.log`); `straces.log`
and `static-head.log`, `static-digests.txt` (below); CI extracts
`ci-<run>-*.txt`. Probes and scripts: `notes/bu28/probes/` (`tprobe3.sh`,
`gnu-passon.sh`, `straces.sh`, `box.sh`, `cbox.sh`, `gauntlet.sh`,
`suites.sh`, `tt.sh`, `b151.sh`, `run-pin.sh`). Generator:
`notes/bu28/gen/kill_cases_0233.py`.

kasumi `~/lanes/bu28/`: `ev/` (the above, the full difftest logs and
`strace*/`), `gnu/` (GNU 9.11), `bin/static-head/` (the static binaries),
`pax/` (mkboreutils and its pin).

**The difftest of record** (kasumi, px12-ubuntu): at the pin
**6,664 / 0 / 120** both tiers, list `2ee3368dc3ce6124` (r38's); at the
head **6,668 / 0 / 120** both tiers, list `dcdb32cb0d7a5e25`, at `ac543c9`
and again at `e55da7d` (`gauntlet-head-*.log`) — the pin's
list plus exactly the four new `timeout` cases (`signal: -s SEGV`,
`RTMIN`, `16`, `BUS -k 1`, a command no host can run). CI at `916a55b`:
ubuntu 6,675 / 0 / 113, macOS 6,481 / 0 / 307.

**CI.** PR run **39327635149** at `916a55b` green, log read: ubuntu
difftest 6,675 / 0 / 113, killprobe 240,578 alike on `-l` and `-t` both
tiers, roottest 178 / 0, killtest 365 / 0 / 0, timeouttest **162 / 0 / 1**
(the runner's own pattern `systemd-coredump`'s, set to `core.%p`; the 12
cores-on rows ran), idtest 1,098 / 0 / 28, inouttest 104 / 0 / 0; macOS
difftest 6,481 / 0 / 307, killprobe alike, killtest 298 / 0 / 67,
timeouttest **126 / 0 / 37** (the cores-on rows skipped by name:
`/cores/core.%P`), idtest 28, inouttest 52 / 0 / 52. Every other FAIL
line in the log is a selftest plant. Plants: §3a. Controls: 39338981129
(0.2.32), 39338984826 (the pin). At `e55da7d` (the reorder): see the PR.

**Static binaries for PAX's next pin** (linux x86-64, pax `d6fbcdc`'s
`tools/mkboreutils` with its two pin lines moved to this branch's head, in
px12-ubuntu, glibc 2.39 `libc.a`; ET_EXEC, no PT_INTERP, each read twice:
`ev/static-digests.txt`, all 47 in `bin/static-head/release/sums.txt`):
at `e55da7d`:

| binary | sha256 | bytes |
|---|---|---|
| `release/kill` | `f9357f765506e2f0dcc8dd33d35c737a15eec9d2baac549ab65496f0228846b9` | 13,999,632 |
| `release/timeout` | `ea39212046270980b2a86ecef2693880653747dee08f60b28b1ed7b0b8f8e1a1` | 14,575,880 |
| `dev/kill` | `1180b93de4c7501f6be588c1a839e6df2e6a4396eabbdd58e1eb56a05e715ea5` | 14,858,280 |
| `dev/timeout` | `e3d59d2d303243d35b0de25d7861f40b476a6ab33fa3c626e23b8522ca63a618` | 15,062,928 |

The other 45 release binaries are in `static-digests.txt`. The build
repeats: at `916a55b` (before the reorder) every release binary but
`timeout` had the same digest (`static-digests-916a55b.txt`). Not booted
on PAX. Their calls beyond bu27's (`ev/straces.log`):
`rt_sigaction(SIGRT_2, SIG_IGN)` (a host signal ignored; SEGV's ignore
makes no call), `kill(-PGID, SIGSEGV/SIGRT_2)`, `rt_sigaction(SIG_DFL)` +
`rt_sigprocmask(SIG_UNBLOCK)` + `tgkill(self)` (the end by a signal), a
`WCOREDUMP` status from `wait4` (no new call); `kill -t 0` none.

## 5. Findings, and what was not verified

**For wolf-lang (not filed: a lane files nothing).**
- *No call makes a process undumpable or sets its own core limit*
  (`prctl(PR_SET_DUMPABLE)`, `setrlimit(RLIMIT_CORE)`): GNU's timeout, ending
  by its command's signal, dumps no core of its own on any host; ours, by
  `os_exit_signal`, dumps where the host writes one (a second core file
  under `ulimit -c unlimited`, a dump handed to `systemd-coredump`).
  Witness: the three `design` rows `core:` in `tests/timeout/cases.toml`.
- *A handler on 33 the program never installed*: a wolf program's
  `SigCgt` has signal 33 caught (bit 32) on both tiers, static and
  dynamic, where GNU's single-threaded timeout's has none, so a group send
  of 33 cannot end it (`os_signal_ignore_one(-33)` is `io`, as the spec
  says). Witness: `group send: -s 33, GNU's timeout ends by it`.
- *The runtime's ignore between two sends is wide enough to matter*: see
  §3a (the double delivery); worked around here by ordering, not a wolf
  fault.

**For boreutils.**
- Not seen before and not changed (no case): GNU's timeout leaves INT
  and QUIT ignored when started with them ignored (a `&` job of a
  non-interactive shell), ours listens for them and passes them on; GNU
  leaves the signal it sent its group ignored after the send, ours listens
  again for a listenable one (`ev/tprobe3-gnu.log`, the dispositions).
- `tools/timeouttest` gained `core`, `cores`, `cores = "on"` and `design`;
  CI's ubuntu timeout legs set a file core pattern (`269737a`).

**Not verified.** The cores-on rows on kasumi or any pipe-pattern host
(skipped by name, by rule); `timeout` and `kill` on linux aarch64; the
static binaries on PAX; macOS's own handling of a SEGV another process
sends under an ignore (#790), which no case here exercises.

**Housekeeping.** kasumi `~/lanes/bu28/` keeps `ev/`, `gnu/`,
`bin/static-head/` and `probes/`; the two trees (`boreutils/`, `dev/`) and
`arch/` are removed at hand-back. Branches `bu28-plant-r1` … `r4`,
`bu28-control-0232`, `bu28-control-pin` and `bu28-repeat` stay on origin:
§3a cites them.
