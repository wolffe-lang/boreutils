# bu27 — the groups (boreutils on wolf 0.2.32: the pin, `kill`'s groups, `timeout`)

Lane note. **Class:** long (boreutils), **Opus**. **Crawl:** 54, batch 7.
Branch `bu27` off boreutils `792ad31` (bu26). Contract:
`sprints/boreutils/21-the-groups/bu27-the-groups.md` (planning `0f647e5`).
§1–§3 are committed before this lane has run GNU's `kill` or `timeout` on
any case (only `timeout --help`, the documentation, was read) and before
any line of `src/`, `tools/`, `tests/`, CI or the pins changes; §3 is
scored in place later (§3a), never rewritten.

One deliverable, in order: boreutils pinned to wolf 0.2.32 / lupin 0.1.54
(its own commit) with the difftest of record on both tiers; then `kill`
reaching process groups (`kill -- -PGID`, `kill 0`, `kill -1`) through
`os_signal_send_group` / `os_signal_send_all`, and `-l` / `-L` through
`os_signal_last`, `os_signal_text` and `-N` where they change an answer;
then a new `timeout` (GNU coreutils 9.11's options and exit statuses, the
command in timeout's own group by `os_set_pgid(0)` unless `--foreground`,
the group send at expiry), each measured against GNU's own binaries in
throwaway `--network none` containers on both tiers, ubuntu and macOS
(macOS by CI); static binaries for PAX's next pin and their system calls.

## 1. Forbidden

- **No implementation's source is read**: not GNU coreutils', procps',
  util-linux's, busybox's, uutils', toybox's, nor any shell's `kill` or
  `timeout`. GNU's behaviour comes from `--help`, the info manual's
  `kill invocation` and `timeout invocation` nodes, POSIX.1-2024 `kill`,
  and black-box runs of the GNU coreutils 9.11 BINARIES built from the
  oracle tarball by digest (`kill` with `--enable-install-program=kill`).
- **A group send and `kill -1` run only inside a fresh `--network none`
  container or a process tree the test itself made.** `kill 0`, `kill
  -1` and every `kill -- -PGID` case is `container = true`; `timeout`
  sends to its OWN group, which holds only itself and the command the
  case started, and its cases run one fresh container a case on linux
  and, on CI's macOS runner (a throwaway machine with no engine), in a
  session the tool makes for the case. Never on a host's real process
  table: no case of either runs on kasumi, hasu or nomad-1 outside a
  container. A process is ended by its recorded pid only, never by name,
  pattern or group.
- Signal meanings are named through `std.signal`, never written as bits,
  and no host signal number is written: host-only signals are reached by
  `-N` from numbers the host answers (`os_signal_last`,
  `os_signal_realtime`).
