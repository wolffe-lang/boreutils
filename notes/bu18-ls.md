# bu18 — ls

Lane note and contract. **Class:** long (boreutils), **Opus**. **Wave:**
53. Contract: `sprints/boreutils/12-ls/bu18-ls.md` in the planning repo
(`wolffe-lang/wolf` trunk, last touched by `ea6a010`). One deliverable:
boreutils' own `ls`, drop-in for GNU `ls` on the behaviour users and
scripts rely on, differential-tested against the staged GNU 9.11 oracle,
and runnable on PAX in place of busybox's `ls` (px12's M-PX3 substitution).
Templates: bu14 (a utility lane, `notes/bu14-the-small-surface-set.md`)
and bu08 (`notes/bu08-sort.md`).

§1, §2 and §3 were written 2026-10-08, after the base was measured, the
GNU binary was run black-box and wolf's directory surface was witnessed,
and before a line of `src/ls.lu` was written or any bench was run.

## 1. Forbidden, absolutely

- **Never read, copy or translate GNU coreutils source** (the licence
  rule). `ls` is written from POSIX.1-2024's `ls` page, GNU's `--help`
  shape and the info manual's option descriptions, and black-box runs of
  the staged GNU 9.11 binary on kasumi (`.gnu-bin/`) and Homebrew's
  `gls` 9.11 on nomad-1; uutils (MIT) and toybox (0BSD) as design
  references only. GNU's `--help` prose is not copied: `--help` and
  `--version` are ours and their cases compare the exit status only.
- No `extern "c"`: pure wolf over the host builtins and std. A missing
  primitive is filed upstream with a witness and named where a reader
  meets it; a behaviour this program cannot match is a stated skip in
  the case file or a refusal by name, never an imitation that happens to
  pass.
- **Terminal detection waits for wolf 0.2.26** (s215's `os_isatty`, in
  r31). Until then `ls` behaves as GNU does when standard output is not
  a terminal: one entry per line, no colour, names printed as they are;
  `-C`/`-x` take `COLUMNS`, `-w`, or 80. The tty-dependent defaults are
  PENDING with the primitive named.
- No `rm` outside `~/lanes/bu18/` on kasumi, this lane's worktree
  (`boreutils-bu18`) and this session's scratchpad; nothing under
  `~/.claude`; no `git add -A`; no edit to another lane's file; pax is
  read-only (its harness runs from a copy in `~/lanes/bu18/`).
- No build on nomad-1. Builds, difftests and the bench run on kasumi,
  detached with `setsid nohup … & echo $! > pid`, waited on in a loop
  that prints at least every five minutes. The PAX binary is built in
  px12's Ubuntu 24.04 container, never with kasumi's CachyOS glibc.
- A full `tools/bench` is ~5.5 h: only `ls` is benched, against GNU, at
  load ~1.
- No merge, no rebase-merge; no `2>/dev/null` on a checkout; the branch
  asserted before every commit. No commit or PR trailers of any kind.
- No "seen red" without a run id, sha, path or digest beside it. File
  checksums carry a trailing `…`. Cross-release binary compares strip
  debug and build-id first.

## 2. Inputs, re-derived against origin (2026-10-08)

