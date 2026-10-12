# boreutils — agent guidance

GNU coreutils rewritten in pure wolf, one program at a time. Each
utility is a drop-in replacement for the behaviour users and scripts
rely on, and is differential-tested against the GNU binary.

## The licence rule (read before writing a line)

**Never read, copy or translate GNU coreutils source.** It is GPL-3.0
and owned by the FSF; a wolf program translated from it would be a
derivative this project does not wholly own. Write each utility from:

- the POSIX.1-2024 utility specification;
- GNU's documented behaviour: `--help`, the info manual's option
  descriptions, and black-box runs of the GNU binary;
- uutils/coreutils (MIT) and toybox (0BSD) as design references only.

Record in each utility's header which of these you consulted. Do not
copy GNU's `--help` text either: it is FSF's prose. `--help` and
`--version` take GNU's SHAPE in our own words, so their differential
cases compare the exit status only.

## Read before writing a line of wolf

1. `AN_AGENTS_GUIDE_TO_WRITING_GOOD_WOLF.md` in the planning repo
   (`wolffe-lang/wolf`, trunk) — current at this repo's pin, and its
   "Writing a command-line program" section is where every boreutils
   program starts.
2. Your sprint contract under the planning repo's `sprints/boreutils/`.
   Contracts are binding.
3. When this file and the wolf spec disagree, the spec wins.

## The repository

- **The pin** is `wolf-toolchain.toml`: wolf and lupin come from their
  release archives BY SHA256 DIGEST, never from a source build, and
  wolf-std is a source tree at a commit. `tools/fetch-toolchain` stages
  all three into `.wolf-bin/` and refuses on a digest mismatch;
  `tools/lib-toolchain.sh` refuses on identity drift.
- **The layout** is one package. A utility is `src/<name>.lu` carrying
  `//! member: false`, which makes it a standalone entry; the shared
  code is the module `src/bore/`, imported as `use bore`. Measured at
  0.2.14: `use` resolves module directories under the ENTRY's own
  directory, so entries and their shared module must sit side by side,
  and a second `main` in one directory is E0302.
- **`src/bore/`** holds option parsing in GNU's getopt_long shape,
  GNU-shaped diagnostics, and the buffered byte writer. A utility
  should be its own behaviour and nothing else.
- **The other pin** is `gnu-oracle.toml`, the GNU coreutils release
  boreutils is drop-in for (B44). `tools/difftest` asserts it and
  returns no verdict against any other version; CI installs it rather
  than taking what the runner ships.

## The exit convention (read it before writing output)

`src/bore/bore.lu`'s header states it in six rules, measured black-box
against GNU. The short form for a new utility:

1. `var out = bore.stdout()` BEFORE any input file.
2. All output through `bore.put` / `put_byte` / `write_all`; never
   `print` or `print_raw`.
3. End on `bore.finish(mut out, prog, status)`, and so does every early
   return that has written anything. **That is the whole convention on
   the common path** — a utility that buffers needs nothing else, and
   gets `prog: write error: Bad file descriptor` and status 1 on a
   closed standard output for free.
4. Report an inline write failure with `bore.write_error(out, prog,
   "write error")`, never a bare `bore.warn`, so the reason is named.
5. A program that STREAMS (only `cat` and `yes` today) calls
   `bore.output_ok(out, prog)` before it starts and returns 1 when it
   answers false. Measured: GNU checks standard output before it looks
   at its operands, and says `prog: standard output: …` when it does.
