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

## 3a. The prediction, scored

§3 above is as it was committed (`1a9a49c`, before the first probe and
the first change). Scored in place, by line.

| # | predicted | measured | verdict |
|---|---|---|---|
| 1 | seven operations exist on all four machines, with the host's number beside the row; lupin perhaps not `fs_create_dir`/`fs_remove_dir` | all seven, on native, release, checked and lupin 0.1.50, every row as predicted (`ENOTEMPTY` 39, `EISDIR` 21). The hedge fell the good way: lupin serves both. **Not predicted:** lupin answers `os_error()` 0 after `fs_create_dir`'s `exists` and `fs_rename`'s `cross_device` (wolf-interp#235) | right; one parting found |
| 2 | a rename between two btrfs subvolumes is `cross_device`, `EXDEV` 18 | `cross_device errno=18 text=Invalid cross-device link` on native, release and checked; the row on lupin, with number 0 | right |
| 3 | fourteen operations are missing on every machine | all fourteen probe names fail to resolve on all four (`E0301` three times, lupin's `does not resolve`); ten issues filed (wolf-lang#698–#707) and two commented (#346, #633) | right |
| 4 | a hole can be written and not found | `hole_kept true` on all four; `fs_seek` whence 3 is `invalid` | right |
| 5 | `fs_copy_chunk` on btrfs shares extents | a 1 GiB file copies in 18.2 ms (GNU 18.1). Told by the time only: `btrfs filesystem du` was not run | right, by one of its two falsifiers |
| 6 | `touch`, `ln`, `chmod` left out | left out, each named in the README with its issue | right |
| 7 | `mkdir`: `-p`, `-v`; `-m` and `-Z` refused; about 60 cases, under 8 skips | 112 cases, 103 pass, 9 skip (seven `-m`, two umask). `-Z` and `--context` are ACCEPTED, as GNU's are on a kernel without SELinux (`--context=CTX` warns, in GNU's words). **Not predicted:** which name `-p` blames — the component it stopped at, and the PARENT when the parent may not be searched | one skip over; better on `-Z` |
| 8 | `rmdir`: about 45 cases, no skip | 70, none skipped. **Not predicted:** `Symbolic link not followed` for a link named with a slash (but not a link to a file), and the word `directory` in a parent's message unless the reason is `Not a directory` | right |
| 9 | `rm`: every option incl. `--preserve-root[=all]` and `--no-preserve-root`; about 120 cases, under 6 skips | 221 cases, 218 pass, 3 skip. **`--no-preserve-root` is refused on purpose and `--preserve-root=all` is not written**: both predicted shipped. The terminal question matches GNU in nine hand probes (`hand-rm.log`). **Not predicted:** which "no" keeps a parent silent (one given BEFORE anything was done to a directory) and which lets GNU ask about the parent and fail; that `rm -r link/` empties the directory behind the link, in GNU and here; the `Try 'rm ./-x'` hint | wrong on two options, right on the rest |
| 10 | `mv`: about 110 cases, under 8 skips; another file system refused | 142 cases, 134 pass, 8 skip; refused by name, and `--no-copy` is GNU's own message (`hand-mv.log`). **Not predicted:** a declined `-i` is status 1; an empty DEST is the working directory; on macOS `-n` looks at DEST before SOURCE, and a stripped `link/` is still handed to the host with its slash | one skip over |
| 11 | `cp`: the list incl. `-P`; about 150 cases, about 20 skips | 194 cases, 163 pass, 31 skip. **`-P` is refused** (it exists to copy a link as a link). `--no-preserve=mode` is shipped and was not predicted: it asks for exactly the mode wolf can give. **Three things wrong on the way:** the first cut asked at a terminal before replacing a protected DEST, and GNU's `cp` never does (found by hand, `hand-cp.log`); it copied a directory in the directory's own order, and GNU copies in INODE order (found by CI on ext4 and APFS, run 38123042749; on btrfs the two are the same order); it listed a directory before making its copy, so a tree copied into itself never met itself | wrong on `-P` and the skip count |
| 12 | about 485 new cases, past 4,300; the 31 utilities' verdict list unmoved by the harness | 739 new, 4,594 in all; the 31 utilities' list is `80aa80b853d27d63…` under trunk's harness (`difftest-trunk-harness.log`), under this one before any utility (`difftest-harness-only.log`) and at the head | right on the list; low on the count |
| 13 | the harness's root, guard, refusals, `umask`, `tree`, a plant each | all there. **One rule changed:** "shallower than two components" would refuse `/tmp`, CI's root; the root is refused when it is `/`, a home directory or the directory homes live in. **Not predicted:** `mkdir -v` and `rmdir -v` name the program on STANDARD OUTPUT, and GNU on macOS is `gmkdir` — 36 reds on that prefix alone (run 38122354989), now `PROG` for a changer's line-leading name | right, with one rule softened and one hole found by macOS |
| 14 | `cp` 1 GiB 0.5–2x; `cp -r` 0.4–0.9x; `rm -r` 0.5–0.9x; `mkdir -p` deep 0.5–1.5x | 1.00x; 0.72x and 0.75x; **0.94x to 1.02x**; **0.37x** | two in band, `rm -r` better than its band, `mkdir -p` worse |
| 15 | no system call outside the list | none outside it; `lseek`, `dup`, `splice` and `munmap` never made (the duplicate is `fcntl(F_DUPFD_CLOEXEC)`) | right |
| 16 | CI green on both hosts; macOS differs in rows and numbers; the plant red | green (§4). macOS differed in NONE of the predicted ways and in four others (line 13's prefix; inode order; `mv -n`; `rename` of `link/`). The plant is red on both hosts, on seven cases, the named one among them (run 38123686799) | right on green and red, wrong on where macOS parts |
| 17 | one thing wrong that this list does not name | five. (a) **A process slip:** the first `tools/fetch-toolchain` and `tools/fetch-oracle` on kasumi ran before `TMPDIR` was set and made their temporary directories under `/tmp` (both remove them; every later command sources `~/lanes/bu21/env.sh`). (b) The prelude's `min` is refused by every compiler tier (wolf-lang#708). (c) `fs_copy_chunk` costs eleven system calls around the one that copies a small file (#709), which is most of `cp -r`'s gap. (d) and (e) are line 11's terminal question and inode order | — |

## 4. Evidence index

Shas are this branch's (`bu21`, wolffe-lang/boreutils). kasumi paths are
under `~/lanes/bu21/ev/` and stay there; a digest's first twelve
characters follow each. **Verified** means run by this lane and read;
**inferred** is said where it applies.

### The census

- `notes/bu21/census/` (`0fa711f`): the probes, `run.sh`, and
  `transcript-kasumi.log` (`bda71944fc20…`, the same bytes as kasumi's
  `census-2.log`). kasumi, linux x86-64, btrfs, wolf 0.2.27 and lupin
  0.1.50 from the release archives by digest. macOS is reached by the
  utilities in CI, not by the census. **Verified**, linux only.

| operation | builtin | native | release | checked | lupin |
|---|---|---|---|---|---|
| make a directory | `fs_create_dir` | yes | yes | yes | yes (`exists` with number 0) |
| … with its parents | `fs_create_dir_all` | yes | yes | yes | yes |
| … with a mode | none (wolf-lang#346) | — | — | — | — |
| remove an empty directory | `fs_remove_dir` | yes | yes | yes | yes |
| unlink (a link is removed, not its target) | `fs_remove` | yes | yes | yes | yes |
| rename, atomic, replacing | `fs_rename` | yes | yes | yes | yes |
| tell another file system | `fs_rename`'s `cross_device` | yes, 18 | yes, 18 | yes, 18 | the row; number 0 |
| rename without replacing, or exchange | none (#706) | — | — | — | — |
| create a hard link | none (#699) | — | — | — | — |
| create a symbolic link | none (#698) | — | — | — | — |
| change a mode | none (#346) | — | — | — | — |
| change times | none (#700) | — | — | — | — |
| change an owner | none (#701) | — | — | — | — |
| truncate to zero | `fs_open_mode(p, 1)` | yes | yes | yes | yes |
| truncate to a length | none (#702) | — | — | — | — |
| copy bytes | `fs_copy_chunk` | yes | yes | yes | yes |
| write a hole | `fs_seek` past the end, then a write | yes | yes | yes | yes |
| find a hole, ask for a clone | none (#703) | — | — | — | — |
| read or set the umask | none (#704) | — | — | — | — |
| make a fifo or a device | none (#705) | — | — | — | — |
| "may I write it?", the user id | none (#633) | — | — | — | — |
| name an entry relative to an open directory | none (#707) | — | — | — | — |

### The prediction, the commits

- `1a9a49c` — §1–§3, before the first probe.
- `0fa711f` — the census.
- `7cb8ffc`, `e281f8c`, `a96fc78` — `tools/difftest`: the scratch root
  and its guard, the changers' refusals, `umask`, `tree`; the plants
  (`tests/selftest/tee.toml`, `tests/refuse/`); a changer's name on
  standard output.
- `c45a83b` — `mkdir`. `310a606` — `rmdir`.
- `ee6ca2b` — `src/bore/change.lu` and `src/change_test.lu`: the root
  and dot refusals as functions, unit-tested, **before any `rm`
  exists** (`rm` is `3b4a9bf`, the commit after it).
- `3b4a9bf` — `rm`. `ef9cf67` — `mv`. `4db0522`, `c8247e1`, `384b532`
  — `cp` (and `mv`'s two macOS rules).
- `c2d463d` — `tools/bench` and the five bench files.
- `8dbb30a`, `7770df6` — the plant and its removal (below).
- `7381599`, `2546034`, `546a656` — cases: one dropped, 29 naming 9.11
  for the field, the generators.
- `78b4bb7`, `306e594` — CLAUDE and README.

### Differential counts, per utility (kasumi, release = dev, at `2546034`)

`gauntlet-2546034.log` (`ef1373030d02…`), `difftest-release-2546034.log`
(`013303a3ecaf…`), `difftest-dev-2546034.log` (`05386bfc4e0a…`): both
tiers built (36 binaries each), fmt, unit tests, the suite on both
tiers, the selftest, the evidence gate. **4,476 passed, 0 failed, 118
skipped** on both tiers, one verdict list (`651d325f118f…`). `rm`, `mv`
and `cp` again under `taskset -c 0-3`: 515 / 0 / 42, the same
(`difftest-taskset-2546034.log`, `647af80da059…`). **Verified.**

| utility | cases | passed | skipped | the skips |
|---|---:|---:|---:|---|
| `mkdir` | 112 | 103 | 9 | 7 wolf-lang#346 (`-m`), 2 #704 (the umask under `-p`) |
| `rmdir` | 70 | 70 | 0 | |
| `rm` | 221 | 218 | 3 | 2 `--no-preserve-root` (refused on purpose), 1 `--preserve-root=all` (not written) |
| `mv` | 142 | 134 | 8 | 1 #706 (`--exchange`), 7 not written yet (`-u`, `-b`, `-S`, `--debug`) |
| `cp` | 194 | 163 | 31 | 9 #346 (a new file's or directory's mode), 4 #346/#700/#701 (`-p`, `--preserve`, `-a`), 6 #698, 1 #699, 1 #705, 5 #703, 5 not written yet |
| `touch`, `ln`, `chmod` | — | — | — | left out: no builtin for the operation (#700; #698, #699; #346) |

What no case can stage is a hand transcript, GNU beside this program,
each run inside a `gx.sh` scratch directory: `hand-rm.log`
(`728b2d43490a…`: `--one-file-system` across a btrfs subvolume, nine
terminal probes, the refusals, a link out of a tree), `hand-mv.log`
(`f04d76d9a6ae…`: another file system, `--no-copy`, three terminal
probes), `hand-cp.log` (`784ea561d18e…`: every refusal, three terminal
probes, a copy across subvolumes). **Verified by hand; no case holds
them.** GNU's two lines for `rm -r /` were inferred when this section
was first written; they are measured now, in a container (§6).

### CI

- Run 38124071375 at `2546034`, the code's head, green on all three
  jobs: ubuntu (job 114424642627) 4,477 passed, 0 failed, 117 skipped;
  macOS (job 114424642667) 4,337 / 0 / 257; the field's GNU 9.4 (job
  114424642693) 4,372 / 15 / 207, the fifteen being trunk's (`expand`
  3, `fold` 10, `unexpand` 2). The commits after it change notes, the
  README and case-file headers; the run at the branch's last commit is
  in the PR body.
- The reds on the way, each fixed before the head: run 38122354989
  (macOS: 36 cases on `gmkdir:`/`grmdir:` at the start of a stdout
  line), run 38123042749 (ubuntu 5 and macOS 9: `cp -r`'s order, and
  macOS's `mv -n` and stripped slashes). Runs 38121786186 and
  38122934032 were this lane's own, superseded, and cancelled by it.
- **linux aarch64 was not run** (the pin has its row; no host).

### The planted break

- `8dbb30a` PLANT: `rm`'s walk reads an entry with `fs_stat` for
  `fs_lstat`, so a link to a directory is taken for the directory and
  followed out of its tree. Against scratch targets only: every link
  in `tests/cases/rm.toml` points inside its scratch directory or at
  nothing. CI run 38123686799 went red on both hosts — ubuntu (job
  114423482748) 4,470 passed, **7 failed**, 118 skipped; macOS (job
  114423482631) 4,330 / 7 / 258 — and the seven are `rm: -r: a link
  out of the tree is removed, and what it names is not` (the case
  written for it: GNU leaves `outside/keep`, the planted `rm` leaves
  `outside` empty), its `-rv` twin, and five more that hold a link in
  a tree. The logs are nomad-1
  `~/lanes/bu21/ev/ci-plant-38123686799-ubuntu.log` (`22031c533f3f…`)
  and `…-macos.log` (`bbc5b2c7918a…`); kasumi saw the same seven first
  (`rm-plant.log`, `369159e045ff…`).
- `7770df6` removes it; its tree is `384b532`'s, which run 38123623741
  had already seen green.

### Bench (kasumi, btrfs, release, GNU 9.11, at `546a656`)

`bench.log` (`c6ef3a46a17f…`), `bench-rm-again.log` (`ef2d644b12c7…`),
`bench-startup.log` (`949bd4786286…`), `floor.log` (`6810935579af…`).
**The load was between 5 and 9 throughout** (other lanes building; it
was 12 for an earlier take), and the README states it over the table.

| bench | boreutils | GNU | GNU / boreutils |
|---|---:|---:|---:|
| `cp` of one 1 GiB file | 18.2 ms | 18.1 ms | 1.00x |
| `cp -r`, 99,856 files in 316 directories | 1,680 ms | 1,208 ms | 0.72x |
| `cp -r`, 100,000 files in one directory | 1,811 ms | 1,353 ms | 0.75x |
| `rm -r` of the first | 933 ms | 893 ms | 0.96x |
| `rm -r` of the second | 982 ms, 987 ms | 999 ms, 1,000 ms | 1.02x, 1.01x (two later takes; in the run of record this row read 2,029 ms under another lane's build) |
| `mkdir -p`, a thousand deep | 21.0 ms | 7.8 ms | 0.37x |
| `rmdir -p`, a hundred deep | 1.1 ms | 1.0 ms | 0.94x |
| start-up: `mkdir`, `rmdir`, `rm`, `mv`, `cp` | 331, 358, 320, 350, 391 µs | 238, 257, 279, 354, 358 µs | 0.72x, 0.72x, 0.87x, 1.01x, 0.92x |

System calls over 10,000 files in 100 directories (`floor.log`): `cp
-r`, GNU 2 `openat`, 1 `ioctl` (the clone), 2 `close` and 2 stats a
file; here 2 `openat`, 2 `copy_file_range`, 4 `fcntl`, 6 `close`, 4
`statx` and 1 `read` a file. `rm -r`, GNU 10,101 `unlinkat`; here
10,000 `unlink`, 101 `rmdir` and 205 `statx`.

### The static binaries, and what PAX's kernel must answer

Built at `546a656` in px12's Ubuntu 24.04 container (glibc 2.39, never
kasumi's own), by pax's recipe (wolf's release build through a `cc`
that adds `-static`): ET_EXEC, no PT_INTERP. `static.log`
(`fa15ef7c4296…`), `static2.log` (`3c721d6373a3…`), the traces in
`ev/strace/` (43 invocations), the binaries in kasumi
`~/lanes/bu21/static/`. **Verified** by `strace -f`.

| binary | sha256 | bytes |
|---|---|---:|
| `mkdir` | `1dd84e0f2529…` | 12,904,256 |
| `rmdir` | `fd6ae2ffbeda…` | 12,910,272 |
| `rm` | `3dbb3c814657…` | 12,951,944 |
| `mv` | `c2ca688804c2…` | 12,929,024 |
| `cp` | `0f9d59057ac9…` | 12,979,464 |

Every binary, before `main` and at the end, as bu20's: `execve`,
`brk`, `arch_prctl`, `set_tid_address`, `set_robust_list`, `rseq`,
`prlimit64`, `readlinkat` (`/proc/self/exe`), `getrandom`, `mprotect`,
`exit_group`. Then, by utility:

- **`mkdir`**: `statx` (descriptor 1; and, under `-p`, a prefix that
  could not be made), `mkdir`, `write`.
- **`rmdir`**: `statx` (descriptor 1; a link named with a slash),
  `rmdir`, `write`.
- **`rm`**: `statx` (descriptor 1, `/`, each operand, and each entry
  the listing calls a directory or a link — `AT_SYMLINK_NOFOLLOW`),
  `openat`/`fstat`/`getdents64`/`close` (a directory under `-r`),
  `unlink`, `rmdir`, `ioctl` (`TCGETS` on descriptor 0: is it a
  terminal), `read` (descriptor 0, an answer a byte at a time),
  `write`.
- **`mv`**: `statx` (descriptor 1, the target, SOURCE and DEST),
  `rename`, `ioctl` (`TCGETS` on 0), `read` (an answer), `write`.
- **`cp`**: `statx` (descriptor 1, the target, SOURCE, DEST, each
  entry under `-r`), `openat` (SOURCE `O_RDONLY`; DEST
  `O_CREAT|O_EXCL` or `O_TRUNC`; a directory), `fcntl`
  (`F_DUPFD_CLOEXEC`, twice a transfer), `copy_file_range` (and
  `sendfile` when the kernel refuses that for the pair: `/dev/null`),
  `read` (the confirming read at the end of a file; an answer under
  `-i`), `mmap` (that read's buffer), `close`, `fstat`, `getdents64`,
  `mkdir`, and its own removals: `unlink` (`-f`,
  `--remove-destination`, a copy refused for its mode) and `rmdir` (a
  directory refused for its mode), `write`.

No signal call, no `futex`, no `poll`, no `lseek`, no `chdir`, no
clock. `rm`, `mv` and `cp` read no file but their operands; none opens
`/etc/passwd`, a zone file or `/proc`.

### Upstream, filed with their witnesses

wolf-lang#698 (no symbolic link can be made), #699 (no hard link),
#700 (no call changes a time), #701 (none an owner), #702 (truncation
to zero only), #703 (a hole cannot be found, a clone cannot be asked
for), #704 (no umask), #705 (no fifo, no device node), #706 (a rename
always replaces), #707 (no call relative to an open directory), #708
(the prelude's `min` refused by every compiler tier), #709
(`fs_copy_chunk`'s eleven calls around one); comments with witnesses
on #346 (a mode at creation AND a change of one) and #633 (`access`,
the ids); wolf-interp#235 (lupin's `os_error()` 0 after two rows).

## 5. Done-when

- Branch `bu21` on origin, PR wolffe-lang/boreutils#26 open and
  unmerged, five sections by name, commit shas as bullets, a test
  checklist.
- CI green at the head on ubuntu and macOS (run 38124071375 at the
  code's head, above; the run at the branch's last commit is in the PR
  body).
- `lane-audit.sh boreutils bu21 26` run from the org directory, exit
  status read directly.
- kasumi: `target/`, `.wolf-bin/`, `.gnu-bin/`, `.lu-cache/`, the
  census work directory and the bench trees pruned; `ev/`, the static
  binaries, the probe scripts and `gen/` kept. No worktree was made.
  No process of this lane left running.
- Nothing closed. To close at the merge, by whoever merges: none.
  Every issue this lane filed stays open: each is a builtin that does
  not exist yet.

## 6. Sent back: the root, run as a program

The first report said the refusal of `/` was unit-tested as a function,
that its wiring into `rm` had no end-to-end test, and that GNU's words
for it were remembered. The orchestrator sent the lane back for that
one path, with a rule that replaces §1's for it: `/` may be handed to
`rm` where `/` is DISPOSABLE — a throwaway container whose whole root
file system is scratch, nothing of a host mounted in it, no network —
and nowhere else.

- **`tools/roottest`** (`8ca04d6`, `5426568`) builds `rm`, `mv` and
  `cp` static on both tiers, copies them and a GNU 9.11 into an image
  (no mount), and runs each case of `tests/root/cases.toml` in a fresh
  container, as an unprivileged user and as root inside it. A script in
  the image sums a sentinel tree, `/etc`'s and `/usr/bin`'s entry
  counts and the programs before and after; a root that was removed
  cannot run the second sum, so a failed guard is a missing line. CI
  runs it on the ubuntu leg with docker (`ab16a1a`); macOS has no
  container engine and the programs are linux binaries.
- **GNU's answers are measured** (`tools/roottest --record`; kasumi,
  px12's Ubuntu 24.04 image, the oracle's tarball by digest built in
  that image, `root-gnu-record.log`, `66c5a48c9c62…`), and asserted of
  GNU again on every run. `rm -r /`, `-rf /`, `-rf -- /`, `-r ///` and
  `-r --preserve-root /`: `it is dangerous to operate recursively on
  '/'`, then `use --no-preserve-root to override this failsafe`,
  status 1. `-rf //`, `-rf link-to-root/` and the link by its whole
  path: the same with `on 'NAME' (same as '/')`. `-rf /.`, `/..`,
  `/../`, `.`, `..`, `./..`: `refusing to remove '.' or '..'
  directory: skipping 'NAME'`. `-rf / other` and `-rf other /`: the
  root refused and **`other` removed, in either order**, status 1.
  `-rf link-to-root`: the link removed, status 0. `-rf ""`: nothing,
  status 0. `rm /`: `Is a directory`; `rm -d /`: `Device or resource
  busy`. The remembered message was right for `/` and for the
  `(same as '/')` form; **what was wrong was `//`**, which this `rm`
  had folded to `/` and GNU names as typed (`296e2e2`).
- **Thirty cases, 178 runs, none failed**: kasumi with podman at
  `5426568` (`roottest-5426568.log`), and CI's ubuntu leg with docker
  (run 38126188058 and the head's). Every `rm` case matches GNU 9.11
  in status, standard error and what is left, as a user and as root,
  on both tiers, the sentinel intact — but two, by design:
  `--no-preserve-root /` is never handed to GNU, and this `rm` refuses
  it by name and removes nothing; `--no-preserve-root other` removes
  `other` in GNU and is refused here the same way.
- **`mv` and `cp` have no root rule of their own, and need none; they
  answer as GNU does**: `mv / x2` is `Device or resource busy`; `mv x
  /` and `cp x /` are `Permission denied` for a user and put `/x`
  there for root; `-T x /` is `cannot overwrite directory '/' with
  non-directory 'x'`; `mv / /` is `'/' and '/' are the same file`
  (this `mv` said `'//'`, fixed in `296e2e2`); `cp / x2` is `-r not
  specified; omitting directory '/'`; `cp -r other /` copies the tree
  into `/` for root. `cp -r /` itself is not a case: GNU copies a
  whole file system there, and so would this.
- **The planted break**, on a branch made for it and deleted after
  (`bu21-plant-root`; its workflow ran the container test and nothing
  else, so the planted program ran nowhere but in containers). With
  the OPERAND's verdict no longer acted on, the test stayed green —
  run 38126496783, 178 passed — because the walk's own fence
  (`bore.record_is_root`) refuses the same directory in the same
  words: two fences, and the first plant showed the second. With both
  out, run 38126834896 went red: **40 failed, 138 passed**, the forty
  being the ten spellings of the root, as a user and as root, on both
  tiers, each with the sentinel gone (`intact=False`, megabytes of
  `cannot remove`), and every other case — the dots, the link without
  a slash, `--no-preserve-root`, `mv`, `cp` — still green. The log is
  nomad-1 `~/lanes/bu21/ev/ci-plant2-38126834896.log`
  (`efa5adbbd099…`). A first take of that plant, run 38126625157, was
  red with one FAIL line and no more: the tool printed three megabytes
  of standard error on one line and the report ended there; it shows a
  failing case's standard error by its head now (`5426568`).
- **Not run, by name:** `rm -rf /*` (the shell expands it; `rm` sees
  ordinary directories); GNU with `--no-preserve-root /`; any of this
  on macOS.

## What the next boreutils lane inherits

- **Six changes, and a rule for the seventh.** `mkdir`, `rmdir`, `rm`,
  `mv`, `cp` stand on `fs_create_dir`, `fs_remove_dir`, `fs_remove`,
  `fs_rename`, `fs_open_mode` and `fs_copy_chunk`. When a builtin for
  a mode, a time, an owner or a link lands (wolf-lang#346, #698–#701),
  the skips that name it are the work list: `chmod`, `touch` and `ln`
  first, then `mkdir -m`, `cp -p`/`-a`/`-P`, and `mv` across file
  systems, which is `cp -a` and `rm -r`.
- **`src/bore/change.lu`**: the root and dot refusals, `same_file`,
  `join_name`, `last_name`, `said_yes`, `order_by`. `chmod -R`, `chown
  -R`, `du` and `find` want the same walk `rm` has; `install` wants
  `cp`'s.
- **The harness stands a changer in a checked scratch directory and
  refuses the rest**, and it compares what `ls -l` would see (`tree`).
  A new utility that changes the file system joins `CHANGERS` in
  `tools/difftest`. `tools/bench` has `prepare`, `{work}` and
  `--input`.
- **What no case can stage is in `~/lanes/bu21/gx.sh` and
  `ptyrun.py`'s shape**: a second file system (a btrfs subvolume under
  the lane's own directory) and a terminal on standard input. A
  `stdin_tty` key for `tools/difftest` would turn nine hand probes
  into cases.
- **GNU copies in inode order and removes in the directory's own.**
  btrfs hides the difference; ext4 and APFS do not, so a `-v` order
  that passes on kasumi is not yet a pass.
- **Owed:** `--preserve-root=all`; `mv -u`, `-b`; `cp -u`, `-b`,
  `--parents`, `-x`, `--attributes-only`; `rm` and `cp` under a path
  longer than the host's limit (#707); `cp -r`'s four `statx` a file,
  which are this program's to trim, beside the builtin's eleven
  (#709); the README's macOS bench column for these five.
