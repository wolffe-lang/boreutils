# bu25 — `cat`'s input-is-output refusal and the macOS tty flake

Lane note. **Class:** long (boreutils), **Opus**. **Crawl:** 54, batch 5.
Branch `bu25` off boreutils `23ea8dd` (bu24). Contract:
`sprints/boreutils/19-cat-and-difftest/bu25-cat-and-difftest.md`
(planning `ed700dc`). §1–§3 are committed before GNU has been run by
this lane on any shape below and before any line of `src/`, `tools/`,
`tests/` or CI changes; §3 is scored in place later, never rewritten.

Two issues. **boreutils#28**: `cat f >> f` copies until the disk is
full where GNU refuses with `cat: f: input file is output file`.
**boreutils#27**: a `tty` case of `tools/difftest` can read an empty
standard output on macOS.

## 1. Forbidden

- **No implementation's source is read**: not GNU coreutils', not any
  kernel's pty driver, not CPython's `pty` module beyond its documented
  interface. GNU's behaviour comes from `cat --help`, the info manual
  and black-box runs of the GNU coreutils 9.11 BINARIES built from the
  oracle tarball by digest; the pty's from runs on the hosts.
- **No disk is filled.** Every case that could grow without bound (our
  `cat` before the fix, any GNU utility GNU lets copy into itself) runs
  in a fresh `--network none` container on a size-limited tmpfs, under
  a `timeout`. Nothing of the host is mounted writable but the lane
  directory, and no unbounded case writes there.
