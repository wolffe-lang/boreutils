# bu20 — the long format (boreutils at wolf 0.2.27 / lupin 0.1.50)

Lane note. **Class:** long (boreutils), **Opus**. **Wave:** 53. Branch
`bu20` off boreutils `5da892e`. §1–§3 are committed before any 0.2.27 or
0.1.50 archive is fetched or unpacked; §3 is scored in place later, never
rewritten.

One deliverable: the pin at wolf 0.2.27 / lupin 0.1.50 by digest; then
`ls -l` and its family (`-s -u -c -i -n -g -o`, `-F`/`-p` on links,
`-L`/`-H`, the unsorted `-f`/`-U`); then `stat`, `readlink` and `env`,
each measured against GNU 9.11.

## 1. Forbidden

No `rm` outside `~/lanes/bu20/` (nomad-1 and kasumi) and this lane's own
private clones; no deletion in any tree this lane did not create; no
`git add -A`; nothing under `~/.claude`; no edit to another lane's file;
no merge, no tag, no attribution trailer; no `2>/dev/null` on a checkout.
The pin from the RELEASE ARCHIVES by digest, never a clone, Homebrew or
`~/.local/bin`. No build on nomad-1: every build, difftest and bench runs
on kasumi with `CARGO_INCREMENTAL=0`, one tree, pruned as it goes; no
scratch in `/tmp` on any host. No "seen red" without a run id, sha, path
or digest. Strict evidence (wolf-lang#571): counts are read from the full
output, SKIP counted; a `wolf build` that exits 2 is a compile error,
never a skip; `env`'s exec rows are also run under `taskset -c 0-3`. No
package is installed anywhere. At most two CI runs of this lane at once;
no other lane's run is cancelled. **GNU coreutils source is never read**,
nor busybox's nor any other implementation's source for this lane: GNU's
behaviour comes from its documentation, POSIX.1-2024 and black-box runs
of the staged 9.11 oracle (`tools/fetch-oracle`).

## 2. Inputs, verified (2026-10-11, release API and origin)

| input | origin says | verdict |
|---|---|---|
| wolf 0.2.27 = wolf-lang `0ddda6b7`; linux x86-64 `5e17eebe…`, linux aarch64 `c475e5dc…`, macOS arm64 `ea461a76…`, windows `ac784416…` | release `v0.2.27`, published 2026-10-11 04:12Z; tag object `d5f9597a` → `0ddda6b7ab9f`; the four asset digests are `5e17eebed7ff…`, `c475e5dc0a37…`, `ea461a7668d9…`, `ac78441650a6…` | holds |
| lupin 0.1.50 = wolf-interp `32b970d`; linux x86-64 `e2867a35…`, aarch64 `a0c0c707…`, macOS `2cbd192d…`, windows zip `420e02c0…`, `lupin.exe` `b37b13bf…` | release `v0.1.50`, published 00:53Z; tag object `b30a6d16` → `32b970da7f3a`; all five digests match | holds |
| boreutils trunk `5da892e` (bu19), pinned 0.2.26 / 0.1.49 | the same; std `0f74ec5`; trunk CI run 37996012670 green | holds |
| 0.2.27's "Read this before you bump the pin" | read in full at the tag (CHANGELOG lines 23–192, and s218's, s220's and s225's sections). The archive carries `std/` (wolf-std `87ba162`) with `std/STD-REV`; seventeen new prelude names; every hosted binary's bytes move because `libwolf_rt.a` did; the bundled std has one stale json row | holds |
| seventeen new prelude names | a grep of `src/` for a declaration (`fn`, `let`, `var`, `const`, `type`, `struct`, `enum`) of any of the seventeen finds none | no W0304 expected |
| wolf-lang#660, #665 (two soundness holes shared with 0.2.26) | `src/` has 24 `in NAME { … }` blocks in eleven files (`cut` 2, `fold` 1, `head` 4, `nl` 3, `paste` 2, `sort` 1, `tac` 1, `tail` 4, `uniq` 5, `bore/sink` 1) and no channel, `spawn` or `send` anywhere. Thirteen of the blocks call nothing (they push or store a `byte`); the other eleven call `bore.ring_push(mut r, b)` with `b` a `byte` and `bore.ring_drop(mut r, n)` with `n` an `int`. #660 needs a callee handed a STRING built in the enclosing region block beside a `mut` argument that outlives it; every argument here is a scalar, which is the shape the release notes say to use until the fix. (This row first said three blocks, from a truncated grep; corrected before any archive was fetched.) Re-checked against the staged compiler after the pin (§3 line 6) | neither shape is in the tree |
| s218's surface (wolf-lang #637, spec `[os.fs.stat]`, `[os.fs.readlink]`, `[os.fs.readdir]`) | `fs_stat`/`fs_lstat` answer twenty words: kind (0 file, 1 directory, 2 other, 3 link, 4 fifo, 5 socket, 6 character device, 7 block device), size, modified_ms, a `have` mask, mode (`& 0o7777`), nlink, uid, gid, blocks (512-byte units), dev, ino, rdev, and atime, mtime, ctime, btime each as seconds and nanoseconds. `fs_read_link` answers the target's bytes; `fs_read_dir_entries` answers the host's order, a kind byte then the name's bytes. **Not there:** the preferred I/O block size (`st_blksize`), any extended attribute (so no ACL or security-context mark), the file-system record (`statfs`), a record from an open handle past `fs_fstat`'s three words, a byte-path spelling (a name that is not UTF-8 is listable, not stat'able), and owner and group NAMES | holds; the gaps are named in §3 and filed where no issue exists |
| s225's surface (wolf-lang #651, `[os.proc.exec]`, `[os.env.unset]`) | `os_exec(exe, argv, env, map) -> () ! {denied, invalid, io, not_found, unsupported}`, a bare name searched along the handed environment's `PATH` else `/usr/bin:/bin`, no `/bin/sh` retry on `ENOEXEC`; `env_unset(name) -> () ! {invalid}` | holds |
| wolf-lang#625, #626 | **both still OPEN** on origin though s218 merged as `76436101` and 0.2.27 ships it. #536 is open by design (its handle half). #534 is closed | drift, reported; this lane closes nothing |
| the std wrappers (wolf-std #57, #60) | both open; wolf-std trunk is `87ba162`, the commit the archive bundles | the builtins are called directly |
| terminal width | wolf-lang#643 open | `ls` on a terminal keeps `-w`, `COLUMNS`, 80 |
| the oracle | GNU coreutils 9.11 by digest (`gnu-oracle.toml`), `LC_ALL=C`, `_POSIX2_VERSION=200112`; kasumi's own GNU is 9.12, so every kasumi run stages the oracle | holds |

## 3. Prediction (committed before the archives are fetched)

Each line names what moves and the observation that falsifies it.

### The pin

1. All 28 utilities build on both tiers under 0.2.27 with
   `--deny-warnings`, no diagnostic. Falsified by one error, warning or
   refusal.
2. `tools/fetch-toolchain` copies the whole archive into `.wolf-bin/`
   and then unpacks its std pin over it, so at this pin it must remove
   `.wolf-bin/std` first. The archive's `std/` is wolf-std `87ba162`'s
   `std/` tree byte for byte, and its `STD-REV` names that commit.
   Falsified by a `diff -r` line. The repository's std pin moves
   `0f74ec5` → `87ba162` (B151: both candidates built first).
3. `--emit=wir` is byte-identical for all 28 at the old std pin, and for
   all 28 at `87ba162` too (the std files that moved — `process`, `env`'s
   cwd, `io`, `map` — add functions no utility calls). Falsified by one
   differing file; if `std.env`'s new functions are emitted unreferenced,
   the 28 that import `bore` all move and this line is wrong.
4. Every binary differs raw and stripped on both tiers, because
   `libwolf_rt.a` did (s222's arena, s224's json kernel, s225's exec
   module). The instruction and load counts inside each program's own
   `_W*` functions are identical. Falsified by a count that moves.
5. The verdict list at the pin commit is byte-identical to trunk's:
   3017 passed / 0 failed / 60 skipped on kasumi against the staged
   9.11, release and dev. Falsified by one line.
6. Neither #660's nor #665's shape is in `src/` (§2). Falsified by a
   site.
7. Bench (ls rows only, one hyperfine call with GNU beside both states):
   plain `ls` and `ls -C` at 100,000 names 0–15% faster than at 0.2.26
   (s222: the root arena takes no lock per allocation, and `ls`
   allocates a `str` per name); falsified outside −5%…+20%. `-S`, `-t`
   within ±5%.

### `ls`

8. Served and byte-identical to GNU 9.11 with standard output a pipe,
   `LC_ALL=C`, `TZ=UTC0`: `-l`, `-n`, `-g`, `-o`, `-G` with `-l`,
   `--full-time`, `-s` (alone and with every format), `-i`, `-u`, `-c`,
   `--time=atime|access|use|ctime|status|birth|creation`, `-U`,
   `--sort=none`, `-f`, `-h`/`--si`/`-k` on the sizes `-l` and `-s`
   print, `-F`/`-p`/`--file-type`/`--indicator-style` with every mark
   (`/ @ * = |`), `-L`, `-H`,
   `--dereference-command-line-symlink-to-dir`, on every file type
   kasumi can make without privilege: regular, directory, link, dangling
   link, fifo, socket, the character and block devices `/dev` already
   holds, setuid, setgid, sticky (with and without the execute bit under
   them), and hard links.
9. The `total` line, every column width, the two time formats on both
   sides of the six-month rule, and a time in the future, are
   byte-identical. The harness cannot fix the clock for a native
   binary without a tool nobody may install, so the six-month cases set
   times RELATIVE to one instant taken once per case (both sides see
   the same age to the second); the ages straddle the boundary by a
   minute each way. Falsified by one FAIL.
10. Of bu18's 30 `ls` skips: the 24 naming #625 and the 1 naming #536
    become ordinary cases and pass; the 3 naming #626 pass (unsorted
    order compared as a set by the harness, since the order is the
    host's and GNU sorts nothing either — both sides read one directory,
    so the bytes are expected equal on one filesystem; if they are not,
    that is a finding); the 2 naming #643 stay skipped. Falsified by a
    different count.
