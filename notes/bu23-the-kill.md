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