- No `rm` outside `~/lanes/bu25/` (nomad-1 and kasumi); no `git add
  -A`; nothing under `~/.claude`; no merge, tag, or issue filed or
  closed; no attribution trailer; the branch asserted before every
  commit. No build on nomad-1. kasumi's login shell is fish (`bash
  -c`); `setsid` with a pid file; a job is killed by its recorded pid
  only. `/home` on kasumi is near full: prune as I go.
- Strict evidence (wolf-lang#571): `wolf build` exit 2 is a compile
  error; SKIP lines counted over the full output; no "seen red" without
  a run id. CI dispatches are one job at a time; no other lane's run is
  cancelled. Waits inline, printing at least every five minutes.

## 2. Inputs, verified (2026-10-17)

| input | origin says | verdict |
|---|---|---|
| boreutils trunk `23ea8dd` | `origin/trunk` `23ea8dd` (bu24); 46 utilities; 6,645 `[[case]]` tables; 0 open PRs; open issues #27, #28, #34 | holds. **Drift:** trunk's push run 38782212755 at `23ea8dd` is RED on macOS in `tools/killtest`, one case, `placing: {pid0} -l` (`kill -l` of a pid past 255 named `XCPU` by GNU) — boreutils#34, a pid-dependent flake, not this lane's |
| the pin | wolf 0.2.30 / lupin 0.1.53, std `fd6bcdc` (bu24) | holds; this lane moves no pin |
| wolf 0.2.30's file surface | `spec/11-os.md` at `v0.2.30^{}` = `1b37f368`: `fs_fstat(fd)` is `[kind, size, modified_ms]`; the full 20-word record with `dev`/`ino` is `fs_stat`/`fs_lstat` BY PATH only; "the handle form … for `cat`'s input-is-output check, #536's second half, stays `fs_fstat`'s three words"; no call reads a handle's open flags (wolf-lang#722, open) | the gap #28 waits on is still in the release |
| GNU 9.11 on linux | bu24's build, `~/lanes/bu24/gnu-build/out/` copied to `~/lanes/bu25/gnu/` (built in `localhost/px12-ubuntu` from tarball `394024ed…`, read twice, `ev/gnu-ubuntu.log` of bu24); `cat` `9b2ee4f7961e`, `tee` `ac2efcbd1c77`, `tac` `cf9ff3cf8b31`, `head` `9c5d82f27ff3`, `tail` `5652981b76f1`, `sort` `8b9fe9013653` (`ev/gnu-digests.log`) | holds |
| boreutils#27's witnesses | macOS legs only: runs 38124794804 (ours empty, 1 case), 38126188058 (GNU's empty twice, ours once, consecutive cases), 38348626720 (ours), 38355253341 (ours, trunk push); every one exit 0, stderr empty, stdout `b''`; 6 of 33 `tty` cases have been seen to lose, never on ubuntu | the shape #27 states |

Measured on nomad-1 before §3 (python, no build): on macOS
`stat("/dev/fd/1")` of a file opened by `>>` answers the file's `ino`,
size and times but a `dev` that is the descriptor file system's own
(`-962187075` beside the file's `16777232`), and a mode masked to the
open's access (`0o100200` for `>>`). An `O_APPEND` descriptor's offset
reads 0 on both hosts before the first write (`lseek(1, 0, SEEK_CUR)`).
On linux `/proc/self/fdinfo/1` says `flags: 0102001` for `>>`.

## 3. Prediction

**boreutils#28 — GNU 9.11, linux, in a container, root and a user
answering alike:**

1. `cat f >> f` (f not empty): `cat: f: input file is output file`,
   status 1, nothing written, f unchanged.
2. `cat < f >> f` and `cat - < f >> f`: the same with `-` as the name.
   `cat /dev/stdin < f >> f`: the same with `/dev/stdin` as the name.
3. A hard link or a symbolic link to f as the operand: refused, named
   as written.
4. `cat f > f` (the shell has emptied f): refused (the output's offset,
   0, is at the input's), status 1.
5. An empty f appended to itself (`cat e >> e`): refused.
6. `cat f 1<> f` (read-write, no append, both at 0): refused.
   `{ head -c 3 >/dev/null; cat; } < f 1<> f` (output BEHIND the
   input): allowed — the copy ends, the file's bytes shifted down 3.
7. Output a pipe, a terminal or `/dev/null`: allowed whatever the input.
8. `cat a f b >> f`: `a` and `b` copied, f refused, status 1.
9. `-n`, `-A` and the other options refuse alike.
10. **No other boreutils utility refuses**: `tee -a f < f` has no
    check (it copies until the tmpfs is full or the timeout), `tac`,
    `head`, `tail`, `sort -o f f`, `uniq f f`, `nl`, `cut`, `paste`,
    `tr` say nothing about it. The message is `cat`'s alone.
11. macOS's GNU (CI) answers 1–9 alike.

**The fix:** wolf 0.2.30 answers standard output's identity only
through a PATH: `fs_stat("/proc/self/fd/1")` on linux (the whole
record, `dev` and `ino` true), `fs_stat("/dev/fd/1")` on macOS (`ino`
true, `dev` not). The append flag is readable only on linux
(`/proc/self/fdinfo/1`). So: linux matches GNU on every shape in 1–9;
macOS matches on 1–5 and 7–9 by `ino` with size and times, and on 6's
"behind" shape refuses where GNU copies (an append and a read-write
descriptor are one thing to it), refused by name in the code with
wolf-lang#722 and #536. No new wolf issue is needed unless GNU's rule
turns out to need something neither names.

**boreutils#27:**

12. **Cause:** on macOS a pseudo-terminal whose last terminal-side
    descriptor closes discards (or stops answering) what is still
    buffered for the controller, so a child that writes and exits
    before the harness's first `read` leaves nothing; on linux the
    bytes stay readable until drained. Reproduced deterministically on
    CI's macOS runner by making the reader wait a few milliseconds
    after the child starts: with trunk's read, nearly every trial
    empty; with no wait, rare (under 1 in 500); on ubuntu, 0 at any
    wait.
13. **Fix:** the harness keeps its own copy of the terminal end open
    until the child has been waited for, reading while it runs, then
    drains what is buffered and only then closes. 0 losses in the
    probe with the wait, on both hosts; the 33 `tty` cases unchanged.
14. Green across repeated dispatches: at least five macOS dispatches of
    the suite at the head, every `tty` case passing in each.

**The counts:** 46 utilities, no new one. About 40 new `cat` cases
(container, root and user) and a probe gate; no verdict of the existing
6,645 moves. `cat` changes, so static `cat` for PAX's next pin is
rebuilt and its digest stated.

## 3a. The prediction, scored

§3 above is as it was committed (`da754cc`), before GNU was run by this
lane on any shape and before the first change. Scored in place, by line.
"A container" is a fresh `--network none` container of kasumi's
`localhost/px12-ubuntu` (podman) with a 16 MiB tmpfs at `/w` and nothing
of the host writable (`probes/cbox.sh`); "GNU" is `~/lanes/bu25/gnu/bin/`
(§2). Each probe ran as root and as `nobody` (65534), and the two logs
are identical but for the `id` line in every probe.

| # | predicted | measured | verdict |
|---|---|---|---|
| 1 | `cat f >> f`: refused, status 1, f unchanged | as predicted (`ev/probe-p1-gnu-root.log`) | right |
| 2 | `< f`, `-`, `/dev/stdin`: refused, named `-` / `/dev/stdin` | as predicted | right |
| 3 | a hard or symbolic link: refused, named as written | as predicted | right |
| 4 | `cat f > f`: refused | **copied** (nothing is: the shell emptied f), status 0 | **wrong** |
| 5 | an empty f appended to itself: refused | **copied**, status 0; and an input at or past its end with `>>` is copied too | **wrong** |
| 6 | `cat f 1<> f` (both at 0): refused; output behind: copied | both at 0 **copied**; behind copied; at an equal offset copied; output AHEAD by even one byte refused, and so is an output past an input already at its end (`1<>`, input 8, output 9) | wrong on the first half, right on the second. **The rule** (§ `bore.inout`'s header): with `>>`, refused while `size > in`; otherwise while `out > in`; and `out` counts what the program has already written (`cat a f 1<> f` and `cat -n a f 1<> f` refuse f: `ev/probe-p3-gnu-root.log`) |
| 7 | a pipe, a terminal or `/dev/null` out: allowed | pipe and `/dev/null` as predicted; the terminal was not probed (no container terminal) | right, one shape unmeasured |
| 8 | `cat a f b >> f`: a and b copied, f refused, status 1 | as predicted; `f f >> f` and `- - < f >> f` refuse twice | right |
| 9 | the options refuse alike | `-n -A -s -u -bETv`: as predicted | right |
| 10 | no other utility refuses; `tee -a f < f` copies until full | as predicted for GNU (`ev/probe-p2-gnu-root.log`: only `cp f f`'s own `are the same file`; `tee -a f < f` filled the 16 MiB tmpfs, status 1). **Not predicted:** on a file SMALLER than GNU's buffer, GNU's filters (`tail -c +1`, `nl`, `cut`, `tr`, `fold`, `expand`, `head -c`) read to the end before they write and stop after one pass, where ours write per chunk and fill the tmpfs; from about 5 KB up GNU fills it too (`ev/probe-p4-*.log`; `paste` the other way round at 5,714 bytes). Not a rule GNU has, so nothing was changed: a finding for the orchestrator (§5) | right on the rule, one buffering difference found |
| 11 | macOS's GNU answers alike | alike where the shape is alike, and one shape is not: macOS's `/dev/stdin` SHARES descriptor 0's offset where linux's opens afresh at 0, so `{ in_at 3; out_at 1; cat /dev/stdin; } < f 1<> f` is refused by GNU on linux and copied on macOS (CI run 39031596793) — the same rule meeting a different open | right on the rule |
| fix | linux: `/proc/self/fd/1` and `fdinfo`; macOS: `/dev/fd/1` by `ino` with size and times, append unknown, both halves; over-refusal only for a read-write output at or behind the input | as predicted. linux: `inouttest` 104 / 0 / 0 on both tiers, as root and as alice (kasumi and CI). macOS (CI): 52 cases as the runner's user, 7 of them by design (`darwin_refuses`): `1<>` both at 0 (operand and `-`), behind, equal, `f f` from 0, `- -` from 0, and #11's `/dev/stdin`. No wolf issue beyond #722 and #536 | right |
| 12 | cause: macOS's pty discards on the last terminal-side close; reproduced by a late reader; rare without | right, and more exact than predicted: the LAST close of the terminal end **blocks for 0.6 s** waiting for a reader and then discards; with the child gone, that last close was the harness's OWN, made before its first read — it waited on itself. Run 39026452370 (macos-latest, 3 cpus): trunk's reader 1 of 200 empty at no delay, 147–200 of 200 at 1–20 ms; every empty trial's first read was end of file with the child exited. Run 39029842340 adds the close's time: every empty trial's close took ≥ 0.1 s, no whole one did. Linux, kasumi under `taskset -c 0-3`: 0 of 1,600 lost at any delay (`ev/ttyprobe-linux-trunk.log`) | right, cause sharpened |
| 13 | fix: hold the terminal end, read while it runs, wait, drain, close | as predicted, plus the order that linux needs: read until the controller has been quiet 50 ms BEFORE closing (macOS), then read to the end AFTER closing (linux hands bytes over asynchronously). Run 39029842340: the fixed reader 2,400 of 2,400 whole on macOS; kasumi 1,600 of 1,600 (`ev/ttyprobe-linux-fixed.log`); `ls`'s 33 `tty` cases unchanged (692 / 0 / 18) | right |
| 14 | five or more macOS dispatches green | see §4 | — |
| counts | ~40 cat cases; no verdict of the 6,645 moves; `cat` rebuilt for PAX | **52** shapes × 2 actors = 104 container cases (`tests/inout/cases.toml`), 27 unit assertions (`src/inout_test.lu`); the difftest verdict list `4644afb15f38b6d3` (6,383 / 0 / 262, both tiers) is trunk's at `23ea8dd` and at this branch (`ev/gauntlet-*.log`); static `cat` digests in §4 | right, more cases |

## 4. Evidence index

Shas are this branch's (`bu25`). kasumi paths are under `~/lanes/bu25/`;
a log's sha256 prefix follows it. The probe scripts are
`notes/bu25/probes/` (run by `runp.sh` in `cbox.sh`'s containers). CI
logs are on nomad-1 under `~/lanes/bu25-ci/`.

- **The prediction:** `da754cc`.
- **#28:** `5eaa771` (`bore.inout`: the rule, the paths to a
  descriptor's identity, 27 unit assertions), `f138736` (`cat`),
  `2ccfd81` (`tools/inouttest`), `2407a01` (52 shapes), `a114238`
  (`tools/inouttest-selftest`), `ada9fc0` (CI), `d799f3a` (macOS's
  `/dev/stdin`, from run 39031596793).
- **#27:** `a713191` (`tools/ttyprobe`, committed and dispatched BEFORE
  the fix), `136aac5` (a dispatch names one job; `ttyprobe` and
  `macos-suite`), `a23d442` (the probe times the harness's own close),
  `37966bc` (the fix: `run_tty`), `456408e` (the gate on both hosts; an
  `inout` job for a plant).
- **Docs:** `45719bd` (CLAUDE.md), `8b2722e` (README's `cat` row).
- **GNU measured:** `ev/probe-p1-gnu-root.log` `601966f6a6e0` (42
  shapes), `probe-p3-gnu-root.log` `8f9fa39c159a` (the offsets, what
  was written, buffering), `probe-p2-gnu-root.log` `551364062d1d` (the
  other utilities), `probe-p4-gnu.log` `f3a4f2aaa2f2` (the filters at
  three sizes); ours: `probe-p1-w1*-*.log` (identical to GNU's but
  for `--help`'s text and `invalid option`'s argv0), `probe-p3-w1*`
  (identical), `probe-p4-w1rel.log` `2ec931a1eece`; trunk's `cat`:
  `probe-p1-trunk-*.log` (every refused shape filled the 16 MiB tmpfs).
- **inouttest on kasumi** (podman, `ubuntu:24.04`, static `cat` built in
  px12-ubuntu): `ev/inout-w1.log` `9cb317c72a73` 104 / 0 / 0;
  `ev/inout-trunk.log` `92eb5b896515` — trunk's `cat`, 30 of 52 root
  cases FAIL, every growing side stopped at 2 MiB by the file-size limit
  (status 153); `ev/inout-selftest-w1.log` `9c3446cafa98`.
- **No regression:** `ev/gauntlet-trunk-23ea8dd.log` `fd9fbba53df4` and
  `ev/gauntlet-w2-136aac5.log` `54437798c1f2`: 46 built on both tiers,
  0 diagnostics, verdict list `4644afb15f38b6d3` (6,383 / 0 / 262) on
  both tiers at both, selftest, evidence and field-verdict selftest 0.
- **The terminal read:** `ev/ttyprobe-linux-trunk.log` `4572c4897540`,
  `ev/ttyprobe-linux-fixed.log` `426645c444d0` (kasumi, `taskset -c
  0-3`, SigBlk 0, SigIgn 0); CI runs below.
- **Static `cat` for PAX** (px12-ubuntu, gcc's `-static`, at the head's
  `src/`, identical by checksum to kasumi's tree): release
  `1f00ef21b92277704045004df6bcf60b099da10fa637f9155a9c189a32ef0790`,
  dev `b9f8276ba5d0f3d3ed2006511f10f592a44c73f8e6e082bd44f967ce3ab303ed`
  (`~/lanes/bu25/bin/head/`, 13,952,560 B, `statically linked`, each read
  twice). `ev/strace-head.log` `13a423547e26`: beside trunk's calls, a
  regular standard output costs `statx("/proc/self/fd/1")`, `openat` +
  `read` of `/proc/self/fdinfo/1`, and per operand `statx(path)` and
  `statx("/proc/self/fd/1")`, plus `lseek(…, SEEK_CUR)` on the input and
  on 1 only when the two are one file. A pipe or terminal costs nothing
  new. **On PAX:** without `/proc/self/fd`, the check reads nothing and
  nothing is refused.

| CI | what | result |
|---|---|---|
| 39026452370 | `only: ttyprobe` at `136aac5`, the harness as trunk's | **red** (the gate: 394 of 800 lost; job 117378278115) — the reproduction |
| 39029842340 | `only: ttyprobe` at `456408e`, the fix | green: trunk's reader as before, the harness 2,400 / 2,400 whole |
| 39031596793 | PR at `456408e` | ubuntu green; macOS red on one `inouttest` case (#11 above), fixed in `d799f3a` |
| 39032969326 | PR at `d799f3a` | green on attempt 2: attempt 1's ubuntu `killtest` met `placing: {pid0} -l` (`KILL` against GNU's `FPE`, see §5) |
| 39036176027 | `only: inout` on `bu25-plant-cat` (`7b47330`, the refusal removed) | **red**: `inouttest-selftest`'s control `f >> f` FAIL as root and alice, release and dev exit 153 (the file-size limit) where GNU says `input file is output file` |

## 5. Findings, and what was not verified

**For the orchestrator (nothing filed or closed by this lane):**

- boreutils#28 and #27 close at merge, by hand.
- **The filters on a small file appended to itself** (§3a #10): GNU's
  `tail -c +1`, `nl`, `cut`, `tr`, `fold`, `expand` and `head -c` stop
  after one pass on a file smaller than their buffer (they read to the
  end before the first write); ours write per chunk and copy until the
  disk is full. Above about 5 KB GNU copies until full too. Not a
  refusal GNU has, so not changed here; a boreutils issue is owed if
  the small-file shape matters (`ev/probe-p4-*.log`).
- **killtest's `placing: {pid0} -l`** went red on UBUNTU in run
  39032969326 attempt 1 (`KILL` against GNU's `FPE`): `kill PID -l`
  names the signal for the target's PID, and each side starts its own
  target, so the two sides are asked about two different numbers.
  boreutils#34 reads it as a macOS fault; this sighting says the case
  itself is not deterministic on either host. Comment owed on #34.
- wolf-lang#722 (a descriptor's open flags) and #536's second half (a
  descriptor's identity) are what would let `cat` drop the `/proc` and
  `/dev/fd` paths and the macOS over-refusal; no new wolf issue.

**Not verified:**

- A terminal as `cat`'s standard output with its input the terminal
  device (§3a #7); a pipe and `/dev/null` were.
- `cat` on a linux with no `/proc` (PAX's case): reasoned from the
  code (every path stat fails, nothing is refused), not run.
- The `-E` carriage return held between operands (`pending_cr`): GNU's
  offset accounting for that one held byte was not probed.
- The input's record is read by path after the open; a rename between
  the two was not exercised.
- The macOS rule's identity words (`ino`, size, link count, owner,
  times) against a second file system with a colliding inode: not
  constructed.
- macOS's own GNU beyond CI's runner (Homebrew's or the source build
  CI made): no Mac but the runner ran the oracle.
