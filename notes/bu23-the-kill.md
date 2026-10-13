# bu23 — the kill (boreutils on wolf 0.2.29: `kill`)

Lane note. **Class:** long (boreutils), **Opus**. **Wave:** 53. Branch
`bu23` off boreutils `2ab3651` (bu22). Contract:
`sprints/boreutils/17-the-kill/bu23-the-kill.md` (planning `a35b2fe`).
§1–§3 are committed before GNU's `kill` has been run once by this lane
and before any line of `src/`, `tools/`, `tests/` or the pins changes;
§3 is scored in place later, never rewritten.

One deliverable: boreutils pinned to wolf 0.2.29 / lupin 0.1.52 (its own
commit), and `kill` written on `os_signal_send` and `os_signal_number`,
measured against GNU coreutils 9.11's `kill` and POSIX in throwaway
containers: `-s NAME`, `-NAME`, `-NUMBER`, `-l`, `-l NUMBER`, `-L`/`-t`
as GNU has them, exit statuses, messages; a process group refused by
name if wolf cannot express one; a static `kill` and its system calls
for PAX; plants.

## 1. Forbidden

- **No implementation's source is read**: not GNU coreutils', not
  util-linux's, procps', busybox's, uutils', toybox's, nor any shell's
  builtin `kill`. GNU's behaviour comes from its `--help`, its manual's
  `kill invocation` node, POSIX.1-2024 `kill`, and black-box runs of the
  GNU coreutils 9.11 BINARY built from the oracle tarball by digest.
  **Which binary answered is recorded with every measurement**: on most
  hosts the `kill` a shell runs is the shell's builtin, and the
  `/usr/bin/kill` beside it is procps' or util-linux's.
- **Signal meanings are named, never literal bits**, and a host signal
  number is never written: `os_signal_number` is the one way from a
  meaning to this host's number, so every table `kill` prints comes
  from it, on linux and on macOS alike.