| the contract says | origin says | verdict |
|---|---|---|
| boreutils trunk `8214ee8` (bu17) | `8214ee8`, "wolf-toolchain.toml: the bump note names wolf-lang#624"; worktree `boreutils-bu18` on branch `bu18` cut from it | holds |
| wolf 0.2.25 / lupin 0.1.48 | `wolf-toolchain.toml`: `wolf 0.2.25 (wolfgang, pin 6710f9e)`, lupin 0.1.48, std `0f74ec5`; kasumi `tools/fetch-toolchain` re-checked both digests (`81cfd77a…` lupin linux, OK) and staged std `0f74ec5` | holds |
| 27 utilities | `src/*.lu` minus `bore_test.lu`: 27, and **no `ls`** | holds |
| `bore`, `tools/difftest`, `gnu-oracle.toml`, the bench | present; `difftest` already gives a case a scratch directory with files, directories, links and modes (bu14), but **no way to set a time**, which `-t` needs; `tools/bench` generates files only, so a directory to list is a new input | holds, two harness additions owed |
| the oracle | `gnu-oracle.toml` 9.11 under `LC_ALL=C _POSIX2_VERSION=200112`; kasumi's own GNU is 9.12 since the 10-02 upgrade, so `tools/fetch-oracle` staged 9.11 into `.gnu-bin/` (44 s); nomad-1's Homebrew `gls` is 9.11 | holds |
| std's directory and stat surface: "`fs_list`/`fs_stat` or their names — re-derive" | the names are `fs_read_dir`, `fs_is_dir`, `fs_is_file`, `fs_exists`, `fs_size`, `fs_modified_ms` (path) and `fs_fstat` (handle), `[os.host.sigs]` and `[os.fs.fstat]` at v0.2.25; wolf-std `0f74ec5`'s `std.fs` wraps the same calls and adds nothing | **drift in names**, as the contract allowed |
| what it gives about owners, modes, times, links and inode numbers | **only `[kind, size, modified_ms]`**: kind 0 file / 1 directory / 2 other, size in bytes, mtime in milliseconds. No mode bits (wolf-lang#346, open), no link count, no owner or group, no inode (wolf-lang#536, open), no blocks, no atime or ctime, and **no `lstat`**: every path call FOLLOWS a symbolic link, and there is no `readlink` | measured, below |
| "user/group name lookup from `/etc/passwd`/`/etc/group` can be read as files" | true, and moot until a uid and gid can be read at all | — |

### wolf's directory surface, witnessed

kasumi, wolf 0.2.25 native, `~/lanes/bu18/wit/main.lu`, transcript
`~/lanes/bu18/wit/witness.txt`. A directory holding `a` (5 bytes), `ln ->
a`, `lnd -> d`, `dangling -> nope`, `zz`, `B`, the links' own times set
to 2020-01-01 with `touch -h`:

```
entry B
entry a
entry d
entry dangling
entry ln
entry lnd
entry zz
t/a: dir=false file=true exists=true size=5 mtime_ms=1791437834905
t/ln: dir=false file=true exists=true size=5 mtime_ms=1791437834905
t/lnd: dir=true file=false exists=true size=0 mtime_ms=1791437834903
t/dangling: dir=false file=false exists=false size=-1 mtime_ms=-1
read_dir u (holds a non-UTF-8 name): utf8
--- GNU stat (lstat) of the same entries:
t/a regular file 5 1791437834
t/ln symbolic link 1 1577854800
t/lnd symbolic link 1 1577854800
t/dangling symbolic link 4 1577854800
```

So: `fs_read_dir` answers names only, without `.` and `..`, **already
sorted by byte** (the runtime sorts: `crates/wolf_rt/src/fs.rs`
`__wolf_rt_fs_read_dir`, `names.sort()`), and **one non-UTF-8 name fails
the whole listing** with `utf8`. A link is indistinguishable from its
target; a dangling link exists in its directory's listing and nowhere
else.

### What GNU `ls` does when standard output is not a terminal (black-box, 9.11)

kasumi `~/lanes/bu18/probe1.sh`, `probe2.sh` (transcripts are their
output). The facts the design rests on:

- One name per line by default; `-C`/`-x` fill columns to `COLUMNS`, then
  `-w`, then 80, and pad with **tabs** at 8-column stops (`-T 0`: spaces);
  `-m` wraps at the same width. The last of `-1 -C -x -m -l` wins, so does
  the last of `-a`/`-A`, and the last of `-S`/`-t`.
- Names are printed raw (a newline in a name is a newline); `-q` prints
  each non-printable byte as `?` — in the C locale every byte of `é`.
- Operands: files first, then each directory under a `name:` header
  separated by blank lines; a single directory operand gets no header
  unless `-R`. A command-line link to a directory is FOLLOWED unless
  `-d`, `-F` or `-l`; inside a listing a link is never followed (`-p`
  gives `lnd` no slash, `-F` gives every link `@`).
- Statuses: **2** for an operand that cannot be accessed or a directory
  operand that cannot be opened, and for a bad option or `-w` value;
  **1** for a subdirectory `-R` cannot open, for a dangling link under
  `-L`, and for `--sort=`/`--time=`/`--format=` arguments argmatch
  refuses (measured 1, not 2); 0 otherwise.
- `ls: cannot access 'nope': No such file or directory`,
  `ls: cannot open directory 'locked': Permission denied`,
  `ls: invalid line width: 'abc'`, and the getopt and argmatch shapes
  `bore` already writes.

### The base

kasumi, trunk `8214ee8`, `~/lanes/bu18/gauntlet.sh` (bu17's, re-pathed)
into `~/lanes/bu18/ev/gauntlet-base-8214ee8.log`: **2749 passed, 0
failed, 32 skipped**, every step exit 0, sorted verdict list
`verdicts-base-8214ee8.txt` sha256 `6f8d7f2d…` — bu17's figure, held.
(Filled in after the prediction's commit, when the run finished.)

## 3. Prediction (committed before the first change)

### P1. The option set

**Covered** (each with differential cases):

- listing: `-a --all`, `-A --almost-all`, `-d --directory`, `-R
  --recursive`, `--` and operands in GNU's order (files, then
  directories with headers);
- format: `-1`, `-C`, `-x`, `-m`, `--format=across|horizontal|commas|
  vertical|single-column`, `-w N`/`--width=N`, `COLUMNS`, `-T N`/
  `--tabsize=N`;
- sorting: by name in the C locale (byte order), `-r --reverse`, `-S`,
  `-t`, `-X`, `--sort=name|size|time|extension`, `--time=mtime|
  modification`, `--group-directories-first`;
- indicators: `-p`, `-F --classify` (`/` for a directory, `@` for a
  dangling link);
- names: `-q --hide-control-chars`, `--show-control-chars` (the non-tty
  default);
- links: `-H --dereference-command-line`, `-L --dereference`,
  `--dereference-command-line-symlink-to-dir` (the default);
- accepted with no visible effect without `-l`/`-s`: `-h
  --human-readable`, `-k --kibibytes`, `--color=never|auto` (auto is
  never off a terminal);
- `--help`, `--version`; GNU's statuses 0/1/2 and diagnostic shapes.

**Deferred**, each refused BY NAME (status 2, the primitive in the
message) rather than ignored, and each with skipped cases naming the
issue:

- the long format and everything that implies it — `-l`, `-g`, `-n`,
  `-o`, `--full-time`, `--format=long|verbose`: no mode, link count,
  owner, group or `readlink` (to be filed); the time columns and
  `/etc/passwd` lookups would follow the primitive in one lane;
- `-i` (wolf-lang#536), `-s` (no block count), `-u`, `-c`,
  `--time=atime|ctime|birth` (no atime, ctime or birth time);
- `-U`, `-f`, `--sort=none`: directory order is lost because
  `fs_read_dir` sorts (to be filed);
- `-v`, `--sort=version`, `--sort=width`, `-b`, `-Q`, `-N`,
  `--quoting-style`, `-I`/`--ignore`, `--hide`, `-B`, `-D`, `-Z`,
  `--color=always`, `--hyperlink`, `--zero`, `--block-size`, `--si`,
  `--author`, `-G`: not this lane (no primitive missing; scope);
- every behaviour that needs to know a LINK from its target: `-p`/`-F`
  on a link that resolves (GNU: no slash / `@`), `-S`/`-t` on a link
  (GNU sorts by the link's own size and time), `-R` meeting a link to a
  directory (GNU does not descend);
- the terminal defaults (columns and `-q` on a terminal): PENDING
  `os_isatty`, wolf 0.2.26.

### P2. Counts

- **200 ± 40 differential cases** in `tests/cases/ls.toml`, of which
  **40 ± 15 are skips** naming an issue or the pending primitive, and
  **0 fail** on either CI leg. The suite total grows from bu17's 2749 /
  0 / 32 (ubuntu) by exactly the new cases, with every old verdict
  unchanged.
- Release and dev tiers give the same verdict list on kasumi.

### P3. Gaps filed upstream

**Two** wolf-lang issues, each with the witness above:
1. **a link-aware stat record**: `lstat`'s kind (link vs target), mode,
   link count, uid, gid, blocks, atime and ctime, and `readlink` — what
   `ls -l`, `-F`, `-p`, `-S`, `-t` and `-R` need on a link; cross-linked
   to #346 (modes) and #536 (identity);
2. **a directory listing as `ls` needs it**: the directory's own order
   (`-U`), names that are not UTF-8 (today one such name fails the
   listing), and the entry's type without a stat.

Not filed: user and group names (`/etc/passwd` and `/etc/group` are
files wolf can read), the local time zone (the TZif file is readable;
only `-l` needs it).

### P4. PAX

A static `ls` built in px12's container runs on pax trunk's initramfs
under px12's harness and prints **byte-identically to the same binary on
Linux** for `ls /` and `ls -a /bin`, first boot, with **no system call
busybox's `ls` did not already make** (`getdents64`, `openat`, `statx`
or `newfstatat`). `ls -l /etc` is refused by name on both sides,
identically (status 2, the same message), because `-l` is deferred; the
PAX syscalls `-l` will need (`newfstatat`/`statx` with the mode and ids,
`readlinkat`) are named for px14/px15 rather than exercised.

### P5. The bench

On kasumi, release tier, against GNU 9.11, a generated tree of 20,000
files in 100 directories: plain `ls` of one 10,000-entry directory at
**0.5–1.2x** GNU's speed (neither side stats an entry; ours allocates a
`str` per name and sorts twice), `ls -R` of the tree at **0.3–0.7x**
(GNU knows a directory from `getdents64`'s type; this `ls` must
`fs_is_dir` every entry), and `ls -C` within 10% of plain `ls`.

## 4. Evidence index

Shas are this branch's (`bu18`, wolffe-lang/boreutils); kasumi paths are
under `~/lanes/bu18/` and stay there with the lane's evidence.

### The commits

- `00662c5` §1–§3, before any change.
- `bff34ab`, `814446b`, `f7208cd` — `tools/difftest`: `scratch_times`
  (an entry's mtime, set without following a link and read back),
  `[tree.NAME]` fixtures, and unlocking a mode-0 directory before the
  tree is emptied (the first `ls` run died in `rmtree` on one).
- `9ad9fe1` — `src/bore/columns.lu`, the `-C`/`-x`/`-m` layout, and 22
  assertions in `src/bore_test.lu`, every expectation read off GNU.
- `1c29aae` — `src/ls.lu` and `tests/cases/ls.toml` (265 cases).
- `7f60406`, `16cd6c3`, `05af69c` — `ls` asks a stat only what the
  listing needs, a region per directory, one sort buffer pair; two loop
  cases.
- `595780c`, `e7c3919`, `40b3353`, `620cb33` — the bench's `tree` input,
  `tests/bench/ls.toml`, a `sync` before timing.
- `ccf71b5` the planted break, `b235767` its revert (the tree at
  `b235767` is byte-identical to `620cb33`'s).
- `a3ab4e3` README, `d90f90a` CLAUDE.md, `7a44cc3`/`5b15662` these
  notes, `3fd2a53`/`a16620b` the eight cases that name 9.11.

### Case counts by option (tests/cases/ls.toml at `d90f90a`)

| section | pass | skip |
|---|---:|---:|
| which names (`-a -A -d`, `--all`, `--almost-all`, `--directory`) | 16 | 0 |
| operands (files then directories, headers, `--`, missing, ENOTDIR, `POSIXLY_CORRECT`) | 25 | 0 |
| formats (`-1 -C -x -m`, `--format=`, the last wins, `-l` then `-C`) | 24 | 1 |
| widths and tabs (`-w`, `--width`, `COLUMNS`, `-T`, `--tabsize`) | 35 | 0 |
| sorting (`-r -S -t -X`, `--sort=`, `--time=`, `--group-directories-first`) | 35 | 0 |
| indicators (`-p -F`, `--classify[=]`, `--file-type`, `--indicator-style=`) | 18 | 0 |
| names (`-q`, `--hide-control-chars`, `--show-control-chars`) | 6 | 0 |
| recursion (`-R`, `--recursive`) | 15 | 0 |
| unreadable places (status 2 and 1) | 6 | 1 |
| links (`-H -L`, dangling, a loop) | 25 | 11 |
| the deferred: the long format, `-s -i -u -c -U -f --sort=none`, the terminal | 0 | 17 |
| the rest (`-h -k`, `--color=never|auto|none|bogus`) | 9 | 0 |
| usage errors (getopt's shapes, ambiguous abbreviations in GNU's order) | 19 | 0 |
| write errors (`>&-`, `/dev/full`: status 2) | 4 | 0 |
| **all** | **237** | **30** |

Eight of the 237 name `gnu_min = "9.11"` (the field's 9.4 differs; they
run on every verdict leg, which is 9.11 everywhere).

Skips by cause: wolf-lang#625 23, #625 and #536 together 1, #536 1,
#626 3, #407 1, `os_isatty` (wolf 0.2.26) 1.

### The gauntlet, both tiers

kasumi, `~/lanes/bu18/gauntlet2.sh` (bu17's gauntlet plus the dev tier's
difftest) on a fresh clone at each head:

| head | release | dev | verdict list |
|---|---|---|---|
| `8214ee8` (base) | 2749 / 0 / 32 | — | `6f8d7f2d…` |
| `1c29aae` | 2985 / 0 / 61 | identical | `a4b3c5db…` |
| `d90f90a` | **2986 / 0 / 62** | **identical** | `b7154d32…` |

At `d90f90a` every step exits 0 (fetch, oracle, both builds — 28
utilities, 0 errors, 0 warnings — `wolf test`, fmt, the self-test, both
difftests); the non-`ls` verdicts are the base's line for line (`comm
-3` of the two lists, `ls:` lines removed: 0). `target/release/ls`
sha256 `2f425351…`.

### CI

- `1c29aae`: run **37735194630**, green (ubuntu 2985 / 0 / 61; macOS
  2944 / 0 / 102, the `/dev/full` and `/proc` cases).
- `e7c3919` 37736224641, `7f60406` 37736743565, `40b3353` 37736996327,
  `05af69c` 37737297289: green.
- **The planted break, `ccf71b5`** ("`-r` leaves the name order of ties
  alone"): run **37737397450**, red on both verdict legs — ubuntu job
  113179963781 (`difftest: 2980 passed, 6 failed, 62 skipped`) and
  macOS job 113179964191 (`2939 passed, 6 failed, 103 skipped`) — the
  same six cases on each and on kasumi
  (`~/lanes/bu18/ev/plant-ccf71b5-kasumi.log`): `-r`, `--reverse`,
  `-S -r`, `-X -r`, `--group-directories-first -r`, `-R -r`.
- The revert onward, green: `a3ab4e3` 37737654415, `d90f90a`
  37737681436, `5b15662` 37738019072 (ubuntu 2986 / 0 / 62, macOS
  2945 / 0 / 103), `a16620b` 37738654818 (the same). The head's own run
  is in the PR body.
- The `field` leg (ubuntu's own 9.4, information): `5b15662` showed
  eight `ls` cases where 9.4 answers otherwise (no `--sort=name`, the
  `--sort` words in another order, no sort on `--time=mtime` alone);
  `3fd2a53` names them `gnu_min = "9.11"`, and the leg's failures went
  back to trunk's 15 (run 37738654818).

### The column layout, swept

`notes/bu18/ls-columns-sweep.py`: random directories (letters, digits,
punctuation, a space, a newline, a tab, `\x01`, `é`), `-C`, `-x` and
`-m` at every width 1–29 and 40, 57, 80, 0, under `-T 0`, `-T 3`, the
default and `-q`, GNU against this `ls`: **47,520 runs over four seeds,
0 differences** (seeds 1 and 7 at `1c29aae`'s tree before it was
committed, 3 at `7f60406`'s, 11 at `d90f90a`). The first run found
`-w 0` (one line, never a grid: 172 of 15,840 differed); the tab rule
(no tab that moves one column) was found by hand before it.

### wolf's surface, the witness

`~/lanes/bu18/wit/main.lu` and `witness.txt` (§2): filed as
**wolf-lang#625** (no `lstat`, `readlink` or stat record) and
**wolf-lang#626** (`fs_read_dir` sorts, fails on one non-UTF-8 name,
gives no entry type).

### PAX

pax trunk `644ef64` cloned to `~/lanes/bu18/pax`, read-only to pax:
`notes/bu18/pax-mpx3-with-ls.patch` is the whole change (the pin at this
branch's head, `ls` among `UTILS`, twelve `ls` lines on the run list).
Built in px12's container (`px12-ubuntu`, Ubuntu 24.04, glibc 2.39) by
pax's own `tools/mkboreutils` from boreutils at the pinned sha, booted on
kasumi (TCG), four legs (native and release kernel × BIOS and UEFI):

- **Run 3, at `d90f90a`: B1–B5 PASS on all four legs, 29 commands**,
  every one byte-identical to the same binary on Linux, statuses
  included (`~/lanes/bu18/ev/pax-run3/`; the release-UEFI transcript is
  `notes/bu18/pax-run3-release-uefi.serial.log`, `9e535d83…`). The
  static `ls` is `e177ec39…`, 11,952,032 bytes. The `ls` lines: `/etc`,
  `-l /etc` (refused, status 2, the same message), `-a /bin`, `-F /etc
  /bin`, `-R /etc`, `-a -C -w 40 /bin`, `-x -w 30 /bin`, `-m /bin`, `-d
  /etc /bin/ls /etc/motd`, `-S -r /etc`, `/nothing /etc` (status 2),
  `-d /`. B4: no system call PAX lacks (`-ENOSYS` only for
  `set_robust_list` and `rseq`, as for every boreutils binary).
- **Run 2, at `1c29aae`** (`~/lanes/bu18/ev/pax-run2/`): the same list,
  20 PASS, 0 FAIL.
- **Run 1, at `1c29aae`, `ls /` itself** (`~/lanes/bu18/ev/pax-run1/`):
  PAX prints `bin dev etc`, Linux `bin dev etc proc` — **pax's
  `tools/linux-run` mounts `/proc` into its chroot** (line 115) and PAX
  has no `/proc`, so `ls /` cannot agree under that harness whatever
  `ls` does; `ls -F /` differs the same way, and `ls -t -p /` because
  PAX's `statx` answers one time for every initramfs entry (PAX lists
  `bin/ dev/ etc/` by name; Linux orders by its mount times). Every
  other line of run 1 was byte-identical. Run 2 and 3 therefore list
  `-d /` and the directories under `/` rather than `/`.
- System calls on Linux for the `ls` lines (`tools/linux-run --strace`):
  `arch_prctl brk close execve exit_group fstat getdents64 getrandom
  mprotect openat prlimit64 readlinkat rseq set_robust_list
  set_tid_address statx write` — busybox's `ls` set less `getuid`,
  `ioctl`, `prctl` and `newfstatat`, plus `statx`, which boreutils' `cat`
  already made.

### The bench

kasumi, load under 1, release tier, GNU 9.11, `tools/bench --scale 10
--runs 20 ls`, `ls` built from `05af69c` (whose `src/` is `d90f90a`'s),
twice (`~/lanes/bu18/ev/bench-ls-s10e.md`, `-s10f.md`): flat/ is 100,000
names, deep/ 316 directories of 316.

| row | boreutils | GNU | GNU / boreutils |
|---|---:|---:|---:|
| flat/, one per line | 34.4 / 35.2 ms | 78.1 / 78.6 ms | **2.27x / 2.23x** |
| flat/, `-C` | 37.5 / 37.3 ms | 92.8 / 92.0 ms | **2.48x / 2.46x** |
| flat/, `-S` | 110.9 / 111.5 ms | 106.5 / 108.0 ms | 0.96x / 0.97x |
| flat/, `-t` | 111.3 / 111.0 ms | 76.9 / 77.3 ms | 0.69x / 0.70x |
| `-R` of deep/ | 84.3 / 83.4 ms | 34.9 / 32.8 ms | 0.41x / 0.39x |
| start-up, `-d` | 0.4 ms | 0.4 ms | tie |

The road there, measured: at `1c29aae` (four stats per name under
`-S`/`-t`, every listing kept) `-S` 0.70x, `-t` 0.50x, `-R` 0.34x and
peak RSS 69 MB flat / **70 MB `-R`** against GNU's 28 MB / 2.2 MB
(`ev/rss.txt`); at `05af69c` 37 MB / **2.8 MB**. At `--scale 1` the
rows sit under hyperfine's shell-calibration floor (±5 ms on ~10 ms,
`bench-ls-1.md`…`-6.md`), which is why the rows of record are at 10.

### Issues filed

- wolf-lang#625 — fs: no lstat, readlink or full stat record.
- wolf-lang#626 — fs_read_dir sorts, fails the whole listing on one
  non-UTF-8 name, and gives no entry type.

## 3, against the result

| predicted | measured |
|---|---|
| P1: the covered set and the deferred set as listed | **held, with additions**: `-m`, `--format=commas`, `--indicator-style`, `--file-type` and `--color=none` covered; `-1` does not undo `-l` (GNU's rule, kept); `--classify=never` and `=auto` change nothing, not even an earlier `-F` (measured, kept). Deferred exactly as listed |
| P2: 200 ± 40 cases | **267** — outside the band, high |
| P2: 40 ± 15 skips | **30** — inside |
| P2: 0 fail on either CI leg; old verdicts unchanged | **held**: green at every head but the plant's; non-`ls` verdicts identical to the base's |
| P2: release and dev give the same verdict list | **held** at `1c29aae` and `d90f90a` |
| P3: two wolf-lang issues, the stat record and the listing | **held**: #625, #626 |
| P4: `ls /` and `ls -a /bin` byte-identical on PAX, first boot | **half**: `ls -a /bin` and eleven more lines identical on the first boot; `ls /` differs by `proc`, which pax's Linux harness mounts and PAX lacks — a harness asymmetry, not `ls` |
| P4: no system call busybox's `ls` did not make | **wrong by one**: `statx` (busybox uses `newfstatat`); PAX already serves it for `cat` |
| P4: `ls -l /etc` refused identically on both | **held** (status 2, byte-identical) |
| P5: plain `ls` 0.5–1.2x | **wrong, in the good direction: 2.27x** |
| P5: `-R` 0.3–0.7x | **held at 0.41x** (0.34x before the stat diet) |
| P5: `-C` within 10% of plain | **held**: 37.5 against 34.4 ms |

## 5. Done-when

- [x] Branch `bu18` on origin; PR wolffe-lang/boreutils#23, unmerged.
- [x] CI green at the head (run id in the PR body); the planted break
  red by run id (37737397450) and reverted.
- [x] `os_isatty`: wolf 0.2.26 (r31) was **not released** while this
  lane was open (latest v0.2.25), so the terminal defaults stay PENDING
  and nothing adopts it; a follow-up after r31.
- [x] Issues filed: wolf-lang#625, #626. Close nothing.
- [x] kasumi: `~/lanes/bu18/` keeps the evidence; its `target/`
  directories and the PAX build directory pruned; no process of this
  lane left running. The local worktree removed.
