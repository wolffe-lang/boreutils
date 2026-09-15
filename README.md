# boreutils

GNU coreutils, rewritten in pure [wolf](https://github.com/wolffe-lang/wolf-lang),
one program at a time.

Each utility aims to be a drop-in replacement for the behaviour that
users and scripts rely on. Where wolf allows it, each also aims to be
faster than GNU. Speed is measured per utility and never promised.
GNU's `cat` and `wc` are already fast, so beating them counts as a
finding, not as a requirement.

## Why

- **A second large production wolf codebase, after
  [lobo](https://github.com/wolffe-lang/lobo).** The project is dozens
  of small, complete programs, each with one job. That makes it a good
  shape of wolf to learn from, whether you are a reader, a new
  contributor or a model.
- **Pressure on the OS and IO surface.** Coreutils need argv, exit
  codes, streaming byte IO on stdin, stdout and files, SIGPIPE,
  permissions, users and time. When a utility hits a gap in wolf, the
  gap is filed upstream with a witness.
- **Verifier-backed data.** GNU coreutils is the behavioural oracle.
  Every boreutils program is differential-tested against it.

## The licence rule

boreutils is **GPL-3.0-or-later** (see `LICENSE`).

**GNU coreutils source is never read, copied or translated here.** It
is GPL-3.0 and owned by the FSF, so a translation of it would be a
derivative that this project does not wholly own. Each utility is
written from these sources only:

- the POSIX.1-2024 utility specification;
- GNU's documented behaviour: `--help`, the info manual's option
  descriptions, and black-box runs of the GNU binary;
- the permissively licensed implementations, as design references
  only: [uutils/coreutils](https://github.com/uutils/coreutils) (MIT)
  and [toybox](https://landley.net/toybox/) (0BSD).

The header of each utility records which of these references were
consulted.

## Building it

The toolchain is pinned by digest and fetched, never built:

```sh
tools/fetch-toolchain     # wolf + lupin release archives, sha256-checked
tools/build               # every utility into target/release/
tools/difftest            # the differential suite against GNU coreutils
tools/bench --scale 0.01  # hyperfine against GNU on generated inputs
```

GNU coreutils is the oracle and must be installed: natively on linux,
`brew install coreutils` on macOS, where the harness uses the
`g`-prefixed names.

**Windows is out of scope.** The only byte-exact route to standard
input and output in wolf 0.2.14 is reopening `/dev/stdin` and
`/dev/stdout` (wolf-lang#405), which windows does not have. CI runs on
linux and macOS.

## Status

Every utility below is byte-for-byte identical to GNU coreutils 9.11 on
its differential corpus, on both hosts: 143 differential cases, macOS
arm64 and linux x86-64.

"vs GNU" is wall-clock from `tools/bench`, GNU's time divided by ours,
so above 1.00 is faster than GNU. It is a measurement on a stated host,
never a promise, and the two hosts do not agree: GNU's `yes` is twice
as fast on linux as it is on macOS, so the same boreutils binary wins
on one and loses on the other. Both numbers are below; neither is "the"
number.

Release tier, 5 runs, GNU coreutils 9.11. `yes` writes 1 GiB of `y`
into `head -c`; the rest start up, write a few bytes and exit.

| bench | nomad-1 (macOS arm64, load 8.8) | kasumi (linux x86-64, load 3.5) |
|---|---|---|
| `yes`, 1 GiB | 238 ms vs GNU 652 ms (**2.74x**) | 198 ms vs GNU 124 ms (0.63x) |
| `echo`, one string | 1.9 ms vs GNU 2.0 ms (1.04x) | — |
| `basename`, one path | 1.6 ms vs GNU 1.7 ms (1.04x) | — |

| utility | status | vs GNU |
|---|---|---|
| `true` | done | start-up only |
| `false` | done | start-up only |
| `echo` | done | 1.04x (macOS) |
| `basename` | done | 1.04x (macOS) |
| `dirname` | done | start-up only |
| `yes` | done | 2.74x (macOS), 0.63x (linux) |
| `cat` | next (bu01) | — |
| `wc` | next (bu02) | — |
