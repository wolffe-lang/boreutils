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
    tools/bench [--scale F]    hyperfine against GNU on generated inputs

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
- No permissions (wolf-lang#346), no pids (wolf-lang#141). The host's
  reason for an fs failure is `bore.io_error()` (`os_error_text`, wolf
  0.2.26): ask it before any other fs call, which clears it, or keep
  `bore.host_code()` and ask `bore.reason_of` later.
- No exec, no environment unset or clear, and a spawned child's stdin is
  the null device (wolf-lang#534); `env_vars()` lists the environment
  only sorted (wolf-lang#535); no file identity, so two names or
  descriptors for one file cannot be recognised (wolf-lang#536).
- `wrapping[u64]` interpolates its top-bit values as signed and cannot
  be divided on the native tier (wolf-lang#538): use `bore.u64_text`
  and `bore.u64_radix`.
- A case that must see a FILE a utility writes, or stand in a directory
  whose path it knows, uses `tools/difftest`'s scratch directory
  (`scratch`, `scratch_dirs`, `scratch_links`, `scratch_modes`,
  `scratch_times`, `cwd`, `{scratch}`); its `files` field is gated by
  `tests/selftest/tee.toml`. A tree many cases share is a `[tree.NAME]`
  table in the case file and `tree = "NAME"` in each case (bu18).
- No `lstat`, no `readlink`, and nothing in a stat past kind, size and
  modification time: every path call follows a link (wolf-lang#625).
  `fs_read_dir` sorts its names, fails on one that is not UTF-8, and
  gives no entry type (wolf-lang#626).