11. New `ls` cases: at least 250, and the corpus total passes 3,400.
    Expected skips, each by named cause: the terminal's width (#643, 2);
    a name that is not UTF-8 under any format that needs a stat (ruling
    #60: listable, not stat'able; GNU prints the row, this `ls` prints
    GNU's `?` row and a diagnostic GNU does not); owner and group NAMES
    on macOS, where accounts are not in `/etc/passwd` (the cases run
    with `-n` there and by name on linux).
12. Remaining refusals, each by name with its issue or "not written
    yet": the ACL and security-context marks after the mode (`+`, `.`:
    no extended-attribute call, to be filed), `--author`, `-Z`,
    `--time-style` other than what `--full-time` implies,
    `--block-size`, `-v`, `--sort=width`, the quoting styles but `-N`,
    `-I --ignore --hide -B`, `-D`, `--color=always`, `--hyperlink`,
    `--zero`.
13. Owner and group names come from `/etc/passwd` and `/etc/group`,
    read once and only when a long listing meets an id; an id with no
    line prints as its number, as GNU's does. What that misses is NAMED:
    any name service that is not those two files (LDAP, systemd's
    dynamic users, macOS's directory service). Time zones come from the
    TZif file `TZ` names (or `/etc/localtime`), read in wolf, footer rule
    included; a `TZ` this reader cannot serve prints UTC and is listed.
    Falsified for the oracle host by one FAIL among the `TZ=` cases.

### `stat`, `readlink`, `env`

14. `stat`: `-c`/`--format`, `--printf`, `-L`, `-t` and the default
    format pass for every file type above, for the directives
    `%a %A %b %B %d %D %f %F %g %G %h %i %n %N %s %t %T %u %U %w %W %x
    %X %y %Y %z %Z %r %R %Hd %Ld %Hr %Lr` with GNU's flags, width and
    precision. **Differs, by named cause:** `%o` and the default
    format's `IO Block:` (the record has no `st_blksize`: printed `?`,
    filed upstream; the default-format cases compare everything else
    through a mask the harness applies to both sides); `%m` (mount
    point) and `%C` are refused. `-f`/`--file-system` is refused by
    name (no `statfs`, filed). At least 120 cases.
