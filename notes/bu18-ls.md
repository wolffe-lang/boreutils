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
into `~/lanes/bu18/ev/gauntlet-base-8214ee8.log`: filled in below when it
finishes (bu17's own figure at this head: 2749 / 0 / 32 on ubuntu).

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
