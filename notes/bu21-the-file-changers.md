# bu21 — the file changers (mkdir, rmdir, rm, touch, ln, mv, cp, chmod)

Lane note. **Class:** long (boreutils), **Opus**. **Wave:** 53. Branch
`bu21` off boreutils `870815c`. §1–§3 are committed before any probe is
run and before any line of `src/` or `tools/` changes; §3 is scored in
place later, never rewritten.

One deliverable: boreutils gains the utilities that change the file
system — `mkdir`, `rmdir`, `rm`, `touch`, `ln`, `mv`, `cp`, `chmod` —
each differential-tested against GNU 9.11 inside scratch trees, as far
as wolf 0.2.27's builtins reach. A utility whose core operation no
builtin performs is left out and named, with the issue that would
unblock it; nothing is faked.

## 1. Forbidden

No `rm` outside `~/lanes/bu21/` (nomad-1 and kasumi) and this lane's own
private clones, `/tmp` included; no deletion in any tree this lane did
not create; no `git add -A`; nothing under `~/.claude`; no edit to
another lane's file; no merge, no tag, no attribution trailer; no
`2>/dev/null` on a checkout. The toolchain from the RELEASE ARCHIVES by
digest, never a clone, Homebrew or `~/.local/bin`; nothing built from
wolf-lang trunk. No build on nomad-1: every build, difftest and bench
runs on kasumi, one tree, pruned as it goes; no scratch in `/tmp` on any
host. No "seen red" without a run id, sha, path or digest. Strict
evidence (wolf-lang#571): counts read from the full output, SKIP
counted; a `wolf build` that exits 2 is a compile error, never a skip.
No package is installed anywhere. At most two CI runs of this lane at
once; no other lane's run is cancelled.

**GNU coreutils source is never read**, nor busybox's, uutils' or
toybox's for this lane: GNU's behaviour comes from its documentation,
POSIX.1-2024 and black-box runs of the staged 9.11 oracle
(`tools/fetch-oracle`).

**These programs delete and overwrite.** Every test and every hand run
of `rm`, `mv`, `cp`, `rmdir` — this lane's or GNU's — happens inside a
scratch directory the harness created under `~/lanes/bu21/` (or CI's
temp root) and whose absolute path it has checked by prefix immediately
before the call. No build of `rm` is ever run with an operand that is
`/`, `~`, `..`, a path outside the scratch root, or an empty or unquoted
variable — and neither is GNU's. The `/` refusal is implemented and
tested (as a function, never as a run) before any recursive removal
exists. Nothing runs as root. `fs_remove_dir_all` is never called by any
program in this repository: a recursive removal is this lane's own walk,
one `lstat` and one host call per entry.

## 2. Inputs, verified (2026-10-11, origin and the release archive)

| input | origin says | verdict |
|---|---|---|
| boreutils trunk `870815c` (bu20; wolf 0.2.27 / lupin 0.1.50; 31 utilities) | `origin/trunk` is `870815c84fe4`; `wolf-toolchain.toml` pins wolf 0.2.27 (`0ddda6b7`, linux x86-64 `5e17eebe…`) and lupin 0.1.50 (`32b970da`, `e2867a35…`), std `87ba162`; 31 `src/*.lu` entries; trunk CI run 38117246786 green | holds |
| `src/bore/info.lu`, `ids.lu`, `clock.lu`, `paths.lu`; harness keys `scratch_*`, `mask`, `accounts`; the harness exits 2 when it dies | all four files present; `tools/difftest` carries the keys and the status-2 arm | holds |
| wolf-std trunk `98e1b7b` (sc58) has `fs.stat`/`lstat`/`read_link`/`entries`, `env.unset`, `process.exec` | wolf-std `trunk` is `98e1b7bcac3a`. This repository's std pin is still `87ba162` (the commit the 0.2.27 archive bundles), which has none of them, and boreutils imports `std.env` and `std.time` only | holds; **the builtins are called directly**, the repository's convention, and the std pin does not move in this lane |
| the 0.2.27 prelude | `wolf prelude` on the staged archive (kasumi, digest checked by `tools/fetch-toolchain`): 151 names, 111 functions. The fs family is `fs_read_text fs_write_text fs_open fs_create fs_read fs_write fs_close fs_remove fs_exists fs_open_mode fs_read_bytes fs_write_bytes fs_read_chunk fs_write_chunk fs_read_dir fs_create_dir fs_create_dir_all fs_remove_dir fs_remove_dir_all fs_rename fs_is_file fs_is_dir fs_size fs_modified_ms fs_fstat fs_stat fs_lstat fs_read_link fs_read_dir_entries fs_seek fs_tell fs_read_at fs_copy_chunk` — 33 names. A grep of all 151 for `link`, `chmod`, `mode`, `time`, `chown`, `owner`, `trunc`, `umask`, `uid`, `access`, `fifo`, `mknod`, `perm` finds `fs_open_mode` (the OPEN mode 0–5), `fs_read_link` (a read), `os_term_mode`/`os_term_set_mode` (the terminal's), `time_now_ms`/`time_unix_ms`/`time_sleep_ms` (the clock) and the keyword `timeout`, and nothing else | the census in §3 is predicted from this and from the spec, then probed |
| spec `[os.fs.*]` at the tag (`spec/11-os.md` at `0ddda6b`, §6 and the host table in §7, 104 lines) | `fs_create_dir(str) -> () ! {denied, exists, io, not_found}`, `fs_create_dir_all(str) -> () ! {denied, io}`, `fs_remove_dir(str) -> () ! {denied, io, not_found}`, `fs_remove(str) -> () ! {denied, io, not_found}` (never a directory: linux `io`, macOS `denied`), `fs_rename(str, str) -> () ! {cross_device, denied, exists, io, not_found}`, `fs_copy_chunk(int, int, int) -> int ! {eof, io}` (linux: `copy_file_range`, `sendfile`, `splice`, then read/write), `fs_open_mode` modes 0–5 with no permission argument. No clause for a link, a mode change, a time change, an owner change or a truncation to a length | holds |
| known open: wolf-lang#536, #684–#687, #692, #688 | all seven OPEN on origin. Also open and met here: #346 (no permission surface), #633 (no uid/euid), #406 (a non-UTF-8 argument aborts), #642 (`fs_copy_chunk`'s lost bytes on a failed write), #416 | holds |
| the oracle | GNU coreutils 9.11 by digest (`gnu-oracle.toml`), `LC_ALL=C`, `_POSIX2_VERSION=200112`; kasumi's own GNU is 9.12, so every kasumi run stages the oracle with `tools/fetch-oracle` | holds |
| hosts | kasumi: 16 cores, /home (btrfs) 51 GB free at the start, `strace`, `hyperfine`, `taskset` present, uid 1000. nomad-1 holds the clone the commits are made in and builds nothing | holds |

## 3. Prediction (committed before the first probe and the first change)

Each line names what is expected and the observation that falsifies it.

### The census

"Four machines" are wolf's: the checked machine (`wolf conform-run
--checked --json`), native (`wolf build`), release (`wolf build
--release`) and lupin 0.1.50 (`lupin run`, which serves the fs tier over
relative paths inside its tree). Probed on kasumi (linux x86-64); macOS
is reached through CI by the utilities themselves, not by the census.

1. **Exists on all four machines, with the host's reason in
   `os_error()`:** make a directory (`fs_create_dir`; `exists` when the
   name is taken, `not_found` for a missing parent), make it with its
   parents (`fs_create_dir_all`), remove an empty directory
   (`fs_remove_dir`; a directory that is not empty is the `io` row with
   `ENOTEMPTY`, 39 on linux), unlink (`fs_remove`; a symbolic link is
   removed and its target is not; a directory is `io`/`EISDIR` on
   linux), rename (`fs_rename`: one `rename(2)`, atomic, replacing an
   existing file, refusing a directory over a non-empty one), copy bytes
   (`fs_copy_chunk`), truncate to ZERO (`fs_open_mode(path, 1)`).
   Falsified by a machine that refuses one, or by a row or number that
   differs. **Hedge:** `[os.host.sigs]` records lupin 0.1.36 as not
   resolving `fs_create_dir` and `fs_remove_dir`; predicted served by
   0.1.50, not known.
2. **A cross-device rename is told by name**: `fs_rename` between two
   btrfs subvolumes under `~/lanes/bu21/` (different `st_dev`) answers
   the `cross_device` row with `EXDEV` (18) on native, release and
   checked. Falsified by another row.
3. **Missing, on every machine** (no prelude name, so a program naming
   one does not compile): make a directory WITH A MODE; create a file
   with a mode; change a mode (`chmod`); create a hard link; create a
   symbolic link; change times (`utimensat`, `UTIME_NOW`/`UTIME_OMIT`);
   change an owner; truncate to a length; find or punch a hole
   (`SEEK_DATA`/`SEEK_HOLE`: `fs_seek`'s whence is 0–2) or ask for a
   reflink; read or set the umask; make a fifo or a device node; ask
   whether THIS process may write a file (`access`, or the effective
   uid: #633); rename without replacing (`renameat2`), which is what
   makes `mv -n` atomic; and any call relative to an open directory
   (`openat`, `unlinkat`), which is what makes a recursive removal safe
   against a directory swapped for a link while it runs. Each gets one
   issue with what GNU needs it for, or a comment where an issue already
   names it (#346, #633).
4. **A hole can be WRITTEN but not found**: `fs_seek` past the end then
   a write leaves a hole (blocks below size), so a sparse file can be
   made; nothing can ask where a source's holes are. Falsified by
   `fs_stat`'s blocks word.
5. `fs_copy_chunk` on btrfs shares extents (linux's `copy_file_range`
   clones there), so a copied 1 GiB file occupies no new data blocks —
   the same thing GNU's default `--reflink=auto` does. Not a builtin
   property: the host's. Falsified by `btrfs filesystem du` or by the
   time.

### The utilities

6. **Left out, each for one missing core operation, and named in the
   README:** `touch` (its operation is changing times; creating an empty
   file is a side effect and is not shipped as "touch"), `ln` (no link
   of either kind), `chmod` (no mode change). Falsified only by a
   builtin the census finds and this list did not.
7. **`mkdir`** ships `-p`, `-v`, `--help`, `--version`: one
   `fs_create_dir` per component, GNU's messages word for word
   (`cannot create directory 'x': File exists`, `…: No such file or
   directory`, `created directory 'x'`). **Refused by name:** `-m`
   (needs a mode at creation or a `chmod`: #346), `-Z`/`--context`.
   **Differs, named:** under `-p` GNU gives a missing parent `u+wx`
   whatever the umask says; this one gets the umask's mode (invisible
   at umask 022, a skip under a umask that masks the owner). About 60
   cases, 0 failed, under 8 skipped.
8. **`rmdir`** ships `-p`, `--ignore-fail-on-non-empty`, `-v`. About 45
   cases, 0 failed, 0 skipped.
9. **`rm`** ships `-f`, `-r`/`-R`, `-d`, `-v`, `-i`, `-I`,
   `--interactive[=WHEN]`, `--one-file-system`, `--preserve-root[=all]`
   (the default) and `--no-preserve-root`. It never follows a link: a
   link is unlinked, whatever it names. `/` is refused by comparing the
   operand's device and inode with `/`'s, and `.` and `..` by name, as
   GNU does; the `/` rule is a function in `src/bore/` with unit tests,
   and no test runs any `rm` on `/`. **Differs, named:** at a terminal
   GNU asks before removing a file this user may not write; wolf cannot
   ask the host that (#633), so the question is decided from the
   owner's write bit. A removal is path-based (no `unlinkat`): a tree
   deeper than `PATH_MAX` fails where GNU's does not, and a directory
   swapped for a link mid-run is followed where GNU's is not. About 120
   cases, 0 failed, under 6 skipped. GNU's two-line message for `/` is
   NOT measured (running it is forbidden) and is marked inferred.
10. **`mv`** ships `-f`, `-n`, `-i`, `-v`, `-T`, `-t`,
    `--strip-trailing-slashes`, files and directories, into a directory.
    **Across devices it is refused by name** (`cross_device`): the copy
    half cannot keep a mode, a time, an owner or a link. `-n` is a check
    then a rename, not one call. `-u`, `-b`/`--backup`, `--exchange`,
    `-Z` refused by name. About 110 cases, 0 failed, under 8 skipped.
11. **`cp`** ships `-r`/`-R`, `-f`, `-n`, `-i`, `-v`, `-T`, `-t`,
    `-L`, `-H`, `-P`, `--remove-destination`. Bytes move by
    `fs_copy_chunk`. **What cannot be done is refused, never
    approximated:** a NEW file gets the mode creation gives it; when
    that is not the mode GNU would have given (the source's, less the
    umask — an executable, say) the copy is removed again and the
    operand fails by name. A symbolic link met under `-r` without `-L`
    cannot be re-created and fails by name; so does a fifo or a device.
    `-p`, `--preserve`, `-a`, `-d`, `-l`, `-s`, `--sparse`, `--reflink`
    (any value but the default's `auto`), `-u`, `-b`, `--parents`,
    `--attributes-only`, `-x`, `-Z` are refused by name. About 150
    cases, 0 failed, about 20 skipped by named cause.
12. The corpus grows by about 485 cases, to past 4,300, with no existing
    verdict moving: the 3,855 cases of the 31 utilities at `870815c`
    keep their verdict list on kasumi (3788 / 0 / 67) after the harness
    learns to check its scratch root, to run a case under a umask and to
    compare modes and link counts. Falsified by one line of that list.

### The harness and the safety tests

13. `tools/difftest` gains: a scratch ROOT it resolves once
    (`$BORE_SCRATCH_ROOT`, else the temp directory) and refuses when it
    is `/`, a home directory or shallower than two components; a check,
    immediately before each side runs, that the scratch directory is
    under that root by resolved prefix and is not a link; for the
    utilities that change the file system, a refusal (status 2) of any
    case whose operand is `/`, `~`, climbs out with `..`, or is absolute
    and outside the scratch directory; a `umask` key; and a fifth
    compared field, `tree`: every entry's kind, permission bits, link
    count (not a directory's), a file's size, and a modification time
    older than the case itself. Each new check has a plant in
    `tests/selftest/` that must fail or refuse by name.

### The bench, the binaries, CI

14. On kasumi (btrfs), release, against GNU 9.11: `cp` of a 1 GiB file
    within 0.5–2x GNU (both end in a clone, a few milliseconds);
    `cp -r` of a 100,000-file tree 0.4–0.9x GNU's speed (a record per
    entry and a path `str` per call); `rm -r` of it 0.5–0.9x; `mkdir -p`
    of a 1,000-deep path 0.5–1.5x. Falsified outside those bands.
15. Static linux builds of the new utilities make no system call
    outside bu20's start-up set (`execve`, `brk`, `mmap`, `munmap`,
    `mprotect`, `arch_prctl`, `set_tid_address`, `set_robust_list`,
    `rseq`, `prlimit64`, `getrandom`, `readlinkat`, `exit_group`) and:
    `statx`, `fstat`, `openat`, `close`, `read`, `write`, `ioctl`
    (`TCGETS`), `getdents64`, `mkdir`, `rmdir`, `unlink`, `rename`,
    `copy_file_range` (with `sendfile`, `splice` behind it), `dup` or
    `fcntl` (the duplicate `fs_copy_chunk` takes), `lseek`. Falsified by
    a name not on the list.
16. CI green on ubuntu and macOS at the head. macOS differs in rows
    (`fs_remove` on a directory is `denied` there) and in `errno`
    numbers; the utilities print `os_error_text`, so the cases pass on
    both. A planted break — `rm -r` taking `fs_stat` for `fs_lstat`, so
    it follows a link out of its tree, against a scratch target only —
    goes red in CI on the case written for it.
17. One thing here is wrong in a way this list does not name.
