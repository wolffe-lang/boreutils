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
tools/fetch-oracle        # GNU coreutils 9.11, sha256-checked, if needed
tools/build               # every utility into target/release/
tools/difftest            # the differential suite against the oracle
tools/bench --scale 0.01  # hyperfine against GNU on generated inputs
```

GNU coreutils is the oracle and must be installed: natively on linux,
`brew install coreutils` on macOS, where the harness uses the
`g`-prefixed names. It must be the version `gnu-oracle.toml` names, and
`tools/difftest` says so and stops when it is not — see **The oracle of
record** below.

**Windows is out of scope.** The only byte-exact route to standard
input and output in wolf 0.2.14 is reopening `/dev/stdin` and
`/dev/stdout` (wolf-lang#405), which windows does not have. CI runs on
linux and macOS.

## Standard output, and the exit convention

Every boreutils program writes through one shared buffered writer, and
honours one convention, stated in full at the top of `src/bore/bore.lu`
and measured black-box against GNU:

- **A write that fails is status 1 and one diagnostic.** `basename a/b
  >&-` is `basename: write error: Bad file descriptor`, exit 1, exactly
  as GNU's is.
- **Writing nothing never fails.** `true >&-` is 0 and `false >&-` is 1,
  because neither writes a byte; `true --version >&-` is 1.
- **A broken pipe is not the program's business.** `yes | head -1` dies
  of SIGPIPE with status 141 and an empty stderr on both sides. wolf
  cannot observe or ignore SIGPIPE at all (wolf-lang#423), and for this
  shape the default disposition is the right answer, so nothing here
  works around it.

Two things GNU says that boreutils cannot yet say. The reason text
after a failed write is `strerror(errno)`, and wolf 0.2.14 carries no
errno text behind an `io` row (wolf-lang#407), so a full disk is
`write error: Input/output error` here against GNU's `write error: No
space left on device`; the status is the same and the differential case
compares it. And on linux, when standard output is a socket, the
`/dev/stdout` reopen is refused and output falls back to `print_raw`,
which discards write errors (wolf-lang#408) — output still arrives, but
a write error on that one path is invisible.

## The oracle of record

`gnu-oracle.toml` names the GNU coreutils release boreutils is drop-in
for. It is **9.11**, and it is the pin that makes "drop-in" mean
something: GNU releases differ from each other, ubuntu-latest ships 9.4
where Homebrew and Arch ship 9.11, and a differential suite whose
verdict depends on which host ran it is a matrix rather than an oracle.

- `tools/difftest` **asserts** the version and returns no verdict
  against any other. `BORE_ORACLE_ANY=1` runs anyway and says on every
  run that the result is information.
- `tools/fetch-oracle` installs the oracle by sha256 digest where the
  host does not already ship it. CI does this and caches it.
- Where an older GNU still in the field behaves differently, the case
  names the range it describes with `gnu_min` / `gnu_max`, and CI's
  non-blocking `field` job runs the distro's own GNU so those ranges
  stay honest.

The oracle is a binary we run, never a source we read; building it
derives no boreutils code from GPL source.

## Status

Every utility below is byte-for-byte identical to GNU coreutils 9.11 on
its differential corpus, on both hosts: 421 differential cases,
macOS arm64 and linux x86-64. Four `wc` cases are skipped and say why in
the case file: two errno shapes that no wolf fs row can carry
(wolf-lang#407), and two code points whose display width the two hosts'
own `wcwidth` disagree about. Five more run only on a host with
`/dev/full`, which is how a write error on a LIVE descriptor is reached
at all, and so are skipped on macOS. Eight `wc` cases name the GNU
version they describe with `gnu_min`, because 9.4 counts words
differently from 9.11 — those cases are a record of the field, not of
the oracle, which is 9.11 everywhere the gauntlet runs.

"vs GNU" is wall-clock from `tools/bench`, GNU's time divided by ours,
so above 1.00 is faster than GNU. It is a measurement on a stated host,
never a promise, and the two hosts do not agree: GNU's `yes` is twice
as fast on linux as it is on macOS, so the same boreutils binary wins
on one and loses on the other. Both numbers are below; neither is "the"
number.

Release tier, 5 runs, GNU coreutils 9.11. `yes` writes 1 GiB of `y`
into `head -c`; the rest start up, write a few bytes and exit.

| bench | nomad-1 (macOS arm64, load 6.7) | kasumi (linux x86-64, load 1.6) |
|---|---|---|
| `yes`, 1 GiB | 238 ms vs GNU 652 ms (**2.74x**) | 198 ms vs GNU 124 ms (0.63x) |
| `echo`, one string | 1.9 ms vs GNU 2.0 ms (1.04x) | — |
| `basename`, one path | 1.6 ms vs GNU 1.7 ms (1.04x) | — |

`wc` has a table of its own too. Release tier, GNU coreutils 9.11, 5
runs, 256 MiB of generated text under `LC_ALL=C`, nomad-1 at load 13.9
and kasumi idle.

| bench | nomad-1 (macOS arm64) | kasumi (linux x86-64) |
|---|---|---|
| `wc -w` | 466 ms vs GNU 592 ms (**1.27x**) | 529 ms vs GNU 464 ms (0.88x) |
| `wc`, the default counts | 463 ms vs GNU 574 ms (**1.24x**) | 528 ms vs GNU 465 ms (0.88x) |
| `wc -l` | 174 ms vs GNU 160 ms (0.92x) | 128 ms vs GNU 22 ms (0.17x) |
| `wc -L` | 719 ms vs GNU 613 ms (0.85x) | 834 ms vs GNU 464 ms (0.56x) |
| `wc -c`, a file | 5.7 ms vs GNU 7.0 ms (1.23x) | 0.2 ms vs GNU 0.2 ms (tie) |
| `wc -c`, through `<` | 74 ms vs GNU 7 ms (0.10x) | 36 ms vs GNU 0.5 ms (0.01x) |

`wc` is the first utility whose flags had to be benched separately,
because each takes a different path, and the first whose locale had to
be stated: the C loop reads a byte where the UTF-8 loop decodes a
character, and under `LC_ALL=C.UTF-8` the same four rows read 0.91x to
0.95x on nomad-1 and 0.71x on kasumi.

Where the work is a byte-at-a-time state machine that GNU cannot
vectorize either — `-w`, and the default counts — wolf is ahead of C.
Where GNU reaches for SIMD it wins by a lot: `wc --debug -l` reports
`using avx512 hardware support` on kasumi, and no bulk byte scan is
expressible in pure wolf today (wolf-lang#411, filed with every
alternative measured). `-c` on a file operand is an `fstat` on both
sides, so it measures start-up; through a redirect GNU still `fstat`s
and we must read, because `wc -c` owes size minus the current offset and
wolf has no seek or tell (wolf-lang#405).

**Read the macOS column with its load.** nomad-1 was at load 13.9 with
other lanes on it, and contention flatters every ratio there, because
GNU's vectorized line counter loses more to a busy machine than our
scalar loop does: the same `-l` comparison read 0.55x at load 6.7.
kasumi was idle.

Memory is flat in the size of the input: counting 256 MiB peaks at
5.7 MB of RSS on nomad-1 against GNU's 1.8 MB, and 4.3 MB on kasumi
against 2.8 MB, and 16 MiB peaks at the same 5.7 MB. That costs one
`region` per chunk, and about 5% of the time; without it the same count
peaked at **271 MB**, because the ambient region never frees what each
read allocates (wolf-lang#416). `-c` never reads at all and peaks at
1.7 MB.

`cat` has a table of its own, because it is the first utility that moves
bulk data and the two hosts disagree sharply about it. Release tier, GNU
coreutils 9.11, 10 runs (50 for start-up), nomad-1 at load 7.4 and
kasumi at load 5.9. The large file is 256 MiB of text; the short-line
file is 16 MiB of nought-to-seven-letter lines.

| bench | nomad-1 (macOS arm64) | kasumi (linux x86-64) |
|---|---|---|
| `cat`, start-up | 1.82 ms vs GNU 2.14 ms (**1.18x**) | 0.26 ms vs GNU 0.25 ms (0.97x) |
| `cat`, 256 MiB to /dev/null | 27.4 ms vs GNU 17.6 ms (0.64x) | 54.1 ms vs GNU 8.5 ms (0.16x) |
| `cat`, 256 MiB to a file | 591 ms vs GNU 569 ms (0.96x) | 123 ms vs GNU 86 ms (0.70x) |
| `cat -n`, 16 MiB of short lines | 94.2 ms vs GNU 54.1 ms (0.57x) | 232 ms vs GNU 61.5 ms (0.26x) |

So `cat` starts up level with GNU on both hosts and loses on bulk
copying, by 1.6x on macOS and by 6x on linux. GNU moves the bytes
without a round trip through user space where the host allows it, and
wolf 0.2.14 exposes neither `splice` nor `copy_file_range`, so every
byte we copy is read into a list and written back out.

Memory is level, and flat in the size of the input either way: copying
256 MiB peaks at 2.4 MB of RSS on nomad-1 against GNU's 1.9 MB, and at
2.8 MB on kasumi against 2.3 MB; `cat -n` peaks at 3.9 MB against
2.2 MB, and at 3.7 MB against 2.7 MB. That costs one `region` block per
chunk — without it the same copy peaked at 340 MB and `cat -n` at
1.1 GB, because the ambient region never frees what each read allocates.

| utility | status | vs GNU |
|---|---|---|
| `true` | done | start-up only |
| `false` | done | start-up only |
| `echo` | done | 1.04x (macOS) |
| `basename` | done | 1.04x (macOS) |
| `dirname` | done | start-up only |
| `yes` | done | 2.74x (macOS), 0.63x (linux) |
| `cat` | done | start-up 1.18x (macOS), 0.97x (linux); bulk copy 0.64x, 0.16x |
| `wc` | done | `-w` 1.27x, `-l` 0.92x (macOS, load 13.9); 0.88x, 0.17x (linux) |
