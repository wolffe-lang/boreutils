# Contributing to boreutils

boreutils is GNU coreutils rewritten in pure
[wolf](https://github.com/wolffe-lang/wolf-lang), one program at a time. Each
utility is a drop-in replacement for the behaviour users and scripts rely on,
and is differential-tested against the GNU binary.

## The licence rule

**Never read, copy or translate GNU coreutils source.** It is GPL-3.0 and owned
by the FSF; a wolf program translated from it would be a derivative this
project does not wholly own. Write each utility from:

- the POSIX.1-2024 utility specification;
- GNU's documented behaviour: `--help`, the info manual's option descriptions,
  and black-box runs of the GNU binary;
- [uutils/coreutils](https://github.com/uutils/coreutils) (MIT) and
  [toybox](https://landley.net/toybox/) (0BSD), as design references only.

Record in each utility's header which of these you consulted. Do not copy
GNU's `--help` text either: `--help` and `--version` take GNU's shape in our
own words, so their differential cases compare the exit status only.

## The toolchain and the oracle

`wolf-toolchain.toml` pins the wolf compiler and the lupin interpreter by the
sha256 digest of their release archives, never a source build, and wolf-std
as a tree at a commit. `gnu-oracle.toml` pins the GNU coreutils release
boreutils is drop-in for, and the environment it runs in.

```sh
tools/fetch-toolchain    # stages wolf, lupin and std into .wolf-bin/, refusing a digest mismatch
tools/fetch-oracle       # installs the pinned GNU coreutils into .gnu-bin/, by digest
```

`tools/lib-toolchain.sh` refuses a toolchain whose identity drifts from the
pin, and `tools/difftest` gives no verdict against any GNU but the pinned one.
A pin moves in a commit of its own.

## Building and running the checks

```sh
tools/build                  # every utility into target/release/ (--dev: the fast backend)
tools/check-fmt              # wolf fmt --check
tools/check-test             # the *_test.lu unit tests
tools/difftest [util...]     # the differential suite against GNU
tools/difftest-selftest      # the harness can still see a difference
python3 ci/tiers-test.py     # CI's planner against its rules
```

The README's "Building it" section lists the rest, among them the container
suites below and `tools/bench`.

## How the code is laid out

- A utility is `src/<name>.lu` carrying `//! member: false`. The shared code is
  the module `src/bore/`, imported as `use bore`: option parsing in GNU's
  getopt_long shape, GNU-shaped diagnostics and the buffered byte writer. A
  utility is its own behaviour and nothing else.
- **The exit convention** is stated in full at the top of `src/bore/bore.lu`.
  In short: `var out = bore.stdout()` before any input file; all output through
  `bore.put`, `put_byte` or `write_all`, never `print`; end on
  `bore.finish(mut out, prog, status)`, as does every early return that has
  written anything; report an inline write failure with `bore.write_error`. A
  program that streams calls `bore.output_ok` before it starts. SIGPIPE is left
  alone.
- Name a signal by its meaning, through `std.signal` (`src/bore/signals.lu`
  shows how): never a meaning's bit, never a host's signal number.
- The host is decided when a program is compiled (`bore.built_for_linux()`),
  never by looking for `/proc`.
- A gap in wolf is filed upstream (wolf-lang or wolf-std) with a small program
  that shows it, named in the code where a reader meets it, and never silently
  worked around. A utility whose core operation wolf cannot do yet is left out,
  never faked; an option that needs one is refused by name.

## What a change must bring

- **Tests land in the same commit as the code.** Every flag a utility gains
  arrives with differential cases in `tests/cases/<util>.toml`. The corpus is
  the oracle: a behaviour nobody wrote a case for is not implemented.
- **Tests never touch the host.** `rm`, `mv`, `cp`, `rmdir`, `mkdir`, `chmod`,
  `touch` and `ln` run only in the scratch directory `tools/difftest` makes,
  and it refuses any case that names `/`, a `~`, a `..` component or an
  absolute path outside the scratch (`tests/refuse/`). Only `tools/roottest`
  hands `/` to a utility, inside a throwaway container. A case that sends a
  signal, runs a command under `timeout`, runs as another user or changes an
  owner runs through its own tool (`tools/killtest`, `tools/timeouttest`,
  `tools/idtest`), one throwaway container a case; no test signals a process
  it did not start.
- Bench numbers state their host, the GNU version and the build tier. Speed is
  a finding per utility, never a promise. Bench inputs are generated, never
  committed, and deleted after the run.

## Commits

- Chunked and terse, with an imperative subject: one file or one coherent
  change a commit. Stage what you mean, never `git add -A`.
- No trailers of any kind: no co-author, sign-off or "generated with" lines.

## Pull requests

Open a pull request from a branch against `trunk`. An unlabelled pull request
runs only a cheap check, so your own run of the checks is the evidence: the
description names the head you ran them on, their results, the GNU version
the differential ran against, and the cases the change adds. A change to CI,
`tools/` or a pin also needs the full CI set green at its head before it
merges: ask for the `full-matrix` label once the head is the one to merge, not
when the pull request opens.