- **A signal is sent only to a process the test itself started, inside
  a fresh `--network none` container** (on CI's macOS leg, which has no
  container engine, on the runner, the throwaway machine, and still
  only to the test's own children). Never to a host process: kasumi is
  shared. No case hands any `kill`, this lane's or GNU's, the ids `0`,
  `-1` or a negative id outside a fresh container.
- A name wolf cannot send is refused with GNU's message shape where GNU
  would also refuse, and listed where GNU would not. No regression in
  the 39 utilities' cases.
- No `rm` outside `~/lanes/bu23/` (nomad-1 and kasumi) and this lane's
  clones; no deletion in a tree this lane did not make; no `git add -A`;
  nothing under `~/.claude`; no edit to another lane's file; no merge,
  no tag, no issue filed or closed; no attribution trailer; no
  `2>/dev/null` on a checkout; the branch asserted before every commit.
- The toolchain from the RELEASE ARCHIVES by digest, each read twice.
  No build on nomad-1. kasumi's login shell is fish (`bash -c`);
  `setsid` with a pid file; a job is killed by its recorded pid only,
  never by name, pattern or process group. `/home` there is near full:
  one build tree, pruned as it goes, this lane's container images
  removed at the end. Scratch under `~/lanes/bu23/`, never `/tmp`.
- Strict evidence (wolf-lang#571): `wolf build` exit 2 is a compile
  error, never a skip; SKIP lines are counted over the full output;
  the sending tests also run under `taskset -c 0-3`; SigBlk and SigIgn
  are read before a signal row is called red. No "seen red" without a
  run id, sha, path or digest. No other lane's run cancelled. Waits are
  inline and print at least every five minutes. A harness refusal stops
  the lane and is reported.

## 2. Inputs, verified (2026-10-13, origin and the release archives)

| input | origin says | verdict |
|---|---|---|
| boreutils trunk `2ab3651` or later | `origin/trunk` is `2ab36513` (bu22); 39 `src/*.lu` entries; pin wolf 0.2.28 / lupin 0.1.51, std `98e1b7b`; 5,646 `[[case]]` tables in `tests/cases/`; 0 open PRs | holds |
| wolf 0.2.29 is `v0.2.29` at `6ffe7c60`; lupin 0.1.52 is `v0.1.52` at `025428b` | `git rev-parse v0.2.29^{}` = `6ffe7c6056ee…`, `v0.1.52^{}` = `025428b725a3…` (annotated tags `6f732110`, `6f099396`) | holds |
| the release archives | fetched on kasumi, each hashed twice from two reads (`~/lanes/bu23/ev/archives.log`), equal to the release API's digests and to r34's evidence: wolf linux x86-64 `ae466e85…` (78,902,948 B), linux arm64 `584b8fc2…`, macOS arm64 `a79928ba…`; lupin linux x86-64 `f5194b74…`, linux arm64 `ac612122…`, macOS arm64 `66dc74d8…`. `_wolf` is `a368c8ec…` in all three wolf archives. `wolf 0.2.29 (wolfgang, pin 6ffe7c6)` / `paired with lupin 0.1.52 …, pin 294d626`; `lupin 0.1.52 (wolf-interp, reference interpreter at pin 294d626)` | holds |
| the archive's std | `std/STD-REV` in all three wolf archives is `d7c2968c…` (sc59), 57 files. wolf-std `trunk` is `9e5bd6b1…` (sc60, merged 2026-10-13): pinned to 0.2.29 / 0.1.52, and the first std whose `std.signal` names all 28 meanings (`reload()` … `bad_syscall()`) | candidates for `[std]`: `d7c2968` and `9e5bd6b`. The CHANGELOG says "write the new bits as numbers" until wolf-std catches up; it has, and this lane's rule is that no bit is written, so `[std]` is expected to move to `9e5bd6b` (B151 first). **Reported:** sc60's four spellings (R1 `continued()`, R2 `env.pid`, R3 `signal.send`, R4 the eight send-only names) are rulings owed, so a name `kill` calls may be re-spelled later |
| the 0.2.29 CHANGELOG's boreutils step | "the toolchain digests (remove the staged `.wolf-bin/std` before unpacking its own std pin, as at 0.2.27). `kill` can be written on `os_signal_send` and `os_signal_number`." `tools/fetch-toolchain` has removed the archive's `std/` since `f18bbe8` | holds; nothing to change in the tool |
| spec `[os.signal.set]`, `[os.signal.set.stable]`, `[os.signal.send]`, `[os.signal.number]` at `v0.2.29` (`spec/11-os.md`) | 28 meanings: 20 listenable (bits 0..19), 8 send-only (`KILL`, `STOP`, six faults). `os_signal_send(pid, meaning) -> () ! {denied, invalid, io, not_found, unsupported}`: **`pid` must be above 0** ("a group — `kill`'s 0 and negative ids — is job control's, the next lane's"), `meaning` 0 or exactly one bit; rows in the order shape, host, target. `os_signal_number(meaning) -> int ! {invalid, unsupported}`. `SIGPOLL` has no bit; real-time signals are out of scope. No prelude constant names a meaning. lupin serves `os_signal_number` and refuses `os_signal_send` by name (R9). The checked machine sends through the host | holds. **A process group cannot be expressed**; no open wolf-lang issue asks for a group send, a real-time signal, a host signal outside the 28, or a signal's description (`strsignal`): searched 2026-10-13 |
| bu22's report and harness | PR #29 read; `tools/roottest` (one fresh container a case, static programs copied in, GNU beside), the kasumi box (`localhost/px12-ubuntu`, Ubuntu 24.04, `--network none`, only the lane directory mounted), GNU 9.11 built in that image from the tarball by digest | holds. **Found while reading:** the oracle is configured `--disable-nls --without-selinux`, and GNU coreutils does not install its `kill` without `--enable-install-program=kill`: neither CI's `.gnu-bin/` nor bu22's build holds one, Homebrew's coreutils ships no `gkill` (nomad-1, 9.11: no such file), and Ubuntu's `/usr/bin/kill` is another package's. So `gnu-oracle.toml` must change, and every cached oracle rebuilds |
| boreutils#28 | OPEN. Its refusal needs a handle's open flags (wolf-lang#722, OPEN) and file identity off a handle (#536, OPEN). 0.2.29's prelude diff is five names, all signal and process-id | open; expected not to move (§3 line 9) |
| known: the checked machine refuses `<<` on a plain int | wolf-lang#736, OPEN | holds; no shift is written here (a meaning is a function call) |
| hosts | kasumi: 16 cores, `/home` 32 GB free (97 %), load 0.3 at the start, podman with `localhost/px12-ubuntu` and `docker.io/library/ubuntu:24.04` | holds |

## 3. Prediction (committed before GNU's `kill` is run and before the first change)

Each line names what is expected and what would falsify it. What GNU
does is predicted from its manual and POSIX, from memory, and is
exactly the part most likely to be wrong.

1. **The pin** (its own commit): wolf 0.2.29 / lupin 0.1.52 by the
   digests above; `[std]` to `9e5bd6b` (B151: `d7c2968` and `9e5bd6b`
   both build all 39 on both tiers under `--deny-warnings`). No W0304
   (no declaration of the five new names in `src/`), no new E1010. The
   verdict list at the pin is byte-identical to trunk's under the same
   harness in the same container. Every binary's bytes move (the
   runtime's signal table). Falsified by a diagnostic or one line of
   the list.
2. **The oracle** gains `--enable-install-program=kill`, and the
   harness asserts, for `kill`, that the binary it calls GNU's says
   `kill (GNU coreutils) 9.11`. Rebuilt with the flag, the oracle
   answers every existing case as before (the same tarball): the list
   does not move. Falsified by one line.
3. **GNU's `kill`**, as its documentation reads: `kill [-s SIGNAL |
   --signal SIGNAL | -SIGNAL] PID...` and `kill -l|--list|-t|--table
   [SIGNAL]...`. A SIGNAL is a name with or without `SIG`, a number, or
   (for `-l`) an exit status of a signalled process (`kill -l 137` is
   `KILL`). `kill -l` alone prints one name a line; `kill -l NAME`
   prints the number and `kill -l NUMBER` the name; `-t` prints number,
   name and the host's description. **`-L` is `-t`** (falsified if GNU
   refuses it). The default signal is `TERM`; signal `0` is taken and
   sends nothing. Status 0 when every signal was sent, 1 otherwise; a
   PID that fails is reported (`kill: PID: REASON`-shaped) and the rest
   are still tried. No PID is a usage error, status 1. Names are
   predicted to be accepted in lower case too. I do not know what GNU
   says for a signal name it does not know, for a PID that is not a
   number, or whether `-l` and a `-s` may be combined: measured, not
   predicted.
4. **`kill` ships** with `-s`, `--signal`, `-NAME`, `-NUMBER`, `-l`,
   `--list`, `-t`, `--table`, `-L` as measured, `--help`, `--version`:
   every one of wolf's 28 meanings by its POSIX name and by this host's
   number, signal 0, and GNU's message and status for a process that is
   not there (`not_found`), one this user may not signal (`denied`), a
   PID that is not a number and a signal nobody knows.
5. **What `kill` cannot do, each refused by name, status 1, nothing
   sent, and each a case the differential skips by name:**
   (a) **a process group**: the ids `0`, `-1` and any negative id
   (`os_signal_send` takes a pid above 0 only); (b) **a signal outside
   wolf's 28**: on linux the real-time range (`RTMIN` … `RTMAX`),
   `STKFLT`, `POLL`/`IO`, `PWR`; on macOS `EMT`, `INFO`, `IO` — by name
   or number, to send or to list; so (c) **`kill -l` and `kill -t` with
   no operand** print 28 lines where GNU prints every host signal (about
   62 on linux), and (d) **`-t`'s third column**, the host's description
   of a signal, has no builtin behind it (`os_error_text` is `strerror`,
   not `strsignal`). Each needs a wolf-lang issue that does not exist
   yet; the texts go to the orchestrator.
6. **The counts:** 39 utilities become **40**. About 150 cases that
   send nothing in `tests/cases/kill.toml` and about 50 that send, 0
   failed, under 25 skipped, every skip named. No verdict of the 39
   moves. Release and dev answer alike.
7. **The harness:** `tools/difftest` refuses any `kill` case that could
   send (it runs on hosts); the sending cases run from a new tool in
   bu21's `tools/roottest` shape, one fresh `--network none` container a
   case, static `kill` on both tiers beside GNU's, every target a
   process the case's own script started, how each target ended
   compared between GNU's side and ours. A plant in it must fail by
   name.
8. **The four machines:** native (dev) and release run every case.
   The checked machine (`wolf conform-run --json --checked`) answers the
   list rows as native does and sends through the host; lupin answers
   `os_signal_number` and refuses the send by name. Predicted: the
   checked machine and lupin cannot be handed an argv, so they are
   measured on a witness program, not on `kill` itself.
9. **boreutils#28 does not move**: 0.2.29 adds no builtin that reads a
   handle's open flags (#722) or its identity (#536).
10. **For PAX:** a static `kill` makes one system call beyond the
    start-up set and `write`: `kill`. `os_signal_number` is a table
    read, no call; no `rt_sigaction`, no `tgkill`, no futex, no thread.
    Falsified by any other name in the trace of a send.
11. **Planted breaks**, each red in CI on its named case and green after
    the revert: `-s NAME` sending `TERM` whatever was named; `-l NUMBER`
    answering the next signal's name; a failed send answering status 0.
12. **CI green** on ubuntu and macOS at the head. macOS parts from
    linux in numbers (`USR1` is 30 there) and in which signals exist,
    and nowhere else; a case written by NAME answers alike on both.
13. One thing here is wrong in a way this list does not name.

## 3a. The prediction, scored

§3 above is as it was committed (`429bcbb`, before GNU's `kill` was run
and before the first change). Scored in place, by line. "The box" is a
throwaway `localhost/px12-ubuntu` container on kasumi (Ubuntu 24.04), no
network, only `~/lanes/bu23` mounted, as uid 1000; "a fresh container"
is one `tools/killtest` or a probe made for one case and removed, with
nothing mounted but the GNU build, read-only. **GNU's `kill` in every
line is `~/lanes/bu23/gnu-build/out/bin/kill`** (sha256 `a78a3c72b1aa…`,
`kill (GNU coreutils) 9.11`), built in that image from the oracle
tarball (`394024ed…`, read twice) with `--enable-install-program=kill`.
The image's own `/usr/bin/kill` is procps-ng 4.0.4's and was never the
oracle; a shell's builtin was used only by the test scripts themselves,
on their own children.

| # | predicted | measured | verdict |
|---|---|---|---|
| 1 | the pin by digest; std to `9e5bd6b` after B151; no W0304, no E1010; the verdict list unmoved; every binary moves | digests as §2 (`ev/archives.log`); B151: `d7c2968` and `9e5bd6b` both build all 39 on both tiers with no diagnostic (`ev/b151.log`); the list is `637ee0857b4eaca9…` (5527 / 0 / 119, both tiers) at trunk on 0.2.28 and at the pin `d77ad3a` on 0.2.29 with std `9e5bd6b` (`ev/gauntlet-trunk-2ab3651.log`, `gauntlet-pin-d77ad3a.log`); 78 of 78 binaries differ | right |
| 2 | the oracle gains `--enable-install-program=kill`, `kill` is asserted by binary, and the rebuilt oracle moves no verdict | on linux, right: the trunk list above was taken against the rebuilt oracle and is bu22's. **On macOS, WRONG, and not in the way predicted**: CI's macOS leg had been using Homebrew's 9.11, and the first push made it use the build (Homebrew has no `gkill`); that build prints `\u0000` for `printf '\u0000'` where Homebrew's prints a NUL, and one `printf` case went red (run 38348626720). Fixed in `a6518a6`: a host of the right version keeps answering for what it holds and the build is staged for `kill` alone | right on linux, wrong on macOS |
| 3 | GNU's forms; `-L` is `-t`; default `TERM`; signal 0; status 1 and the rest still tried; lower-case names taken; three things not predicted | right on every line predicted, and `-L` is `-t`. **Not predicted** (`ev/probe1.log`, `probe-p2.log` … `probe-p4.log`): `-l` alone starts with `EXIT` and leaves out the unnamed 32 and 33; `-n SIGNAL` is `-s SIGNAL`, undocumented; a digit form (`-9`) is the signal ONLY as the first argument — later it is a process group, option reading stops there, and every operand before it is lost (`kill 123 -9` never touches 123); an upper-case first letter makes the whole argument a signal (`-Kill`), except `L`; a signal's first character inside a cluster is `invalid option -- K`, unquoted; a lower-case `-term` is a cluster; a number past the last signal is an exit status with a two-branch rule (past 255 the low eight bits, else the low seven: 393 is invalid, 65545 is `KILL`), measured for 0 to 700; `SIG9` is 9; an operand is quoted `'x'` with backslash escapes; a PID is `strtol`'s (blanks and one sign before, nothing after, a C `int`); a second signal is refused even when it is the same one; `cannot combine` is said only after every option is read | right, with twelve rules nobody predicted |
| 4 | `kill` ships the forms, the 28 signals, signal 0, GNU's messages for no such process, not permitted, a bad PID and a bad signal | shipped (`f88af66`, `b3947cf`); 270 forms that send nothing answer as GNU's but for the designed differences and a non-UTF-8 argument (`ev/ab1.log`), before any case file existed | right |
| 5 | refused by name: a group; a signal outside the 28; so 28-line tables; no description column | as predicted, and each is run: a group by `ours`/`expect` cases in fresh containers, the signals by `skip_on` and by `ours`/`expect`. The tables are 29 lines, not 28 (`EXIT`). **Not predicted:** `CLD` is a name only where the host's C library has it (linux), so it is gated on the build target; a failed send has two reasons with rows and no other (#682) | right, 29 for 28 |
| 6 | 40 utilities; ~150 cases that send nothing, ~50 that send, 0 failed, under 25 skipped; no verdict of the 39 moves; release = dev | **40**; **868** cases that send nothing (725 passed, 0 failed, 143 skipped on linux) and **335** that send (335 passed, 0 failed, 0 skipped); the 39's list is still `637ee0857b4eaca9…` with `kill`'s lines taken out; release and dev answer alike (`ev/gauntlet-w1.log`, list `4cca7ca46318f541…`, 6252 / 0 / 262). The skips are 142 cases that name a signal GNU has on linux and wolf has no meaning for, one a case (a number, a name, an exit status), and one non-UTF-8 argument (#406) | right on the rule, far low on the counts and wrong on the skips |
| 7 | `tools/difftest` refuses a sending case; a new tool in `tools/roottest`'s shape; a plant must fail by name | `5bf6a07` (the refusal, three plants under `tests/refuse/kill-*`; `gnu_keep`, with a plant and a control in `tests/selftest/echo.toml`; the oracle by binary), `8d3b064` (`tools/killtest`, `tools/killtest-selftest` with three plants, a control and a refusal). **Not predicted:** three sides in ONE container a case, not three containers | right |
| 8 | native and release run every case; checked and lupin measured on a witness, not on `kill` | the witness is the two unit-test files (`src/signals_test.lu`, `src/signals_send_test.lu`), each run as `wolf conform-run FILE --json --checked`, `--native`, `--release` and `lupin conform-run FILE --json` in the box (`ev/machines-w1.log`): the table and the operand readers are `exit(0)` on all four; the send rows are `exit(0)` on checked, native and release, and `unsupported` on lupin, by name (`os_signal_send` … this machine admits no `unsafe`) | right |
| 9 | boreutils#28 does not move | it does not: 0.2.29's prelude diff is the five signal and process-id names; wolf-lang#722 (a handle's open flags) and #536 are open | right |
| 10 | a static `kill` makes `kill` beyond the start-up set and `write`; no `rt_sigaction`, `tgkill`, futex or thread | `kill`, and nothing signal-shaped beside it: no `rt_sigaction`, `rt_sigprocmask`, `sigaltstack`, `tgkill`, futex, clone or pipe in any of fourteen traces (`ev/static.log`). **One call not named:** `statx(1, "", AT_EMPTY_PATH)`, `bore.stdout()`'s look at descriptor 1, in every trace | right but for `statx` |
| 11 | three plants red in CI | three breaks in two plant commits, because a red at the differential step ends the job before `tools/killtest` runs. `28f0b02` (`-l NUMBER` answers the next signal's name): red in run 38351505210 on both hosts at the differential step, ubuntu 6162 / 97 / 255 and macOS 6135 / 97 / 282, every one of the 97 a `kill` case, `kill: number: -l 9` among them — ours said `USR1` on linux and `BUS` on macOS, the next signal by each host's own numbering. `2763b25` (`-s` sends `TERM` whatever was named; a failed send leaves the status 0): red in run 38352429037 on both hosts at the killtest step, ubuntu 145 / 190 / 0 and macOS 92 / 185 / 58, `-s KILL` (`ended 143` where GNU's is `ended 137`) and `a process that has ended` (exit 0 where GNU's is 1) among them. Reverted in `64a321b` and `ab082b7`; the tree is `a6518a6`'s again. Both were red locally first (`ev/plant-local.log`) | right, in two runs |
| 12 | CI green on both hosts; macOS parts in numbers and in which signals exist, nowhere else | green at `a6518a6`, run 38349931313, all three jobs: ubuntu 6,259 / 0 / 255 (`kill` 725 / 0 / 143), roottest 178 / 0, killtest 335 / 0 / 0; macOS 6,232 / 0 / 282 (`kill` 846 / 0 / 22), killtest 277 / 0 / 58 (41 container cases and 17 that name linux's signals); the field leg as trunk's (5,413 passed and the same 31 differences, `kill`'s 868 skipped: the distro's `kill` is procps'). The 39's list on macOS is trunk's last run's, line for line (`a735613424de3cc4…`); ubuntu's differs in four lines that say which disk the runner had (`/dev/nvme0n1` or `/dev/sda`). **macOS parted as predicted — numbers, and which signals exist (22 skips for `EMT`, `IO`, `INFO` and `/dev/full` against linux's 143) — and in two ways not predicted:** `CLD` is no name there (gated before the first push, and CI agreed), and the oracle's BUILD (line 2). The first run, 38348626720 at `831989b`, was red on macOS on two cases that are not `kill`'s: that `printf` one, and boreutils#27's pty flake | right at the second run; wrong on where macOS parts |
| 13 | one thing wrong this list does not name | four. (a) **The harness read every target's fate through `$( )`**, where `wait` answers 127 for a process that is not the subshell's child: both sides agreed on `ended 127` whatever was sent, through the first run of 71 cases (`ev/killtest-t1.log` `fd5d2531f7aa`). Caught by the first case with a measured `expect` (`ended 162` for `RTMIN`), fixed before any count was taken, and gated since by `tools/killtest-selftest` (GNU's `KILL` must read 137). (b) A target that catches `CHLD` was ended by its own `sleep`'s exit; one case flaked once (`ev/killtest-full1.log`, 334 / 1), and such a target now spins. (c) `taskset -c 0-3 podman run` confines nothing: the container's `Cpus_allowed_list` is still 0-15 (`ev/taskset-check.log`), so the first "four-processor" run was not one (`ev/killtest-w1-taskset.log`, kept and named); `tools/killtest --cpus` asks from inside and asserts the list took. (d) line 2's macOS half | — |

## 4. Evidence index

Shas are this branch's (`bu23`). kasumi paths are under `~/lanes/bu23/`;
a digest's first twelve characters follow a log.

- **The prediction:** `429bcbb`. **The pin:** `2e58cef`, `d77ad3a`,
  `5c1c240`; `ev/archives.log` `9fcadf051748`, `ev/b151.log`
  `38170ece5f68`, `ev/gauntlet-trunk-2ab3651.log` `8dd32d91245e`,
  `ev/gauntlet-pin-d77ad3a.log` `324172943b8a`.
- **GNU's `kill`, measured:** `ev/gnu-ubuntu.log` `108afbe8f795` (the
  build, the binary's digest, `dpkg -S /usr/bin/kill` = procps);
  `ev/probe1.log` `f942c2a2458b` (173 forms that send nothing),
  `ev/probe-p2.log` `8de75a6c4863` (`-l N` for 0 to 700, every name
  sent to a `sleep` of the probe's own), `ev/probe-p3.log`
  `74491ea21605` (the digit rule, the order of refusals, PID syntax,
  `POSIXLY_CORRECT`, a closed output, not permitted, groups, `0` and
  `-1`), `ev/probe-p4.log` `3046668cbc52` (quoting). The scripts are
  `probes/p1.sh` … `p4.sh` there. Every probe ran as one fresh
  `--network none` container and signalled only processes it started.
- **The oracle:** `289c450`, `a6518a6` (`gnu-oracle.toml`'s
  `configure_args` and `needs`; `tools/fetch-oracle`).
- **The harness:** `5bf6a07`, `831989b` (`tools/difftest`: the refusal,
  `gnu_keep`, the oracle by binary), `8d3b064` (`tools/killtest`,
  `tools/killtest-selftest`, `tests/kill/selftest.toml`, `refuse.toml`).
- **`kill`:** `b3947cf` (`src/bore/signals.lu` and its two unit-test
  files), `f88af66` (`src/kill.lu`, `tests/cases/kill.toml`,
  `tests/kill/cases.toml`, the generator `notes/bu23/gen/kill_cases.py`).
- **The gauntlet at the code's head** (the tree of `831989b`; `a6518a6`
  changes how the oracle is found, and CI ran it) — `ev/gauntlet-w1.log`
  `40cd8e546dc9`: 40 built on both tiers, fmt, `wolf test` 4 of 4, the
  suite **6,252 passed, 0 failed, 262 skipped on release and on dev**,
  the same list `4cca7ca46318f541…`, the selftest, the evidence gate,
  the field-verdict selftest; `difftest-release-w1.log` `bef1a7dd7a47`,
  `difftest-dev-w1.log` `77f6ac020b34`. `kill`: 725 / 0 / 143.
- **`tools/killtest`**, podman, both tiers static (built in
  px12-ubuntu), GNU's own `kill` beside them:
  `ev/killtest-w1.log` `118c99d2a960`, **335 passed, 0 failed, 0
  skipped**; under four processors (`--cpus 0-3`, `Cpus_allowed_list
  0-3` read inside the container) `ev/killtest-w1-cpus4.log`
  `b6f2fb56e99c`, 335 / 0 / 0. `tools/killtest-selftest`:
  `ev/killself-w1.log` `c2f615e54ce8`.
- **SigBlk and SigIgn.** The kasumi jobs were started over ssh with
  `setsid nohup` and carry `SigIgn 0x7` (HUP, INT and QUIT ignored;
  `SigBlk 0`), printed at the top of each killtest log, and a container
  inherits that. So no target is a bare background job: each is started
  through GNU `env --default-signal`, and what GNU's `kill` itself does
  to one is recorded (`ev/record.log` `7488059223ae`, `tools/killtest
  --record`): `-s HUP` ends it with 129, `-s INT` 130, `-s QUIT` 131,
  `-s KILL` 137, `-s USR1` 138, `-s TERM` 143; `-s STOP` leaves it
  `stopped`; a caught `CHLD` or `CONT` ends it with 42.
- **The four machines:** `ev/machines-w1.log` `0f580a5e5eea` (§3a line 8).
- **The static binary for PAX** (`ev/static.log` `c09e8f15c51c`): kasumi
  `~/lanes/bu23/static/kill`, sha256 `4b24caa3354f1471cf3bd5a21694570e636ca1e4032eeef23093bf36015f341c`,
  13,570,888 bytes, `statically linked`, no INTERP, built in px12-ubuntu
  (gcc 13.3.0, glibc 2.39) by pax's recipe: wolf's release build through
  a `cc` that adds `-static`. Fourteen runs under `strace -f`:
  - every run: `execve`, `brk` ×5, `arch_prctl`, `set_tid_address`,
    `set_robust_list`, `rseq`, `prlimit64`, `readlinkat`
    (`/proc/self/exe`), `getrandom`, `mprotect`, `statx` (descriptor 1,
    `AT_EMPTY_PATH`), `exit_group`;
  - a run that prints (`-l`, `-t`, `--help`, a diagnostic): `write`,
    once;
  - a send: **`kill(PID, SIGNAL)`**, once a PID, with the HOST's number
    (`kill(86, SIGUSR1)`); signal 0 is `kill(PID, 0)`; a PID past every
    process is `kill(2147483647, SIGTERM) = -1 ESRCH`;
  - a refused group (`kill -- -5`) makes NO `kill` call;
  - nothing else: no `rt_sigaction`, `rt_sigprocmask`, `sigaltstack`,
    `tgkill`, `futex`, `clone`, `pipe` or `poll`, and no thread.
  **For a pax lane:** `kill` needs `kill(2)` for a positive pid with
  signal numbers in linux's numbering (1–31 less 16, 29, 30; 0 as the
  existence probe, `ESRCH` and `EPERM` as its two refusals), `statx` on
  descriptor 1 with `AT_EMPTY_PATH`, and `write`. Not run on PAX by this
  lane.
- **The plants:** locally `ev/plant-local.log` `7e9739b13f47`
  (`ev/plant1-difftest.log` `099559fdcac2`: 628 / 97 / 143, red on
  `kill: number: -l 9` and 96 more; `ev/plant2-killtest.log`
  `633743e91c1d`: 13 of 30 named cases red, `-s KILL` and `a process
  that has ended` among them). In CI: `28f0b02` red in run 38351505210 (the differential step, both hosts, 97 `kill` cases each), reverted in `64a321b`; `2763b25` red in run 38352429037 (the killtest step, both hosts: 190 cases on ubuntu, 185 on macOS), reverted in `ab082b7` (§3a line 11).
- **CI:** green at `a6518a6`, run 38349931313 (ubuntu, macOS, field; the counts are §3a line 12); the logs are on nomad-1 under `~/lanes/bu23/ci/`. Earlier: 38348626720 at `831989b`, ubuntu green and macOS red on `printf: \u for a NUL and DEL` (the oracle's build) and `ls: -l on a terminal quotes a name that needs it` (boreutils#27). The code at the head is `a6518a6`'s (`git diff a6518a6 ab082b7` is empty); the head's own run is named in the PR.

### What `kill` cannot do yet, and the wolf issue each needs

No issue was filed by this lane. Searched 2026-10-13: wolf-lang has no
open issue for any of the first three; the texts are for the
orchestrator.

1. **A signal to a process group** — *new issue*. `os_signal_send(pid,
   meaning)` answers `invalid` for a `pid` that is not above 0
   (`[os.signal.send]`: "a group … is job control's, the next lane's").
   Witness: `src/signals_send_test.lu` (`row(0, term)`, `row(-1, term)`,
   `row(-me, term)` are `invalid` on the checked machine, native and
   release). What waits on it: `kill 0`, `kill -- -PGID`, `kill -1`
   (refused by name here; 33 cases in `tests/kill/cases.toml` state GNU's
   answer beside ours); `timeout`'s kill of the command's group; pelt's
   `kill %job`. Asked for: a group send (`kill(2)`'s 0 and negative
   ids), by a call of its own or by the pid's sign.
2. **A signal the host has and wolf has no meaning for** — *new issue*.
   linux: `STKFLT` (16), `POLL`/`IO` (29), `PWR` (30), the real-time
   range 34–64 (`RTMIN`, `RTMIN+n`, `RTMAX-n`) and the unnamed 32 and
   33; macOS: `EMT` (7), `IO` (23), `INFO` (29). GNU's `kill` names and
   sends every one; this one says `invalid signal`, and `-l`/`-t` print
   29 lines where GNU prints 63 on linux. 142 differential cases are
   skipped on linux for it and 17 sending cases state both answers.
   There is also no way to ask the host its LAST signal number, so a
   number above it cannot be told from one wolf does not know. Asked
   for: meanings for the host-only signals and a real-time family, or a
   send by host number with the host's range.
3. **A signal's description in the host's words (`strsignal`)** — *new
   issue*. `kill -t`'s third column (`Killed`; `Killed: 9` on macOS),
   and what a shell prints when a job is ended by a signal.
   `os_error_text` gives an error number's words; nothing gives a
   signal's, and a table of one C library's words would be wrong on the
   other host. Asked for: `os_signal_text(meaning) -> str`.
4. **Why a send failed**, beyond `not_found` and `denied` — wolf-lang#682
   (open: the os family leaves no error number behind). A third reason
   is `io` and `kill` says "wolf does not say why".
5. **A non-UTF-8 argument** aborts the runtime in `env_args` —
   wolf-lang#406 (open). GNU says `kill: '\377': invalid signal`.

Depends on rulings owed elsewhere: `kill` calls `std.signal`'s 28 names
at wolf-std `9e5bd6b`, and sc60's spellings (`continued()`, the eight
send-only names) are not ruled yet.

Also for the orchestrator, **a boreutils issue, not filed**: the oracle
of record BUILT on macOS does not answer as Homebrew's 9.11 does —
`printf '\u0000\u007f|'` prints `\u0000`, then DEL, from the build, and
a NUL, then DEL, from Homebrew's (run 38348626720, the macOS job; this
lane's nomad-1 has Homebrew's 9.11, whose `gprintf` prints the NUL).
B44's cost (a) said the source-built path on macOS was untested; it is
tested now, and it parts in one `printf` case. The macOS leg will meet
it the day Homebrew ships 9.12. And **boreutils#27** (the macOS pty
flake) fired once more in that run: `ls: -l on a terminal quotes a name
that needs it`, our side's standard output empty.

## 5. Done-when

- [x] Branch `bu23`, PR wolffe-lang/boreutils#30, unmerged; five sections.
- [x] The pin, its own commits (`2e58cef`, `d77ad3a`, `5c1c240`); the archive's `std/` removed before the pin's own is staged (`tools/fetch-toolchain`, unchanged since `f18bbe8`).
- [x] `kill` on `os_signal_send` and `os_signal_number`: `-s NAME`, `--signal`, `-NAME`, `-NUMBER`, `-n`, `-l`, `-l NUMBER`, `-t` and `-L` as GNU has them, exit statuses, messages; differential against GNU coreutils 9.11's own `kill` on ubuntu and macOS, both tiers; every skip named.
- [x] A process group refused by name, with the wolf issue it needs; so too a signal with no meaning and `-t`'s description (§4).
- [x] Tests signal only processes they started, in fresh `--network none` containers on linux; on CI's macOS runner, which has no engine, on the runner itself.
- [x] A static `kill` and its system calls for PAX (§4).
- [x] Planted breaks red in CI (38351505210, 38352429037), reverted.
- [x] boreutils#28: unmoved by 0.2.29, and still open.
- [x] CI green at `a6518a6` (38349931313); the head's run and the audit's exit status are in the PR.
- Utility count: **40** of GNU's 103.
- No issue filed or closed. For the orchestrator: three wolf-lang issues to file (a group send; signals without a meaning; a signal's description), one boreutils issue (the oracle built on macOS and `printf '\u0000'`), one more sighting of boreutils#27.

