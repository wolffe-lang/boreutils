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
