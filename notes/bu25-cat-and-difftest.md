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
