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
