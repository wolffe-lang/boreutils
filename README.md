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

boreutils is **GPL-3.0-or-later** (see `LICENSE`). The wolf Training Data
Permission (see `LICENSE-TRAINING-DATA`) lets you train models on this
repository's text and ship excerpts of it in datasets under CC BY 4.0.

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
input and output in wolf 0.2.16 is reopening `/dev/stdin` and
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
after a failed write is `strerror(errno)`, and wolf 0.2.16 carries no
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
  host does not already ship it, with the configure line the pin file
  names. CI does this and caches it.
- Where an older GNU still in the field behaves differently, the case
  names the range it describes with `gnu_min` / `gnu_max`, and CI's
  non-blocking `field` job runs the distro's own GNU so those ranges
  stay honest.

**The pin is a version AND an environment** (B73). Two builds of one
coreutils release disagree about the obsolete `+N` operand form —
Arch's `tail +3` reads "from line 3" and Homebrew's reads `+3` as a
file name — because gnulib decides it from a value `configure` compiles
in. A pin file cannot name a build nobody published, and it does not
have to: `$_POSIX2_VERSION` overrides that value at run time, so
`[oracle.env]` in `gnu-oracle.toml` pins it beside `LC_ALL`, and every
build answers the same. `[oracle.probe]` then runs one command whose
answer the build-time default decides — `uniq +1 /dev/null` — and
`tools/difftest` refuses a verdict when the answer is not the one the
pin file declares, exactly as it refuses one against the wrong version.
On the `field` leg the probe is reported rather than enforced, which is
how B73 was found in the first place.

What that does NOT close is the other half: divergences that are the
two hosts' C LIBRARY rather than coreutils at all — `seq -f %a`, the
`strerror(ERANGE)` wording, the width table — and a build identity
would not have helped there either. Those stay recorded skips.

**A death on the `field` leg is loud, a difference is not** (B98). The
leg used to carry `continue-on-error` on the whole job, which made it
non-blocking about everything including its own death: it had been
dying of signal 13 with a partial report and reporting success. The
advisory now sits on the differential step alone, and
`tools/field-verdict` decides what an exit code means — 0 quiet, 1 an
advisory, a signal death or a harness refusal LOUD.
`tools/field-verdict-selftest` gates that, planting a real SIGPIPE
death of the harness on every CI run.

The oracle is a binary we run, never a source we read; building it
derives no boreutils code from GPL source.

## Status

Every utility below is byte-for-byte identical to GNU coreutils 9.11 on
its differential corpus. The corpus holds **1,772 cases**; a run on
kasumi (linux x86-64) at this pin answers **1,753 passed, 0 failed, 19
skipped**, and macOS skips five more that need `/dev/full`. The corpus
and the run are stated separately on purpose: an earlier edition of this
paragraph called the passing count the case count, which quietly
subtracted the skips from the corpus instead of naming them.