- No regression in the 46 utilities' cases; if the pin regresses one,
  stop and report (bu26's rule), do not bump.
- No `rm` outside `~/lanes/bu27/` (nomad-1, kasumi) and this lane's
  clones; no deletion in a tree this lane did not make; no `git add -A`;
  nothing under `~/.claude`; no edit to another lane's file; no merge, no
  tag, no issue filed or closed; no attribution trailer; no `2>/dev/null`
  on a checkout; the branch asserted before every commit.
- Toolchains from the release archives by digest, each read twice. No
  build on nomad-1. kasumi's login shell is fish (`bash -c`); `setsid`
  with a pid file; `/home` there has 36 G free: one build tree, pruned
  as it goes, this lane's images removed at the end. Host ports 8080 and
  8088 never used.
- Strict evidence (wolf-lang#571): `wolf build` exit 2 is a compile
  error; SKIP lines counted over the full output; process and signal
  tests also run under `taskset -c 0-3` (asserted from inside the
  container); SigBlk and SigIgn read before a signal row is called red.
  No "seen red" without a run id. CI dispatches name one job; no other
  lane's run is cancelled. Waits are inline and print at least every five
  minutes. A harness refusal stops the lane and is reported.

## 2. Inputs, verified (2026-10-18, origin and the release archives)

| input | origin says | verdict |
|---|---|---|
| boreutils trunk `792ad31` | `origin/trunk` `792ad31` (bu26); 46 utilities; pin wolf 0.2.30 / lupin 0.1.53 / std `fd6bcdc`; killtest 338 cases (`tests/kill/cases.toml`), 33 of them `ours` group refusals; 0 open PRs; open issues #37 (owes a ruling, not this lane) and #39 | holds |
| wolf 0.2.32 is `v0.2.32` at `72de141f`; lupin 0.1.54 is `v0.1.54` at `0e536e8` | `git rev-parse v0.2.32^{commit}` = `72de141f6246…` (annotated tag object `d21c4b28`); `v0.1.54^{commit}` = `0e536e8fb451…` (tag object `9c98d445`) | holds |
| the release archives | release 416327027 (wolf, 2026-10-18 08:38Z) and 415937354 (lupin, 2026-10-17 16:48Z). Fetched on kasumi, each read twice, both reads equal to the API's digest (`~/lanes/bu27/ev/archives.log`): wolf linux x86-64 `4c37f9c5…` (80,092,071 B), linux arm64 `af27d426…`, macOS arm64 `061ea7e5…`; lupin linux x86-64 `175df238…`, linux arm64 `5fb15e31…`, macOS arm64 `9cd14db7…`. `_wolf` is `a368c8ec…` in all three wolf archives (one build). `wolf 0.2.32 (wolfgang, pin 72de141)` / `paired with lupin 0.1.54 (reference interpreter), pin 294d626`; `lupin 0.1.54 (wolf-interp, reference interpreter at pin 294d626)` | holds |
| the bundled std is wolf-std `d37c911` | `std/STD-REV` `d37c911f1220…` in all three wolf archives; wolf-std `origin/trunk` is `d37c911` (sc63; sc64 is running beside this lane and has not merged) | one candidate for `[std]` (B151: built under 0.2.32 before the pin) |
| the 0.2.32 CHANGELOG's boreutils line | "the toolchain digests, now unblocked … `792ad31`'s difftest against this release's candidate archive … passes 6383, fails 0, skips 262 on both tiers … Then `kill`'s groups and `timeout`, as 0.2.31's list says": `kill -- -PGID`, `kill 0`, `kill -1` through `os_signal_send_group`/`os_signal_send_all`; `-l`/`-L` through `os_signal_last`, `os_signal_text`, `-N`; `timeout` (`os_set_pgid(0)`, the group send). No new prelude names since 0.2.31; 0.2.31's seven (`os_signal_send_group`, `os_signal_send_all`, `os_set_pgid`, `os_signal_last`, `os_signal_realtime`, `os_signal_text`, `os_wait_poll`) are not declared in `src/` | holds |
| the crawl's "of record" | crawl-54 r37 STOP 2: boreutils `792ad31` difftest against the PUBLISHED 0.2.32, 6383/0/262 on both tiers | the number this lane must not do worse than; re-measured here (§3 line 1) |
| spec at `v0.2.32` (`spec/11-os.md`) | `[os.signal.send.group]`: `os_signal_send_group(pgid, m)`, `invalid` for a pgid not above **1** (group 1 cannot be named), rows as the host answers (`not_found` ESRCH, `denied` EPERM); `kill 0` is `send_group(os_pgid()?, m)` and reaches the caller. `[os.signal.send.all]`: `kill(-1)`, `not_found` when no other process exists (s241, as root in a namespace). `[os.signal.host]`: `-N` with `1 <= N <= os_signal_last()` on the sends and the text; `os_signal_realtime()` (34, 64) glibc, (0, 0) macOS. `[os.signal.text]`: `strsignal` in the C locale; macOS appends the number. `[os.term.group]`: `os_set_pgid(0)` moves the caller only; `denied` for a session leader. `[os.proc.job]`: `os_spawn_job(exe, args, map, group, tty, defaults)`; `[os.proc.poll]`: `os_wait_poll()` with `256 + N` for a stop. `[os.signal.disp]`: a listened meaning is the default in a child, an ignored one stays ignored. **Only the twenty listenable meanings can be ignored**: no call ignores `KILL`, `STOP`, the six faults or a host `-N` | holds. The last line matters to `timeout` (§3 line 12) |
| ruling #79 | R1 two builtins, `kill 0` = `send_group(os_pgid())`; R2 `os_set_pgid` on the caller; R3 host rows; R4 `-N`; R5 `os_signal_text`; R9 the order ending "boreutils' `kill` groups, then `timeout`" | holds |
| s241's report (crawl-54 2026-10-16) | `send_all` as root with nothing left answers `not_found`; podman `--init` leaves TSTP/TTIN/TTOU blocked | holds; no case here runs under `--init` |
| bu23's and bu26's reports, `tools/killtest`, `tools/killprobe` | read (`notes/bu23-the-kill.md`, `notes/bu26-the-kill-cases.md`). killprobe: 0 parted on both hosts at 0.2.30; by design linux 34,045 and macOS 2,803 numbers (the host-only and real-time signals); `-t` compared on its first two columns only | holds |
| boreutils#39 | OPEN: the `macos-suite` job counts reds under `bash -e`, so its count is always 0 | an input with no "not this lane"; one line (`set +e`), taken as its own commit |
| pax `notes/` | px38 traced Linux's answers to `kill(-1, 0)`, `kill(0, 0)` and `setpgid(0, 0)` (`notes/px38/linux/ct.txt`); px48 gave PAX groups and sessions: `setpgid`, `kill(0)`, `kill(-g)` (`notes/px48-job-control.md` §3). No note traces GNU `timeout` | holds: PAX can run a group-sending `kill` and a `timeout` that leads a group |
| hosts | kasumi: 16 cores, load 0.07, `/home` 36 G free (97 %), podman with `localhost/px12-ubuntu` and `docker.io/library/ubuntu:24.04`; bu26's GNU 9.11 build copied to `~/lanes/bu27/gnu/` (`timeout (GNU coreutils) 9.11`, dynamically linked for the container's glibc) | holds |

## 3. Prediction (committed before GNU's `kill` or `timeout` runs a case, and before the first change)

What GNU does is predicted from `--help`, the manual and memory, and is
the part most likely to be wrong.

**The pin (wolf 0.2.32 / lupin 0.1.54 / std `d37c911`).**

1. The difftest of record at the pin, in a throwaway px12-ubuntu
   container on kasumi, is **6383 / 0 / 262 on both tiers**, the verdict
   list trunk gives at 0.2.30 (bu26's `4644afb1…`): the five dev-tier
   `>&-` cases 0.2.31 failed pass again (#778). Falsified by any verdict
   that moves or any other count.
2. No W0304 under `--deny-warnings` (no prelude name since 0.2.31, and
   `src/` declares none of 0.2.31's seven); every binary differs from
   0.2.30's (the runtime archive moved); killtest 338 / 0 / 0, inouttest
   104 / 0 / 0 and idtest unchanged at the pin with `src/` untouched.

**`kill` reaches groups.**

3. GNU in a fresh container: `kill -- -PGID` (and `-s SIG -PGID`, `-N
   -PGID`) ends all three members of a group the case made and exits 0;
   a group that is not there is `kill: '-N': No such process`, status 1.
   `kill 0` from the case's script reaches the script's group, the
   targets and the `kill` itself: the targets end 143 and so does GNU's
   `kill` (its status read as 143). `kill -0 0` sends nothing, exit 0.
   `kill -- -1` as root in the container ends every target and spares
   the container's process 1, exit 0; with no other process it is
   `kill: '-1': No such process`, status 1.
4. After the change both tiers answer exactly as GNU on every one of
   those, so all 33 `ours` group refusals retire into GNU-compared cases
   and new cases are added for `kill 0`, `kill -1`, a group of another
   user's (EPERM), `-N` host signals to a group, and `-2147483648`.
   killtest at the head: **every case passes on ubuntu in containers, 0
   failed**, and on the macOS runner the `group = true` cases run too (in
   a session the tool makes), 0 failed.
5. `-l` and `-t` gain the host's whole numbering: on linux 64 signals
   (the real-time range named `RTMIN`, `RTMIN+1` … `RTMAX-1`, `RTMAX` as
   GNU names them from `os_signal_realtime`, 32 and 33 by number), on
   macOS 31; `STKFLT`, `POLL`/`IO`, `PWR` (linux) and `EMT`, `IO`, `INFO`
   (macOS) named. `-t` gains its third column, `os_signal_text`'s words,
   which are GNU's `strsignal` words on the same C library. killprobe
   (now comparing `-t`'s whole line) at the head: **0 parted and 0 by
   design on both hosts** over the same 240,578 numbers. Falsified by any
   number left by design or parted.

**`timeout`.**

6. GNU's statuses as its `--help` says: 124 when the command times out
   (TERM by default), 125 for a bad duration, signal, option or a missing
   operand, 126 for a command found but not runnable, 127 for one not
   found, and with `-s KILL` (or `-k` reaching KILL) **137, timeout
   itself ending by KILL** because the signal goes to its whole group.
   `--preserve-status` answers the command's own status, a death by TERM
   as 143. A command that ends by itself answers its own status, a death
   by a signal re-raised so timeout ends by the same signal.
7. Without `--foreground` timeout is the leader of a new group (its
   pgid is its pid) and at expiry its command's own children end too;
   with `--foreground` it stays in its parent's group and a command's
   child that ignores nothing outlives the expiry.
8. A signal sent to timeout itself (TERM, INT, HUP, QUIT) is passed to
   the command, and timeout answers as the command ended; an ALRM sent to
   timeout is read as the expiry (124).
9. A stopped command is continued after the expiry's signal, so `timeout
   1 sh -c 'kill -STOP $$'` ends 124 at about one second.
10. Ours answers GNU's exit status, standard output and standard error,
    and the fates of the command's children, **on every case on both
    tiers**, in containers on ubuntu (also under `taskset -c 0-3`) and on
    the macOS runner, about 100 cases, 0 failed; each case's elapsed time
    within 0.3 s of GNU's.
11. Idle, our timeout makes no polling wake-ups: 0 to 2 voluntary
    context switches a second while it waits (read from
    `/proc/<pid>/status`), as GNU's.
12. The one difference by design: wolf cannot IGNORE a send-only meaning
    (the six faults) or a host `-N` signal, and timeout must not be ended
    by its own group send. So `-s SEGV` (or `-s RTMIN`) without
    `--foreground` is refused by name, status 125, where GNU sends it and
    answers 124. Falsified if GNU itself does not survive such a send, or
    if a send to the group can be made without reaching timeout.

**For PAX.**

13. Static `kill` and `timeout`, both tiers. `kill`'s calls past bu23's
    (`kill` per pid, `statx` on fd 1): `kill(-PGID)`, `kill(0)` after
    `getpgid`/`getpgrp`, `kill(-1)`. `timeout`'s: `setpgid(0, 0)`,
    `rt_sigaction` and `rt_sigprocmask` for its listen, the hub's
    `pipe2` and thread (`clone3`), a spawn (`clone`/`vfork` or `fork`
    then `execve` in the child), `wait4` with `WNOHANG`, the timer as a
    thread's `clock_nanosleep`, `kill(0 or -pgid, SIG)`, `exit_group`.

**Plants.** A: `kill`'s group refusal put back; the group cases go red.
B: `timeout` without `os_set_pgid(0)` and sending to the command alone;
the cases about the command's children go red. Each is a branch, red in
a one-job CI dispatch.