15. `readlink`: no option, `-n`, `-z`, `-f`, `-e`, `-m`, `-v`/`-q`/`-s`,
    several operands, every failure's status and message. At least 60
    cases, 0 skips.
16. `env`: `-i`, `-`, `-u`, `NAME=VALUE`, `-C`, `-0`, `-a`, `--`, exit
    125 (its own failure), 126 (found, cannot run), 127 (not found),
    and the command's own status. It replaces the process (`os_exec`).
    At least 70 cases. **Differs, by named cause:** the whole
    environment printed without `-i` is in `env_vars()`'s sorted order
    and drops an entry that is not UTF-8 (wolf-lang#535: skipped, as
    `printenv`'s four are); a file with no `#!` line is not re-run under
    `/bin/sh` (`[os.proc.exec]`: GNU's `execvp` does; status 126 here
    against GNU's 0) unless `os_error` lets `env` tell `ENOEXEC` apart,
    in which case it retries as `execvp` does. `-S`, the signal options
    and `-v` are refused by name.

### The bench, the binaries, CI

17. `ls -l` at 100,000 names in one directory on kasumi, release,
    against GNU 9.11: **0.5–0.9x GNU's speed**. The floor is one
    `statx` per name on both sides (`strace -c` counted, expected
    100,000 ± a handful each); what this `ls` adds is a 20-word list
    and a `str` path per name. Falsified outside 0.3x–1.0x. `stat` on
    one file and `readlink` on one link start within 1.5x of GNU either
    way; `env true` within 2x.
18. Static linux builds of `ls`, `stat`, `readlink` and `env` make no
    system call outside: `execve`, `brk`, `mmap`, `munmap`, `mprotect`,
    `arch_prctl`, `set_tid_address`, `set_robust_list`, `rseq`,
    `prlimit64`, `getrandom`, `rt_sigaction`, `rt_sigprocmask`,
    `sigaltstack`, `poll`, `openat`, `read`, `pread64`, `write`,
    `close`, `fstat`/`newfstatat`/`statx`, `getdents64`, `readlink`/
    `readlinkat`, `ioctl` (the terminal question), `getcwd`, `chdir`,
    `lseek`, `clock_gettime`, `futex`, `sched_getaffinity`,
    `exit_group`. Falsified by a name not on this list.
19. CI green on ubuntu and macOS at the head; the field leg (ubuntu's
    own GNU 9.4) reports new divergences in the long format, which are
    information.
20. One thing here is wrong in a way this list does not name.

## 3a. The prediction, scored

§3 above is as it was committed (`0029738`, corrected for the `in` block
census in `f054aaf`, both before any archive was fetched). Scored in
place, by line.

| # | predicted | measured | verdict |
|---|---|---|---|
| 1 | all 28 build on both tiers, no diagnostic | errors 0, warnings 0, built 28 on release and dev at the pin `bdae32b` (`gauntlet-pin-bdae32b.log`) | right |
| 2 | the archive's `std/` is wolf-std `87ba162`'s tree byte for byte; `fetch-toolchain` must remove it first | the 52 source files are identical in all three archives and `STD-REV` names `87ba162`; the archive's copy ALSO holds `LICENSE` and `LICENSE-EXCEPTION`, which the tree's `std/` does not (`archives.log`). The removal is `f18bbe8` | wrong in the letter (two files more), right in what it was for |
| 3 | `--emit=wir` identical for all 28 at both std pins | identical in all 28 at `0f74ec5`; at `87ba162` all 28 gain 71 or 72 lines and lose none: `std.env.cwd` and `set_cwd` emitted unreferenced | half right; the hedge named the cause |
| 4 | every binary differs raw and stripped; own-code counts identical | 28 of 28 differ both ways on both tiers. Own code: release, 27 identical and `head` 6074 → 6062 instructions; dev, two more functions in every binary (line 3's) | wrong on the counts |
| 5 | the verdict list at the pin is trunk's | `591bf0fc…` at base `f054aaf` and at the pin, release and dev, 3017 / 0 / 60 | right |
| 6 | neither #660's nor #665's shape in `src/` | 24 `in` blocks, every call inside one handed a `byte` or an `int`; no channel, `spawn` or `send`. A source census: the compiler has no check for either, which is the bug | right, as far as a census reaches |
| 7 | plain `ls` and `-C` 0–15% faster at the pin, falsified outside −5%…+20%; `-S`, `-t` within ±5% | at 100,000 names, pin against base: plain 38.4 against 38.2 ms (−0.5%), `-C` +3.5%, `-t` −3.4%, `-S` +6.8% with σ 9.2 and 4.3 ms on the two sides (`bench.log`; load 2.3 rising to 8) | in the band for three rows and not a speed-up; `-S` is outside ±5% by less than its own σ: not resolved at that load |
| 8 | the long format, `-s -i -u -c --time -U -f`, `-h --si -k`, every mark, `-L -H` byte-identical on every kind a user can make | 418 new cases, 0 failed on kasumi (btrfs) and on CI's ubuntu (ext4) and macOS. **Except `-f` and `-aU`:** on ext4 `.` and `..` are not first in the directory's own order, and `fs_read_dir_entries` leaves them out (wolf-lang#692): six cases skipped by name | right but for `-f` under `-a` |
| 9 | `total`, every width, both sides of the six-month rule, a future time | the nine `ages` cases pass on both hosts, and the plant below turns seven of them red and leaves the two that do not use the rule green | right |
| 10 | of bu18's 30 skips, 28 become cases and pass; the 2 for #643 stay | 27 pass; `-f` is skipped again under #692 (line 8); the 2 for #643 stay | wrong by one |
| 11 | at least 250 new `ls` cases, the corpus past 3,400; a name that is not UTF-8 listed byte-identically where no stat is needed | 418 new; 3,855 in the corpus. A name that is not UTF-8 is NOT listed in any format: this program's names are `str`s end to end, so it is reported and skipped, status 1 (wolf-lang#687). No case holds one: a TOML string cannot spell the name | right on the counts, wrong on the name |
| 12 | the refusals named | as named, less `--time-style`: `full-iso`, `long-iso`, `iso` and `locale` are served (with `TIME_STYLE`), only `+FORMAT` is refused | better than predicted |
| 13 | names from the two files; zones from TZif and its rule | 31 `TZ=` cases pass on kasumi and ubuntu, a rule in Julian days and Dublin's negative daylight time among them | right on linux; macOS in §4 |
| 14 | `stat`: the default and terse formats and thirty-odd directives; `%o` printed `?` behind a mask; `%m` and `%C` and `-f` refused; at least 120 cases | 160 cases, 152 pass and 8 skip on kasumi. `%m` is SERVED (the walk `readlink -f` needed serves it). **Not predicted:** `-` is refused too, because `fs_fstat` answers three words (wolf-lang#536's other half) | right, with one refusal I did not see coming and one I did not need |
| 15 | `readlink`: at least 60 cases, no skip | 97, none skipped | right |
| 16 | `env`: at least 70 cases; a file with no `#!` line 126 unless `os_error` tells `ENOEXEC` apart | 103 cases, 90 pass and 13 skip. `os_error` does not tell (the os family leaves no number, wolf-lang#682); `env` reads the file's first four bytes itself and re-runs it under `/bin/sh` as GNU's `execvp` does, and the three cases pass. **Not predicted:** `=VALUE` (an empty name) is refused by `os_exec`, and an empty `PATH` component runs `./name` where `execvp` runs `name` (wolf-lang#689) | right on the count; two partings I did not predict |
| 17 | `ls -l` at 100,000 names 0.5–0.9x GNU, falsified outside 0.3x–1.0x; one `statx` a name on both sides; `stat` and `readlink` start within 1.5x, `env true` within 2x | **1.22x** at the head (196.5 against 239.7 ms). The first cut was 0.70x and in the band (`bench-first-cut.log`); after the records moved to one flat list it is past it — and GNU makes a second call per name, 99,998 `llistxattr`, that this `ls` cannot make (wolf-lang#685). `statx`: 99,998 GNU, 100,003 here. Start-up: `stat` 1.29x, `readlink` 1.30x, `env true` 1.29x slower | wrong on `ls -l`, in the direction nobody complains about and for a reason that is partly a missing feature; right on the floor and the start-ups |
| 18 | the static binaries make no system call outside the list | every name each makes is on it (§4); none of `rt_sigaction`, `sigaltstack`, `poll`, `futex`, `lseek`, `clock_gettime` or `sched_getaffinity` was made at all | right |
| 19 | CI green on both hosts; the field leg reports new divergences in the long format | green (§4). The field's 9.4 differs on ten new cases and none is the long format: `env -a` (four; 9.4 has no `-a`), `ls --sort=name` and `--time=mtime` (four), `readlink` under `POSIXLY_CORRECT` (two). Each names 9.11 now, and the field leg is back at trunk's fifteen | right on green, wrong on where |
| 20 | one thing here is wrong in a way this list does not name | four. (a) The first `ls` was 34% SLOWER than trunk on a plain listing and half its speed under `-S` (`bench-first-cut.log`): a listing that needs records is read in the directory's own order, so the sort does every comparison, and each reached through two 150-byte entries. (b) CI's ext4 holds no time past 2446 or before 1901 and no file past 16 TiB, and the harness died on each (runs 38113933764, 38114708822) — with status 1, which is its word for "a case differs", so the field leg read a dead harness as an advisory. It exits 2 now (`83b64e0`). (c) An `0o…` literal compiles under `wolf test` and not under `wolf build` (wolf-lang#688), so a green unit test said nothing about the program. (d) I wrote, and committed, that reading a field of a list's element copies the element — a guess from a profile. A witness said no (kasumi `~/lanes/bu20/wit/copy/`: two million reads in 1 ms either way), and `fff90ae` says what was measured | — |

## 4. Evidence index

Shas are this branch's (`bu20`, wolffe-lang/boreutils). kasumi paths are
under `~/lanes/bu20/ev/` and stay there; a digest's first twelve
characters follow each.

### Archives and the pin

- `archives.log` (`abe314fa8427…`): the six archives fetched and hashed,
  each digest as the release API gives it — wolf 0.2.27 linux x86-64
  `5e17eebe…`, linux aarch64 `c475e5dc…`, macOS arm64 `ea461a76…`; lupin
  0.1.50 `e2867a35…`, `a0c0c707…`, `2cbd192d…` — every member hashed,
  `_wolf` `a368c8ec…` in all three wolf archives, `STD-REV` `87ba1620…`
  in all three.
- `0029738`, `f054aaf` — §1–§3, before the archives.
- `f18bbe8` — `fetch-toolchain` removes the archive's `std/`.
- `bdae32b` — the pin, both halves by digest, and the std pin.
- `2ec7c07` — the bump note.
- `gauntlet-base-f054aaf.log` (`3730126e9e8f…`), `gauntlet-pin-bdae32b.log`
  (`d685b95e85d7…`): both tiers built, WIR, own-code counts, stripped
  hashes (`objcopy --strip-debug --remove-section .note.gnu.build-id`),
  unit tests, fmt, the selftest, the differential suite on both tiers.

### The move table

| | base `f054aaf` (0.2.26) | pin `bdae32b` | head `9633593` |
|---|---|---|---|
| utilities built, release and dev | 28 | 28 | 31 |
| diagnostics | 0 | 0 | 0 |
| kasumi verdicts, release = dev | 3017 / 0 / 60 | 3017 / 0 / 60 | **3788 / 0 / 67** |
| verdict list | `591bf0fc…` | `591bf0fc…` | `d278de5c…` |
| `libwolf_rt.a` | `679d77e1…` | `ab575b27…` | `ab575b27…` |
| binaries differing from base, stripped | — | 28 of 28 | — |

The head gauntlet is `gauntlet-head-9633593.log` (`ea56163e9f7c…`), from
a clean tree at that commit.

### Differential counts, per utility (kasumi, release, at `9633593`)

| utility | cases | passed | skipped | the skips |
|---|---:|---:|---:|---|
| `ls` | 710 (292 before) | 694 | 16 | 6 wolf-lang#692, 2 #643, 1 #685, 4 not written yet, 3 devices this host lacks |
| `stat` | 160 | 152 | 8 | 2 #686, 1 #536, 1 #684, 1 #685, 3 devices this host lacks |
| `readlink` | 97 | 97 | 0 | |
| `env` | 103 | 90 | 13 | 5 #535, 1 #689, 1 `os_exec`'s empty name, 6 not written yet |

`env`'s cases were also run under `taskset -c 0-3` on kasumi: 90 / 0 /
13, the same.

### The commits

- `c2ac77c`, `b0c65ba`, `83b64e0` — `tools/difftest`: pipes, sockets,
  hard links, holes, access times, times relative to one instant, a tree
  kept for both sides, a mask, cases that print an account's name; a
  hole compared by its length; a dead harness is status 2.
- `56cad08`, `02cf532`, `6ca7d3a`, `9dc4f07` (with `readlink`), `bd4d616`,
  `ddefa27` — `src/bore/`: `info` (the record's words), `ids` (names
  from the two files), `clock` (TZif and the POSIX rule), `paths` (the
  canonical walk); the host decided at compile time.
- `0e39469`, `c5d574f`, `fff90ae`, `c8b2ccb`, `4bd40b4` — `ls`.
- `0b904f2` — `stat`. `9dc4f07`, `fe4f78d` — `readlink`. `6cb30e8` —
  `env`.
- `92e30f2` — the bench rows. `da9dafc`, `1dfec0b` — CLAUDE and README.

### The planted break

- `9545d10` PLANT: `six_months()` two minutes too long. CI run
  38115150278, job 114398462802 (ubuntu) went red on exactly the seven
  cases that stand on the rule — `ls: the six-month rule` and its
  `-nt`, `-nu`, `-ntu`, `--time-style=iso`, `-gn` and New York forms —
  3782 passed, 7 failed, 66 skipped; the two `ages` cases that print no
  short date (`long-iso`, `--full-time`) stayed green. The log is
  nomad-1 `~/lanes/bu20/ev/ci-plant-38115150278-ubuntu.log`
  (`a78569fb9226…`). The run's macOS job was still queued, and the run
  was cancelled by this lane once ubuntu had answered.
- `9633593` reverts it; its tree is `fe4f78d`'s.

### Bench (kasumi, release, GNU 9.11, at `9633593`, a clean tree)

`bench.log` (`f342b7fe6521…`), `bench-startup.log` (`e1c541bb9972…`), and a
JSON per row beside them. The load was 2.3 at the start and 8 at the
end; the README states it over the table.

| ls, 100,000 names | 0.2.26 | 0.2.27, same source | head | GNU | GNU / head |
|---|---:|---:|---:|---:|---:|
| plain | 38.2 | 38.4 | 29.0 | 57.8 | 1.99x |
| `-C` | 43.1 | 41.6 | 34.2 | 67.0 | 1.96x |
| `-S` | 147.6 | 137.6 | 161.6 | 109.3 | 0.68x |
| `-t` | 140.0 | 144.7 | 151.5 | 91.1 | 0.60x |
| `-R` (316 × 316) | 100.3 | 99.5 | 28.9 | 27.2 | 0.94x |
| `-l` | — | — | 196.5 | 239.7 | 1.22x |
| `-n` | — | — | 185.0 | 250.2 | 1.35x |
| `-s` | — | — | 153.8 | 139.7 | 0.91x |
| `-i` | — | — | 166.8 | 118.1 | 0.71x |
| `-F` | — | — | 151.0 | 115.7 | 0.77x |
| `-U` | — | — | 26.0 | 16.1 | 0.62x |
| `-lU` | — | — | 155.1 | 199.7 | 1.29x |
| `-lR` | — | — | 122.1 | 214.1 | 1.75x |

(milliseconds.) **The floor of `ls -l`:** `strace -c -f` over the 99,998
names of `flat/` — GNU 99,998 `statx` and 99,998 `llistxattr`, 201,751
calls in all; this `ls` 100,003 `statx` and 100,327 calls in all. Peak
RSS: 174 MB here, 29 MB GNU (33 MB and 28 MB for a plain listing).
`stat -c %s` of one file 279 µs against 215; of 10,000 files 19.4 ms
against 13.3; `readlink` of one link 275 µs against 211; `env true` 438
µs against 341.

### The static binaries, and what PAX's kernel must answer

Built at `9633593` in px12's Ubuntu 24.04 container (glibc 2.39, never
kasumi's own), by pax's `tools/mkboreutils` recipe (wolf's release build
through a `cc` that adds `-static`): ET_EXEC, no PT_INTERP, each
answering the dynamic binary's bytes on the probes. `static.log`
(`ba828af2da30…`), the traces in `ev/strace/`.

| binary | sha256 | bytes |
|---|---|---:|
| `ls` | `2bcd252c…` | 13,034,680 |
| `stat` | `6df81de1…` | 12,946,816 |
| `readlink` | `0871f02c…` | 12,905,624 |
| `env` | `f9321cc9…` | 12,945,456 |

Every binary, before `main`: `execve`, `brk`, `arch_prctl`
(`ARCH_SET_FS`), `set_tid_address`, `set_robust_list`, `rseq`,
`prlimit64` (`RLIMIT_STACK`), `readlinkat` of `/proc/self/exe`,
`getrandom` (8 bytes, `GRND_NONBLOCK`), `mprotect`; and `exit_group` at
the end. Then, by utility (`strace -f`, thirteen `ls` invocations, six
`stat`, five `readlink`, eight `env`):

- **`ls`**: `statx` (of descriptor 1 with `AT_EMPTY_PATH`; of each
  operand and, where the listing needs a record, of each name, with
  `AT_SYMLINK_NOFOLLOW` unless `-L`), `ioctl` (`TCGETS` on descriptor 1,
  the terminal question), `openat` (`O_RDONLY|O_NONBLOCK|O_CLOEXEC|
  O_DIRECTORY`), `fstat`, `getdents64`, `close`, `readlink` (a link's
  target under `-l`), `read`, `write`, and `mmap` for a large listing.
  **The files `-l` reads:** `/etc/passwd` and `/etc/group` (not under
  `-n`), and the zone — `/etc/localtime` when `TZ` is unset, else one
  `statx` of `/usr/share/zoneinfo/$TZ` and a read if it is there
  (`TZ=UTC0` costs the one failed `statx` and reads nothing).
- **`stat`**: `statx`, `readlink` (a link), `openat`/`read`/`close` (the
  same account and zone files, for a format that prints a name or a
  time), `getcwd` (`%m`), `write`.
- **`readlink`**: `readlink`; under `-f`, `-e`, `-m` also `getcwd` and
  one `statx` (`AT_SYMLINK_NOFOLLOW`) per component; `write`.
- **`env`**, its own calls: `statx` (descriptor 1, and each `PATH`
  candidate), `chdir` (`-C`), `write` (printing), and `execve` of the
  command. What follows the exec is the command's.

No signal call, no `futex`, no `poll`, no `clock_gettime` (the time is
read without one), no `lseek`.

### Upstream, filed with their witnesses

wolf-lang#684 (no I/O block size in the record), #685 (no extended
attribute: the ACL mark), #686 (no file-system record), #687 (a name that
is not UTF-8 is listable and nothing else), #688 (`0o…` and `0b…`
literals refused by native and release, run by the checked machine,
lupin and `wolf test`), #689 (`os_exec` runs `./name` for an empty
`PATH` component), #692 (the listing leaves out `.` and `..`).

## 5. Done-when

- Branch `bu20` on origin, PR wolffe-lang/boreutils#25 open and unmerged,
  five sections by name, commit shas as bullets, a test checklist.
- CI green at the head on ubuntu and macOS (run ids in the PR body).
- `lane-audit.sh boreutils bu20 25` run from the org directory, exit
  status read directly.
- kasumi: the pin worktree removed (`bench.sh` removes it as soon as its
  one binary is built); `target/`, `.wolf-bin/`, `.gnu-bin/`, the bench
  tree and the unpacked archives pruned; `ev/`, the static binaries and
  the probe scripts kept. No process of this lane left running.
- Nothing closed. To close at the merge, by whoever merges: none of
  boreutils' own. wolf-lang#625 and #626 are still OPEN on origin though
  0.2.27 ships their answer and this lane is written on it; that is the
  orchestrator's call.

## What the next boreutils lane inherits

- **`src/bore/info.lu`, `ids.lu`, `clock.lu`, `paths.lu`.** A record's
  words by name, account names, local time in any zone, a canonical
  path. `du`, `realpath`, `test`, `date`, `id` and `touch`'s reading
  side start from them.
- **The harness can hold a tree still**: `scratch_keep` for inodes and
  status-change times, `"now-N"` for anything measured against the
  clock, `mask` for one field one side cannot know, `accounts` for a
  name. And it must stay inside what ext4 holds: years 1901 to 2446,
  files to 16 TiB.
- **Keep a hot list's elements small, and sort on flat keys.** The cost
  was locality, measured; see `Keys` in `src/ls.lu`.
- **A unit test is not a build.** `wolf test` accepted what `wolf build`
  refuses (#688).
- **Owed:** `ls`'s `+` (needs #685), `stat -f` and `df` (#686), `stat -`
  and `cat f >> f` (#536), names that are not UTF-8 (#687), `ls -f`'s
  dots on ext4 (#692), `env -S`, `-v` and the signal options, `ls
  --block-size`, `--time-style=+FORMAT` and the quoting styles; and
  `ls -l`'s 174 MB over 100,000 names, which wants a list that can be
  given its room (#416).