Four `wc` cases are skipped and say why in
the case file: two errno shapes that no wolf fs row can carry
(wolf-lang#407), and two code points whose display width the two hosts'
own `wcwidth` disagree about. Five more run only on a host with
`/dev/full`, which is how a write error on a LIVE descriptor is reached
at all, and so are skipped on macOS. Nine `wc` cases name the GNU
version they describe with `gnu_min` — those are a record of the field,
not of the oracle, which is 9.11 everywhere the gauntlet runs. The
ninth was found by the `field` leg on the first run it ever made: with
descriptor 1 closed, 9.11 stops at the first write that fails and 9.4
keeps walking, so `wc FILE nope >&-` names the missing file on 9.4 and
not on 9.11.

**The transform set adds eight more skips, all the same shape, and none
of them a coreutils version difference.** They are places where the two
hosts' C LIBRARIES disagree at one coreutils release, or where GNU's
long double gives an answer exact arithmetic does not: `seq -f %a`,
`seq 1 1 1e400`, `seq 1e30 …` and two long-double stalls, `nl -w 0`'s
`strerror(ERANGE)` wording, and one BRE construct `nl` here does not
implement. Each names both hosts' answers in its own `skip` line.

**It used to be nine, and `uniq +1` was the ninth.** That one was a
BUILD-TIME POSIX2 setting rather than a release, so Arch read `+1` as
"skip one character" and Homebrew as a file name; `tail +3` was skipped
for the same reason. Both are ordinary cases now, because the oracle
pins the environment that decides it (B73, above). The text-tools
milestone adds four skips of its own and no more: two `fold -w` values
that are numbers OUT OF RANGE, where GNU appends the C library's
`strerror(ERANGE)` and the two hosts word it differently — the same
shape as `nl -w 0` — and two `tac -r` expressions, `\(…\)` and `\|`,
that are outside the regular-expression subset that utility states in
its header.

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
wolf 0.2.16 exposes neither `splice` nor `copy_file_range`, so every
byte we copy is read into a list and written back out.

Memory is level, and flat in the size of the input either way: copying
256 MiB peaks at 2.4 MB of RSS on nomad-1 against GNU's 1.9 MB, and at
2.8 MB on kasumi against 2.3 MB; `cat -n` peaks at 3.9 MB against
2.2 MB, and at 3.7 MB against 2.7 MB. That costs one `region` block per
chunk — without it the same copy peaked at 340 MB and `cat -n` at
1.1 GB, because the ambient region never frees what each read allocates.

`head`, `tail` and `cut` have a table of their own, because they are
the first utilities where reading the whole file is a defect rather than
a style choice. Release tier, GNU coreutils 9.11, 5 runs, 256 MiB of
generated text, kasumi at load 1.4. **These numbers are linux only**:
wave 45 forbids builds on nomad-1, so macOS is CI's job on this branch
and not a column here.

**The `head` question, answered with a syscall count and not an
adjective.** `head -n 1` of a 268,435,456-byte file:

| | read calls | bytes read | max RSS |
|---|---:|---:|---:|
| `head -n 1`, boreutils | 4 | 265,216 | 2.8 MB |
| `head -n 1`, GNU | 4 | 12,214 | 2.3 MB |
| `head -c 1`, boreutils | 4 | 3,073 | 2.5 MB |
| `head -c 1`, GNU | 4 | 4,023 | 2.3 MB |
| `tail -n 10`, boreutils | 1,028 | **268,438,528** | 2.9 MB |
| `tail -n 10`, GNU | 5 | 12,214 | 2.3 MB |

boreutils `head -n 1` reads one 256 KiB chunk and stops — 0.1% of the
file, and the rest of each figure is the dynamic linker. `tail -n 10`
reads **all of it**, and that row is the whole point of the `tail`
section below.

| head | kasumi (linux x86-64) |
|---|---|
| `-n 1` of 256 MiB | 0.4 ms vs GNU 0.2 ms |
| `-c 1` of the same | 0.3 ms vs GNU 0.2 ms |
| `-n 10`, the default | 0.4 ms vs GNU 0.2 ms |
| `-n 1` through a pipe | 0.7 ms vs GNU 0.4 ms |
| `-n 100000` of short lines | 1.4 ms vs GNU 1.2 ms (0.86x) |
| `-c 100000000`, a bulk copy | 3.8 ms vs GNU 2.9 ms (0.75x) |
| `-c -1024` on a file, which an `fstat` turns into a copy | 32.8 ms vs GNU 26.5 ms (0.81x) |
| `-c -1024` through a pipe, where the window is the only way | 243 ms vs GNU 32 ms (0.13x) |
| `-n -1`, a window over everything | 295 ms vs GNU 26 ms (0.09x) |
| `-n -1` of short lines | 47 ms vs GNU 2.1 ms (0.04x) |

The first four rows are start-up on both sides and hyperfine will not
divide numbers that small, which is the right answer: neither
implementation reads the file. The `-c -K` and `-n -K` rows are where
`head` has to hold a window, and they are the repository's clearest
price for having no bulk copy in the language: the bytes leaving the
window are pushed into a list one at a time where GNU `memcpy`s them. A
`chunk[0..k]` slice was tried in their place and is **2.2x slower**
(656 ms against 297 ms), because a list slice allocates and copies a
whole fresh list.

| tail | kasumi (linux x86-64) |
|---|---|
| `-n 10` of a file, where GNU seeks | 111 ms vs GNU 0.2 ms |
| `-c 10` of a file | 27 ms vs GNU 0.2 ms |
| `-n 10` through a pipe, where neither side may seek | 114 ms vs GNU 68 ms (0.60x) |
| `-c 10` through a pipe | 28.9 ms vs GNU 28.8 ms (**1.00x**) |
| `-n 10` of short lines through a pipe | 35 ms vs GNU 20 ms (0.56x) |
| `-n +1`, the whole file | 33.6 ms vs GNU 26.7 ms (0.80x) |
| `-c +100000000`, a skip and a copy | 32.7 ms vs GNU 23.9 ms (0.73x) |
| `-n 100000` of short lines | 118 ms vs GNU 0.9 ms |

**`tail` on a regular file is O(size) here and O(1) for GNU, and no
amount of tuning closes that.** GNU seeks to the end and reads a few
kilobytes; wolf 0.2.16 has no seek, no tell and no positional read
(wolf-lang#426, filed by this lane), so boreutils reads the file
forward. On a PIPE, where GNU cannot seek either, the comparison is
fair and boreutils is level with it: 1.00x on `-c` and 0.60x on `-n`.

| cut | kasumi (linux x86-64) |
|---|---|
| `-b1-10`, C | 206 ms vs GNU 101 ms (0.49x) |
| `-c1-10`, C, where a character is a byte | 206 ms vs GNU 100 ms (0.49x) |
| `-c1-10`, UTF-8, where it is not | 1375 ms vs GNU 377 ms (0.27x) |
| `-n -b1-10`, UTF-8 | 1507 ms vs GNU 534 ms (0.35x) |
| `-f1 -d' '`, C | 283 ms vs GNU 136 ms (0.48x) |
| `-f1,3 -d' '`, C | 441 ms vs GNU 228 ms (0.52x) |
| `-f2- -d' ' --output-delimiter=:`, C | 1754 ms vs GNU 919 ms (0.52x) |
| `--complement -b1-10`, C | 384 ms vs GNU 113 ms (0.30x) |
| `-b1-10` on very short lines, C | 87 ms vs GNU 53 ms (0.61x) |
| `-f1 -d' '` on very short lines, C | 123 ms vs GNU 77 ms (0.63x) |
| `-b1-10` on binary noise, C | 34.5 ms vs GNU 10.6 ms (0.31x) |

`cut` is between 0.27x and 0.63x, and two measurements got it there. The
first draft pushed every input byte through the shared ring, because the
ring is the one buffer that can outlive a per-chunk `region`, and it read
**0.06x**; cutting each line out of the chunk it arrived in, and using
the ring only for a line that straddles two chunks, is 7x faster. Then
`-f1` was still 0.09x because it walked every field of every line to the
end: stopping at the last field any range names took it to 0.48x. Both
are in the git history rather than only in this table.

**Memory is flat in the size of the input for all three**, at one
`region` per chunk plus a window: 2.8 MB for `head -n 1`, 2.9 MB for
`tail -n 10` and 3.1 MB for `cut -b1-10` on 256 MiB, against GNU's
2.3–2.5 MB. `tail`'s window is the last K lines and `head -n -K`'s is
the same, so a `tail -n 100000` costs what those hundred thousand lines
weigh and nothing more.

The transform set — `tr`, `uniq`, `seq` and `nl` — has a table of its
own, and it is the first one taken on ONE host. Wave 45 forbids builds
on nomad-1, this project's macOS box, so there is no macOS binary to
measure; every number below is kasumi (linux x86-64, 16 cpus) at load
1.3, release tier, GNU coreutils 9.11, 5 runs, 256 MiB of generated
text for the `tr`, `uniq` and `nl` rows and 16 MiB of very short lines
where the row says so. `seq` reads nothing, so its rows are a million
numbers each, 5 runs.

**The predictions were written into the bench files before the first
run, and two of the four were wrong in a way worth keeping.**

| bench | boreutils | GNU | vs GNU |
|---|---:|---:|---:|
| `tr a-z A-Z`, 256 MiB | 273 ms | 92 ms | 0.34x |
| `tr '[:lower:]' '[:upper:]'` | 274 ms | 92 ms | 0.34x |
| `tr -d a` | 411 ms | 179 ms | 0.44x |
| `tr -cd '[:alpha:]'` | 700 ms | 441 ms | 0.63x |
| `tr -s ' '` | 419 ms | 375 ms | 0.90x |
| `tr -s a-z A-Z` | 422 ms | 1570 ms | **3.72x** |
| `uniq`, 16 MiB of short lines | 95 ms | 90 ms | 0.94x |
| `uniq -c`, short lines | 392 ms | 255 ms | 0.65x |
| `uniq`, 256 MiB of ordinary lines | 642 ms | 295 ms | 0.46x |
| `uniq -f 1` | 759 ms | 389 ms | 0.51x |
| `nl`, 16 MiB of short lines | 233 ms | 220 ms | 0.94x |
| `nl -n rz -w 9`, short lines | 447 ms | 231 ms | 0.52x |
| `nl`, 256 MiB of ordinary lines | 676 ms | 464 ms | 0.69x |
| `nl -b 'p^a'` | 551 ms | 663 ms | **1.20x** |
| `seq 1 1000000` | 71 ms | 4.9 ms | 0.07x |
| `seq -w 1 1000000` | 125 ms | 158 ms | **1.27x** |
| `seq 0 0.001 1000` | 73 ms | 144 ms | **1.96x** |
| `seq -f %g 1 1000000` | 108 ms | 148 ms | **1.37x** |

**`tr -s a-z A-Z` is not our win, it is GNU's cliff.** Measured on the
same file and the same host, 20 runs: GNU squeezes alone in 85 ms and
translates alone in 95 ms, and does both in 1585 ms — eighteen times
its own squeeze. boreutils does both in one pass over the byte, so it
answers in 422 ms whether one is asked for or two, and the ratio is
3.7x with a standard deviation of 1.3 ms on our side. It is worth
saying plainly: everywhere else in this table `tr` is behind, by 0.34x
where the loop is a table lookup and a stored byte.

**`seq` splits in two, and the split is the whole design.** GNU has a
hand-written decimal incrementer for a pure integer sequence, and it is
fifteen times faster than anything this project can write today: 4.9 ms
against 71 ms for a million integers. The moment the sequence is not a
plain integer walk — a fractional increment, `-w`, a `-f` format — GNU
falls back to a long double add and a `printf` per value, and exact
decimal arithmetic beats that by 1.3x to 2.0x. So the exactness `seq`
promises is not paid for in speed except on the one case GNU
special-cases.

**What the predictions got wrong.** `uniq` was predicted at 0.4x to
0.6x and measured at 0.35x to 0.61x, which is a hit. The other three
missed:

- **`tr`** was predicted at 0.6x to 0.9x for bulk work. Translation is
  worse than that (0.34x) and the translate-and-squeeze row is 3.72x,
  four times outside the band in the other direction.
- **`seq`** was predicted at 0.3x to 0.5x throughout. It is 0.07x on
  integers and 1.27x to 1.96x everywhere else: wrong in both
  directions, and the prediction missed that GNU has two paths.
- **`nl`** was predicted worst on short lines, because the per-line
  work is what it pays most for. It is the other way round: the
  short-line rows are the best ones. The per-BYTE copy, not the
  per-line work, is what costs — which is the same conclusion `head`,
  `tail` and `cut` reached, and their lane's measurement is why the
  numbers above are what they are.

**`uniq` and `nl` were re-measured after taking the streaming lane's
finding.** Both first read a line by copying it out of the chunk it
arrived in, and `nl` then built a `str` from those bytes on EVERY line
just to compare it against `\:`. Cutting each line out where it lies —
carrying a line into the boundary buffer only when it actually straddles
one — and comparing the delimiter as bytes moved seven of the eight
rows, one of them past GNU:

| bench | before | after |
|---|---:|---:|
| `uniq`, short lines | 0.56x | **0.94x** |
| `uniq`, ordinary lines | 0.36x | 0.46x |
| `uniq -i` | 0.35x | 0.45x |
| `uniq -D`, short lines | 0.59x | **1.01x** |
| `nl`, short lines | 0.65x | **0.94x** |
| `nl`, ordinary lines | 0.51x | 0.69x |
| `nl -b n` | 0.37x | 0.51x |
| `nl -b 'p^a'` | 0.74x | **1.20x** |

Neither utility uses the ring `head`, `tail` and `cut` share: what a
line straddling a chunk needs here is one buffer that outlives the
chunk, and that is a first-class region (`let keep = region()`) written
through `in keep { }`, which is cheaper than a ring for a boundary that
is crossed once per megabyte.

Memory is flat in the size of the INPUT and linear in the longest LINE.
Peak RSS over 256 MiB, ours against GNU's: `tr` 6.9 MB against 2.2 MB,
`uniq` 9.0 MB against 2.2 MB, `nl` 10.5 MB against 2.4 MB, and `seq`
3.3 MB for a three-million-number sequence against 2.3 MB. That costs
one `region` per chunk read, and, in `uniq` and `nl`, a FIRST-CLASS
region (`let keep = region()`) holding the one or two buffers that must
outlive a chunk, written through `in keep { }` and overwritten in place
rather than rebuilt. On a single 64 MiB line with no newline in it,
where that bound is the line and not the chunk, `uniq` peaks at 527 MB
against GNU's 70 MB and `nl` at 398 MB: the line is materialized six to
eight times over on the way through, and GNU holds one copy.

The text-tools set — `tac`, `paste`, `fold`, `expand` and `unexpand` —
finishes B3, and its table is the first in this repository where wolf is
AHEAD of GNU on most rows. kasumi (linux x86-64, 16 cpus) at load 2–5,
release tier, GNU coreutils 9.11, 5 runs, 256 MiB of generated text and
16 MiB of very short lines. Wave 45 forbids builds on nomad-1, so there
is no macOS column.

**The predictions were written into `notes/bu07-the-pin-and-the-rest-of-b3.md`
and the bench files before anything was measured, and four of the five
were wrong.**

| bench | boreutils | GNU | vs GNU |
|---|---:|---:|---:|
| `tac`, ordinary lines, a file | 778 ms | 139 ms | 0.18x |
| `tac`, ordinary lines, a pipe | 778 ms | 142 ms | 0.18x |
| `tac`, very short lines | 89 ms | 53 ms | 0.60x |
| `tac -b` | 773 ms | 139 ms | 0.18x |
| `tac -s ' '` | 1142 ms | 562 ms | 0.49x |
| `tac -r -s q`, a literal expression | 1245 ms | 3472 ms | **2.79x** |
| `tac -r -s '[aeiou][aeiou]*'` | 2072 ms | 4329 ms | **2.09x** |
| `paste -s` | 837 ms | 481 ms | 0.57x |
| `paste`, one file | 780 ms | 294 ms | 0.38x |
| `paste`, two files | 1629 ms | 609 ms | 0.37x |
| `paste`, four files | 3312 ms | 1158 ms | 0.35x |
| `fold -b` | 867 ms | 1191 ms | **1.37x** |
| `fold`, display columns | 980 ms | 1676 ms | **1.71x** |
| `fold -c` under UTF-8 | 1164 ms | 1395 ms | **1.20x** |
| `fold`, columns under UTF-8 | 1776 ms | 1902 ms | **1.07x** |
| `fold -s` | 1276 ms | 2697 ms | **2.11x** |
| `fold -b -w 64` on binary noise | 220 ms | 1132 ms | **5.15x** |
| `expand` | 707 ms | 2101 ms | **2.97x** |
| `expand -t 3,7` | 702 ms | 2118 ms | **3.02x** |
| `expand -i` | 694 ms | 1596 ms | **2.30x** |
| `expand` on a tab-heavy input | 3274 ms | 3312 ms | **1.01x** |
| `expand` on binary noise | 177 ms | 1500 ms | **8.47x** |
| `unexpand` | 668 ms | 1701 ms | **2.55x** |
| `unexpand -a` | 1170 ms | 3145 ms | **2.69x** |
| `unexpand -a` over long blank runs | 348 ms | 351 ms | **1.01x** |
| `unexpand -a` under UTF-8 | 1190 ms | 3561 ms | **2.99x** |
| `unexpand` on binary noise | 173 ms | 1594 ms | **9.23x** |

**`tac` is the one that loses, and the reason is `tail`'s reason.** GNU
seeks to the end of a regular file and walks backwards through it; wolf
0.2.16 has no seek, no tell and no positional read (wolf-lang#426), so
`tac` reads the whole input forward before it can answer anything. That
is 0.18x, and through a pipe — where GNU cannot seek either — it is
*still* 0.18x, because GNU buffers a pipe to `$TMPDIR` and reads it back
with the same seek. There is no arrangement of this program that closes
that gap today.

**`tac -r` is the other side of the same coin.** GNU's regular-expression
path gives up the seek and runs `re_search` backwards over the buffer,
and a small hand-written matcher beats it by 2.1x to 2.8x on the same
input. So `tac` is 0.18x where GNU has a syscall we do not and 2.8x
where neither of us does.

**Where GNU decodes and we do not have to, we win by a lot.** `expand`,
`unexpand` and `fold` are 1.0x to 9.2x, and the largest ratios are on
BINARY NOISE — 8.5x and 9.2x — because coreutils 9.x runs these
utilities through a multibyte decoder even in the C locale, and invalid
bytes are its slowest path. The smallest ratios are where the OUTPUT is
large: `expand` on a tab-heavy input is 1.01x, because there both sides
are writing, not deciding.

**`fold -s` was predicted to be the worst row and is the best of its
width** (2.11x). The backwards scan for the last blank runs once per
break over a piece that is at most `-w` bytes long; GNU pays more for
the same decision.

Memory is flat in the input for four of the five. Peak RSS over
256 MiB, ours against GNU's: `paste -s` 3.4 MB against 1.7 MB, `paste`
of two files 4.3 MB against 1.7 MB, `fold` 4.4 MB against 2.0 MB,
`expand` 3.3 MB against 2.0 MB, `unexpand -a` 3.4 MB against 2.0 MB.

**Getting there was a measurement, not a habit.** All five first wrote
their output through `bore.put_byte`, which is correct and cost **2.6 to
2.8 times the output in resident memory**: the shared writer empties its
buffer by allocating a fresh one, and every replacement is abandoned in
an arena that frees nothing, so `expand` over 256 MiB peaked at 715 MB
and `paste` of two such files at 1.35 GB. The three that read and write
a chunk at a time now build each pass's output inside the per-chunk
`region` and hand it to `write_direct`; `tac` and `paste` cannot do that
and use `bore.Sink`, one buffer filled in place and written whole.

**`tac` is the exception and always will be**: it holds the whole input,
so 256 MiB peaks at **515 MB**, twice the input, against GNU's 1.8 MB.
The factor of two is not the design, it is `List` having no capacity
surface at 0.2.16 (wolf-std F-0011): a list built by pushing doubles,
and each doubling abandons the previous buffer. Sizing it up front from
`fs_fstat` does not help — filling it is itself a run of pushes — and
that was measured rather than assumed.

A single line that is the whole input is the other bound: a 64 MiB line
with no newline in it costs `fold` 322 MB and `paste` 131 MB, against
GNU's 2.0 MB and 1.7 MB, for the same reason.

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
| `head` | done | `-n 1` start-up on both sides; `-n -K` 0.09x (linux) |
| `tail` | done, `-f` included | pipe `-c` 1.00x, `-n` 0.60x; a file 111 ms against GNU's 0.2 ms, and the reason is wolf-lang#426 |
| `cut` | done, without 9.11's `-w`, `-F` and `-O` | 0.27x to 0.63x (linux) |
| `tr` | done | 0.34x translating, **3.72x** translating and squeezing (linux) |
| `uniq` | done | 0.46x to **1.01x** (linux) |
| `seq` | done | 0.07x on integers, **1.27x to 1.96x** everywhere else (linux) |
| `nl` | done | 0.51x to **1.20x** (linux) |
| `tac` | done | 0.18x on a stream, **2.09x to 2.79x** under `-r` (linux) |
| `paste` | done | 0.35x to 0.57x (linux) |
| `fold` | done | **1.07x to 5.15x** (linux) |
| `expand` | done | **1.01x to 8.47x** (linux) |
| `unexpand` | done | **1.00x to 9.23x** (linux) |