6. SIGPIPE is left alone. `prog | head -1` dies with status 141 on both
   sides, and wolf cannot observe or ignore the signal (wolf-lang#423).

## The tools

    tools/fetch-toolchain      stage the pinned toolchain into .wolf-bin/
    tools/fetch-oracle         install the oracle of record into .gnu-bin/
    tools/build [--dev] [name] compile utilities into target/<tier>/
    tools/check-fmt            wolf fmt --check
    tools/check-test           wolf test (the *_test.lu unit tests)
    tools/difftest [util...]   the differential suite against GNU
    tools/difftest-selftest    prove the harness can still see a difference
    tools/roottest             rm, mv and cp handed `/`, each case in a
                               throwaway container (docker or podman)
    tools/bench [--scale F]    hyperfine against GNU on generated inputs
                               (`prepare`, `{work}` and `--input` for
                               the programs that change what they run on)

## Hard rules

- **Tests are first-class and land in the same commit as the code.**
  Every flag a utility gains arrives with differential cases for it.
- The differential corpus is the oracle: a behaviour nobody wrote a
  case for is not implemented, however much source exists.
- A gap in wolf is FILED UPSTREAM with its witness (wolf-lang or
  wolf-std), named in the code where a reader meets it, and never
  silently worked around. This track is upstream's best bug-finder.
- Bench numbers state their host, the GNU version and the build tier.
  Speed is a finding per utility, never a promise.
- Commits: chunked, terse, imperative. Never `git add -A`. No commit or
  PR trailers of any kind, ever.
- Branch per lane, PR left unmerged; the orchestrator audits and
  fast-forwards.
- Ship `--release`. Bench inputs are generated, never committed, and
  deleted after the run.

## What wolf cannot do here yet

- Descriptors 0, 1 and 2 are read and written directly since wolf
  0.2.26 (`[os.fs.std]`); `bore.stdout()` still comes BEFORE any input
  file, because GNU checks standard output first.
- A non-UTF-8 argument aborts the runtime in `env_args`
  (wolf-lang#406), so no utility can handle one yet.
- `print`/`print_raw` discard write errors and are one `write(2)` per
  call (wolf-lang#408): use `bore.Out`.
- **What wolf can do to a file** (bu21's census, `notes/bu21/census/`,
  and wolf 0.2.28's s230, ruling #67): make a directory
  (`fs_create_dir`, or with a mode `fs_create_dir_mode`), remove an
  empty one (`fs_remove_dir`), unlink (`fs_remove`), rename
  (`fs_rename`, which names another file system by its own row,
  `cross_device`), create (`fs_open_mode`, or with a mode
  `fs_open_perm`) and write, copy bytes in the kernel
  (`fs_copy_chunk`), change a mode (`fs_set_mode`, following a final
  link), make a symbolic or hard link (`fs_symlink`, `fs_link`), set
  both times or either (`fs_set_times`, a link's own too), truncate a
  handle to a length (`fs_truncate`), and set the umask and be told
  the old one (`os_umask`; reading it is setting it and putting it
  back, `bore.current_umask`). The builtins are called directly:
  wolf-std's wrappers (wolf-std#62) are not in the std pin yet.
  NOTHING changes an owner (#701, and no user id: #633), makes a fifo
  or a device (#705), finds a hole (#703), renames without replacing
  (#706), names an entry relative to an open directory (#707), sets a
  link's own mode, sets times through a handle (#714) or reads a
  handle's open flags. A utility whose core operation is missing is
  left out, never faked; an option that needs one is refused by name.
  `fs_remove_dir_all` is never called: a recursive removal is `rm`'s
  own walk.
- **A MODE** (`chmod`, `mkdir -m`) is `src/bore/modes.lu`, measured
  against GNU 9.11; **a date** (`touch -d`, `-t`) is
  `src/bore/dates.lu`, which reads part of GNU's grammar and refuses
  the rest by name.
- **`rm`, `mv`, `cp`, `rmdir`, `mkdir`, `chmod`, `touch` and `ln` delete,
  overwrite or change, so they
  are run only where `tools/difftest` stands them**: a scratch
  directory it made under its root (`$BORE_SCRATCH_ROOT`, else the temp
  directory) and checked by prefix immediately before each side starts.
  The harness refuses the whole run when a case of one of them names
  `/`, a `~`, a `..` component or an absolute path outside `{scratch}`
  (`tests/refuse/` holds a plant per rule). **No test runs any `rm` on
  a HOST's `/`**, this one or GNU's. The refusal is `bore.rm_verdict`,
  a function, unit-tested in `src/change_test.lu`, and it is run as a
  program by `tools/roottest` and nowhere else: one throwaway container
  a case, no mount, no network, as a user and as root inside, both
  tiers beside GNU 9.11, a sentinel tree summed before and after
  (`tests/root/cases.toml`; CI's ubuntu leg, docker). By hand, the same
  rule: a fresh directory, its path checked, never a variable that
  could be empty — and `/` only through that tool.
- A scratch case compares `tree` beside `files` (bu21): every entry's
  kind, permission bits, link count and size, and a time older than the
  case. `umask = 0o077` runs both sides under a mask; the harness
  itself runs at 022. A changer's own name at the start of a line of
  standard output is `PROG` (`mkdir -v` says `mkdir: created …`, and
  GNU on macOS is `gmkdir`). `times = true` (bu22) adds a sixth field:
  every entry's access and modification time to the nanosecond, a
  link's own, with a time inside the side's own run read as `now` — so
  give an entry a fixture time (`"S.NNNNNNNNN"` takes nanoseconds) when
  the case is about it moving to now. `skip_on = { Darwin = "why" }`
  skips on one host by name. The changers' differential runs on a
  lane's host belong in a throwaway container (bu22 ran px12-ubuntu,
  no network, only the lane directory mounted).
- No pids (wolf-lang#141). The host's
  reason for an fs failure is `bore.io_error()` (`os_error_text`, wolf
  0.2.26): ask it before any other fs call, which clears it, or keep
  `bore.host_code()` and ask `bore.reason_of` later.
- A program can become another (`os_exec`) and remove a variable
  (`env_unset`) since wolf 0.2.27 (s225); `env` does. Two things are
  still missing there: `env_vars()` lists the environment only sorted
  and without an entry that is not UTF-8 (wolf-lang#535), and the os
  family leaves no error number behind, so a failed exec or `chdir` has
  a row and no reason (wolf-lang#682).
- `wrapping[u64]` interpolates its top-bit values as signed and cannot
  be divided on the native tier (wolf-lang#538): use `bore.u64_text`
  and `bore.u64_radix`.
- A case that must see a FILE a utility writes, or stand in a directory
  whose path it knows, uses `tools/difftest`'s scratch directory
  (`scratch`, `scratch_dirs`, `scratch_links`, `scratch_modes`,
  `scratch_times`, `cwd`, `{scratch}`); its `files` field is gated by
  `tests/selftest/tee.toml`. A tree many cases share is a `[tree.NAME]`
  table in the case file and `tree = "NAME"` in each case (bu18). Since
  bu20 a tree can hold pipes, sockets, hard links and holes
  (`scratch_fifos`, `scratch_sockets`, `scratch_hardlinks`,
  `scratch_sizes`), access times and times relative to "now"
  (`scratch_atimes`, `scratch_time_all`, `"now-N"`), and can be laid
  out ONCE for both sides (`scratch_keep`) where the answer is an inode
  or a status-change time; `mask` hides one named field on both sides.
- A file's whole record is `fs_stat`/`fs_lstat`'s twenty words since
  wolf 0.2.27 (s218); `src/bore/info.lu` names them, and `ls -l`,
  `stat` and `readlink` stand on them, with `fs_read_link` and
  `fs_read_dir_entries` (the directory's own order, each entry's type).
  What the record does NOT hold, each filed: the I/O block size
  (wolf-lang#684), any extended attribute, so no ACL or context mark
  (#685), the file system's own record (#686), and the record of an
  open handle past three words (#536's other half: `cat f >> f`,
  `stat -`). A name that is not UTF-8 can be listed and nothing else
  (#687), and the listing leaves out `.` and `..`, so `ls -f` cannot
  place them (#692).
- Owner and group NAMES come from `/etc/passwd` and `/etc/group`
  (`src/bore/ids.lu`): wolf has no account lookup. A case that prints
  one is `accounts = true` and has a numeric twin, because macOS keeps
  its users elsewhere.
- Local time is read from the zone's TZif file and its POSIX rule
  (`src/bore/clock.lu`); a canonical path is walked a component at a
  time (`src/bore/paths.lu`). Neither is a builtin.
- An `0o…` literal lowers on every tier since wolf 0.2.28 (#688); the
  code here still writes modes in decimal (`438` is 0666) and need not.
- The host is decided when a program is compiled:
  `bore.built_for_linux()` (`#[cfg(target = "…")]`), never by looking
  for `/proc`.
