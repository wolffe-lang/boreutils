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

**Windows is out of scope**: the oracle of record is a unix build of GNU
coreutils, and CI runs on linux and macOS. (The reason used to be that
the only byte-exact route to standard input and output was reopening
`/dev/stdin` and `/dev/stdout`; since wolf 0.2.26 boreutils reads
descriptor 0 and writes descriptor 1 directly, bu19.)

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

**The reason is the host's.** Since wolf 0.2.26 (`os_error`,
`os_error_text`, bu19) the text after a failed write or read is the
host's own `strerror`, as GNU's is: a full disk is `write error: No
space left on device` on both sides, and every `/dev/full` case compares
stderr. A program that reports after other fs calls keeps the host's
number from the moment of the failure (`bore.host_code`), because the
next successful call clears it. And standard output is descriptor 1
itself, so a socket is written like any other descriptor (until 0.2.26
linux refused the `/dev/stdout` reopen for a socket and output fell back
to `print_raw`, which discards write errors, wolf-lang#408).

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
its differential corpus, except where a case says otherwise and is
skipped with its reason. The corpus holds **3,077 cases**; a run on
kasumi (linux x86-64) at this pin answers **3,017 passed, 0 failed, 60
skipped**, the same list on the release and the dev tier, and CI's
macOS leg skips the `/dev/full` and `/proc` cases besides, because
macOS has neither (bu19's figures and run ids are in
`notes/bu19-the-byte-surface.md`). (The previous edition of this
sentence, before bu19, said 3,048 cases, 2,986 and 62 on kasumi; before
bu18's `ls` it said 2,674 cases, 2,642 and 32 on kasumi, and 2,618 and 56
on macOS, run 37060771131; before bu14's six utilities it said 2,114
cases, 2,094 and 20 on kasumi, and 2,077 and 37 on macOS, run
36044150121; before that it said 1,753 and 19 for the 1,772-case
corpus, and "five more" on macOS; kasumi answered 1,752 and 20 at that
commit, `eac2a32`, and macOS 37 at that lane's first green, run
36029854007.) The corpus
and the run are stated separately on purpose: an earlier edition of this
paragraph called the passing count the case count, which quietly
subtracted the skips from the corpus instead of naming them.

Two `wc` cases are skipped and say why in
the case file: two code points whose display width the two hosts' own
`wcwidth` disagree about. (Two more, the ENOTDIR and ELOOP reasons, ran
once wolf 0.2.26 put the host's error number beside the row, bu19.) Five more run only on a host with
`/dev/full`, which is how a write error on a LIVE descriptor is reached
at all, and so are skipped on macOS. Ten `wc` cases name the GNU
version they describe with `gnu_min` — those are a record of the field,
not of the oracle, which is 9.11 everywhere the gauntlet runs. The
ninth was found by the `field` leg on the first run it ever made: with
descriptor 1 closed, 9.11 stops at the first write that fails and 9.4
keeps walking, so `wc FILE nope >&-` names the missing file on 9.4 and
not on 9.11. The tenth is bu19's: into `/dev/full` 9.11 names the
reason and 9.4 says a bare `write error`. Sixteen more name 9.11 for the same reason, all bu14's:
9.4 has no `%N$` in `printf` at all, takes an empty number without a
word, and refuses an `nproc --ignore` past 2^64. Eight more are bu18's
`ls`: 9.4 has no `--sort=name`, lists the `--sort` words in another
order, and does not sort by `--time=mtime` alone.

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

**The small-surface set adds twelve skips, and not one of them is a C
library's.** Each is a wolf 0.2.25 gap, filed with a witness and named
in the case file: `printenv`'s four bare listings (wolf lists the
environment only sorted, wolf-lang#535), `pwd -L` beside a `cp -a` twin
of the working directory (no file identity, wolf-lang#536), and `tee`'s
seven — five broken-pipe branches of `-p` and `--output-error`, and
`-i` twice, all of which need a signal ignored (wolf-lang#423).

**`ls` adds thirty skips, and every one is wolf's.** Twenty-three need a
link's own identity or the rest of a stat record — the long format and
the options that imply it, `-s`, `-u`, `-c`, `--time=birth`, and `-F`,
`-p`, `-S`, `-t` and `-R` meeting a link that resolves (wolf 0.2.25
follows every link and has no `lstat`, no `readlink`, no mode, owner or
link count: wolf-lang#625); three need the directory's own order
(`-U`, `-f`, `--sort=none`: `fs_read_dir` sorts, wolf-lang#626); one
needs an inode (`-i`, wolf-lang#536) and one an inode and `lstat` both
(`-L -R` meeting a loop); two are a terminal whose own width is not 80,
which GNU asks and wolf cannot (wolf-lang#643). Each is refused by name,
status 2, where this program cannot answer; none is ignored. (bu19
cleared two: `Permission denied` through an unreadable directory is the
host's reason now, and the terminal defaults are taken through
`os_isatty`, with 24 cases run on a pseudo-terminal.)

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
| `wc -c`, through `<` | 74 ms vs GNU 7 ms (0.10x) | 36 ms vs GNU 0.5 ms (0.01x); **0.43 ms vs GNU 0.39 ms** since bu15 (wolf 0.2.22, linux) |

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
sides, so it measures start-up. Through a redirect GNU `fstat`s and
asks the offset, because `wc -c` owes size minus the current offset;
before wolf 0.2.22 we could ask neither and read the whole input
(34 ms on 256 MiB). Since bu15 we ask both, and the row is start-up
too: 0.43 ms against 0.39 ms, hyperfine 50 runs, kasumi at load 5–7.
The size is believed only when two positional reads confirm it, so a
sysfs or `/proc` file, whose size lies, is read and counted as GNU
counts it (trunk said 4096 and 0 for two of them, where GNU said 23
and 144).

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
wolf 0.2.25 exposed neither `splice` nor `copy_file_range`, so every
byte was read into a list and written back out.

**Since wolf 0.2.26 the host does the copy (bu19).** `cat`'s plain path
is `fs_copy_chunk` to descriptor 1 (`copy_file_range`, `sendfile`,
`splice`, then a loop), `wc -l` counts newlines with `bytes_count`, and
`head`, `tail`, `nl`, `uniq` and `cut` find their lines with
`bytes_find`/`bytes_count`. kasumi, release tier, GNU 9.11, the bench's
full-size inputs, one hyperfine call per row with every build and GNU
in it (10 runs; load 4 to 11, other lanes): 0.2.25 is trunk `50d8907`,
"before" the same tree at 0.2.26 with descriptors 0..2 adopted, "after"
the adoption.

| bench | 0.2.25 | before | after | GNU | vs GNU |
|---|---:|---:|---:|---:|---:|
| `cat` 1 GiB to /dev/null | 285 ms | 252 ms | **9.9 ms** | 8.3 ms | 0.84x |
| `cat` 1 GiB to a file (btrfs) | 700 ms | 548 ms | **60 ms** | 55 ms | 0.91x |
| `cat`, 64 operands to /dev/null | 804 ms | 818 ms | **25 ms** | 18 ms | 0.73x |
| `cat -n`, short lines | 874 ms | 888 ms | 910 ms | 249 ms | 0.27x |
| `wc -l`, 1 GiB | 504 ms | 481 ms | **173 ms** | 88 ms | 0.51x |
| `wc -l`, very short lines | 140 ms | 141 ms | **15.6 ms** | 7.0 ms | 0.45x |
| `tail -n 10` through a pipe | 454 ms | 460 ms | **167 ms** | 302 ms | **1.82x** |
| `tail -n 10` of short lines through a pipe | 138 ms | 138 ms | **11.2 ms** | 79.6 ms | **7.11x** |
| `head -n -1` through a pipe | 1352 ms | 1294 ms | 1058 ms | 362 ms | 0.34x |
| `nl`, ordinary lines | 2624 ms | 2632 ms | 2409 ms | 2167 ms | 0.90x |
| `uniq`, very short lines | 424 ms | 422 ms | 371 ms | 381 ms | **1.03x** |
| `uniq`, ordinary lines | 3069 ms | 2679 ms | 2342 ms | 1250 ms | 0.53x |
| `cut -b1-10` | 949 ms | 971 ms | 698 ms | 495 ms | 0.71x |
| `cut -f1 -d' '` | 1317 ms | 1241 ms | 951 ms | 619 ms | 0.65x |
| `cut -b1-10`, very short lines | 373 ms | 546 ms | 533 ms | 221 ms | 0.41x |
| `cut -b1-10` on binary noise | 155 ms | 160 ms | 75 ms | 51 ms | 0.68x |

Every row and the rest are in `notes/bu19-the-byte-surface.md`. One row
moved the wrong way and it is not the program's: `cut` on very short
lines went from 373 to 546 ms when descriptor 1 stopped being reopened,
with the same instructions; the system time is 1,537 `brk` calls where
there were 10, glibc trimming and regrowing the heap as each chunk's
`region` frees, and a malloc tunable makes both builds equal
(wolf-lang#644). `uniq` moved 11% the other way for the same reason.

Memory is level, and flat in the size of the input either way: copying
256 MiB peaks at 2.4 MB of RSS on nomad-1 against GNU's 1.9 MB, and at
2.8 MB on kasumi against 2.3 MB; `cat -n` peaks at 3.9 MB against
2.2 MB, and at 3.7 MB against 2.7 MB. That costs one `region` block per
chunk — without it the same copy peaked at 340 MB and `cat -n` at
1.1 GB, because the ambient region never frees what each read allocates.

`head`, `tail` and `cut` have a table of their own, because they are
the first utilities where reading the whole file is a defect rather than
a style choice. **These numbers are linux only**: wave 45 forbids
builds on nomad-1, so macOS is CI's job and not a column here.

**`tail` and `head` read from the end since wolf 0.2.22** (bu15,
boreutils#19). Until then wolf had no seek, no tell and no positional
read (wolf-lang#426), so `tail -n 10` of a regular file read all of it
and `head -n -K` held a window over everything. 0.2.22 has all three,
and descriptor 0 answers them (`[os.fs.std]`), so a regular file —
named, or standard input that is one — is read from where the answer
starts, as GNU reads it. What each program does with each kind of
input:

| | a regular file | standard input that is a regular file | a pipe |
|---|---|---|---|
| `tail -n K` | walk back 8 KiB at a time from the end to the last K lines, then a positional copy | the same, counted from descriptor 0's offset; the offset is left at the end | read forward through the window |
| `tail -c K` | a positional copy of the last K bytes | the same, from the offset | read forward through the window |
| `tail -c +K` | a seek past K - 1 bytes, then a copy | the same, from the offset | read and discard K - 1 bytes |
| `tail -n +K` | read forward from the start (lines must be counted) | read forward from the offset | read forward |
| `head -c -K` | copy the first end - K bytes | the same, from the offset; the offset is left past the output | the window |
| `head -n -K` | walk back K lines from the end, then copy what precedes them | the same, from the offset | the window |
| `head -n K`, `-c K` | read forward and stop (as before) | the same; the offset is put back just past the output, as GNU puts it | read forward and stop |
| `wc -c` | the size, no read | the size minus the offset, no read; the offset is left at the end | read |

A file whose `fstat` size cannot be trusted is read forward like a pipe:
a sysfs attribute reports 4096 bytes whatever it holds, and a `/proc`
file reports 0, and GNU reads both. `bore.verified_end` believes a size
only when the byte before it exists and nothing exists at it, which is
two positional reads.

**The `head` question, answered with a syscall count and not an
adjective.** `head -n 1` and `tail -n 10` of a 268,435,456-byte file,
`strace` of the read-family calls on the file's descriptor:

| | read calls | bytes read | max RSS |
|---|---:|---:|---:|
| `head -n 1`, boreutils | 4 | 265,216 | 2.8 MB |
| `head -n 1`, GNU | 4 | 12,214 | 2.3 MB |
| `head -c 1`, boreutils | 4 | 3,073 | 2.5 MB |
| `head -c 1`, GNU | 4 | 4,023 | 2.3 MB |
| `tail -n 10`, boreutils at 0.2.20 | 1,025 | **268,435,456** | 2.9 MB |
| `tail -n 10`, boreutils (bu15) | 4 | 9,134 | — |
| `tail -n 10`, GNU | 2 | 8,192 | 2.3 MB |
| `tail -c 10`, boreutils (bu15) | 3 | 11 | — |
| `tail -c 10`, GNU | 1 | 10 | — |
| `wc -c`, boreutils (bu15) | 2 | 1 | — |
| `wc -c`, GNU | 2 | 16 | — |

(The `head` rows and the RSS column are bu03's, whose counts include the
dynamic linker. The `tail` and `wc` rows are bu15's, `strace -y` on the
input file's descriptor only: boreutils' extra calls are the two
positional reads that verify the end before trusting it, and its
`tail -n 10` copies the last 941 bytes with one more read where GNU
writes them from the block it already holds.)

Release tier, GNU coreutils 9.11, kasumi (linux x86-64, 16 cpus),
256 MiB of generated text (16 MiB of short lines where a row says so),
**hyperfine 20 runs, kasumi at load 5 to 9** with other lanes running
(the load at each table's start and end is in bu15's notes). The
"before" column is trunk `010f3144` built by wolf 0.2.20, the last
release without the seek.

| head | before (wolf 0.2.20) | after (bu15, wolf 0.2.22) |
|---|---|---|
| `-n 1` of 256 MiB | 0.4 ms vs GNU 0.1 ms | 0.4 ms vs GNU 0.3 ms |
| `-c 1` of the same | 0.3 ms vs GNU 0.3 ms | 0.3 ms vs GNU 0.2 ms |
| `-n 10`, the default | 0.4 ms vs GNU 0.2 ms | 0.5 ms vs GNU 0.2 ms |
| `-n 1` through a pipe | 0.6 ms vs GNU 0.4 ms | 0.8 ms vs GNU 0.6 ms |
| `-n 100000` of short lines | 1.4 ms vs GNU 1.2 ms (0.81x) | 1.5 ms vs GNU 1.3 ms (0.90x) |
| `-c 100000000`, a bulk copy | 3.9 ms vs GNU 3.0 ms (0.77x) | 3.9 ms vs GNU 2.9 ms (0.76x) |
| `-c -1024` of a file | 35.0 ms vs GNU 27.7 ms (0.79x) | 33.7 ms vs GNU 28.2 ms (0.84x) |
| `-c -1024` of standard input that is a file | 248 ms vs GNU 26.9 ms (0.11x) | **37.6 ms** vs GNU 30.3 ms (0.81x) |
| `-n -1` of a file | 299 ms vs GNU 26.9 ms (0.09x) | **37.3 ms** vs GNU 29.4 ms (0.79x) |
| `-n -1` of standard input that is a file | 296 ms vs GNU 27.8 ms (0.09x) | **36.5 ms** vs GNU 28.7 ms (0.79x) |
| `-n -1` of short lines | 47.4 ms vs GNU 1.9 ms (0.04x) | **3.0 ms** vs GNU 2.1 ms (0.71x) |
| `-c -1024` through a pipe, the window | 254 ms vs GNU 33.5 ms (0.13x) | 250 ms vs GNU 34.8 ms (0.14x) |
| `-n -1` through a pipe, the window | 306 ms vs GNU 83.5 ms (0.27x) | 315 ms vs GNU 83.2 ms (0.26x) |

| tail | before (wolf 0.2.20) | after (bu15, wolf 0.2.22) |
|---|---|---|
| `-n 10` of a file | 114 ms vs GNU 0.21 ms | **0.31 ms** vs GNU 0.21 ms |
| `-c 10` of a file | 29.1 ms vs GNU 0.21 ms | **0.30 ms** vs GNU 0.21 ms |
| `-n 10` of standard input that is a file | 111 ms vs GNU 0.33 ms | **0.39 ms** vs GNU 0.33 ms |
| `-n 100000` of short lines | 124 ms vs GNU 0.8 ms | **1.5 ms** vs GNU 0.7 ms (0.45x) |
| `-n 10` through a pipe, neither side may seek | 116 ms vs GNU 74.8 ms (0.64x) | 102 ms, the same binary path as before (A/B below) |
| `-c 10` through a pipe | 32.0 ms vs GNU 31.6 ms (0.99x) | 39.3 ms vs GNU 34.5 ms (0.88x) |
| `-n 10` of short lines through a pipe | 35.3 ms vs GNU 20.3 ms (0.57x) | 38.1 ms vs GNU 21.9 ms (0.57x) |
| `-n +1`, the whole file | 36.2 ms vs GNU 29.6 ms (0.82x) | 45.4 ms vs GNU 37.1 ms (0.82x) |
| `-c +100000000`, a seek and a copy | 36.3 ms vs GNU 25.5 ms (0.70x) | 41.0 ms vs GNU 34.4 ms (0.84x) |

The sub-millisecond `tail` rows are hyperfine at **50 runs** with
`-N` (no shell), because the bench tool's tenth-of-a-millisecond
rounding cannot tell 0.21 from 0.31; the rest are `tools/bench` at 20.
**`tail -n 10` of a file is 366x faster than it was and 1.5x GNU's
time**, the remaining 0.1 ms being wolf's start-up, not the read: both
sides now read about 8 KiB of a 256 MiB file.

**The pipe rows did not move, and the A/B says so rather than the
tables.** Between the two tables the load moved, and so did GNU's own
numbers (the `-n +1` copy is 29.6 ms and 37.1 ms for the SAME GNU
binary). Run back to back, three rounds of 10, the pin without the seek
and bu15 read 102.6/104.1/102.2 ms against 102.4/104.0/101.8 ms for
`tail -n 10` through a pipe. `head -n -1` through a pipe first read 8%
SLOWER (299 ms against 327 ms): threading a `mut sent: int` parameter
through the window loop to know where to leave the offset cost that, in
a loop that never needs it. The window now places the offset once, from
the reader's offset less what the window holds, and the A/B reads
303.4 ms against 303.3 ms.

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
2.3–2.5 MB (bu03's measurement). `tail`'s window is the last K lines
and `head -n -K`'s is the same, so through a pipe a `tail -n 100000`
costs what those hundred thousand lines weigh and nothing more; on a
regular file there is no window at all.

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

**At wolf 0.2.25, `unexpand` lost about a third of its lead
(wolf-lang#624, bu17).** The program did not change, and its hot
function's IR did not change either. The release tier's codegen
partition moved `flush_run` into the same unit as the loop that calls
it. That happened because unrelated functions grew. With the callee's
body visible, clang compiles the loop into code that runs 14% more
instructions and 63% more cycles. The measurement is kasumi, GNU 9.11,
the bench's full-size inputs, and 0.2.23 and 0.2.25 in one hyperfine
run:

| bench | 0.2.23 | 0.2.25 | GNU | vs GNU |
|---|---:|---:|---:|---:|
| `unexpand`, ordinary lines | 2594 ms | 4182 ms | 5903 ms | 2.28x → **1.41x** |
| `unexpand`, very short lines | 286 ms | 311 ms | 622 ms | 2.17x → **2.00x** |
| `unexpand`, leading runs | 834 ms | 889 ms | 1550 ms | 1.86x → **1.74x** |
| `unexpand` on binary noise | 686 ms | 721 ms | 5981 ms | 8.73x → **8.29x** |

**At wolf 0.2.26 the loss is gone, and not because anything fixed it
(bu19).** In one hyperfine run at load ~4.5, boreutils trunk `50d8907`
at 0.2.25 and the same tree at 0.2.26 run `unexpand` on ordinary lines
in 2820 ms and 2929 ms against GNU's 6547 ms (2.24x), with identical
user instructions (62.17 G) and a `one` of 689 instructions, 0.2.23's
count rather than 0.2.25's 710: the partition no longer puts
`flush_run` beside it. `unexpand.lu` did not change; the shared `bore`
module did (bu18's `ls`). The fragility wolf-lang#624 names stands, and
the issue carries the measurement.

**`tac` is the one that loses, and the reason was `tail`'s reason.** GNU
seeks to the end of a regular file and walks backwards through it; until
wolf 0.2.22 there was no seek, no tell and no positional read
(wolf-lang#426), so `tac` reads the whole input forward before it can
answer anything. That is 0.18x, and through a pipe — where GNU cannot
seek either — it is *still* 0.18x, because GNU buffers a pipe to
`$TMPDIR` and reads it back with the same seek. 0.2.22 has the calls and
`tail` and `head` use them (bu15); `tac` has not been rewritten onto them
yet, and its numbers here are the forward reader's.

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
surface at 0.2.22 (wolf-std F-0011): a list built by pushing doubles,
and each doubling abandons the previous buffer. Sizing it up front from
`fs_fstat` does not help — filling it is itself a run of pushes — and
that was measured rather than assumed.

A single line that is the whole input is the other bound: a 64 MiB line
with no newline in it costs `fold` 322 MB and `paste` 131 MB, against
GNU's 2.0 MB and 1.7 MB, for the same reason.

`sort` is B5, and the first utility here that may not hold its input:
past a run budget (256 MiB by default, `-S` sets it) it sorts each run
into a temporary file and merges the runs, at most 16 at a time. Every
comparison is on bytes — GNU's behaviour under `LC_ALL=C`, which is the
oracle's environment — and the sort is a merge sort of line indices,
stable by construction; GNU's last-resort whole-line comparison makes
that unobservable except under `-s` and `-u`, where input order decides
on both sides. kasumi (linux x86-64, 16 cpus), release tier, GNU
coreutils 9.11, 5 runs, generated text: 10 MB is `tools/bench --scale
0.01`, 100 MB is `--scale 0.1`, load 2–3, at the commit that carries
this table's code.

**The predictions were committed in `notes/bu08-sort.md` §3 and in the
bench file before anything was timed, from the oracle's build rather
than the algorithm: GNU sorts on eight threads here and compares with
`memcmp`; this program sorts on one and compares in a loop. Four of
eight bands were right.**

| bench | 10 MB | 100 MB |
|---|---:|---:|
| start-up, no input | 0.8 ms vs GNU 0.4 ms | 0.9 ms vs 0.4 ms |
| whole lines, a file | 99 ms vs 30 ms (0.30x) | 1532 ms vs 333 ms (0.22x) |
| whole lines, through a pipe | 99 ms vs 30 ms (0.30x) | 1530 ms vs 336 ms (0.22x) |
| `--parallel=1`, one thread each | 102 ms vs 45 ms (0.44x) | 1531 ms vs 640 ms (0.42x) |
| very short lines | 34 ms vs 15 ms (0.45x) | 476 ms vs 104 ms (0.22x) |
| binary noise | 11 ms vs 3.3 ms (0.30x) | 120 ms vs 33 ms (0.28x) |
| `-r` | 101 ms vs 30 ms (0.30x) | 1382 ms vs 309 ms (0.22x) |
| `-u` | 103 ms vs 31 ms (0.30x) | 1491 ms vs 331 ms (0.22x) |
| `-f` | 151 ms vs 32 ms (0.21x) | 2361 ms vs 399 ms (0.17x) |
| `-n` | 154 ms vs 47 ms (0.30x) | 2334 ms vs 475 ms (0.20x) |
| `-t ' ' -k2,2` | 279 ms vs 38 ms (0.14x) | 4026 ms vs 421 ms (0.10x) |
| `-k2` | 216 ms vs 38 ms (0.18x) | 3357 ms vs 420 ms (0.13x) |
| `-s -k1,1` | 198 ms vs 36 ms (0.18x) | 2947 ms vs 386 ms (0.13x) |
| the external merge, `-S 10M` | 123 ms vs 50 ms (0.40x) | 1365 ms vs 610 ms (0.45x) |

**Eight threads buy GNU less than two times.** Its `--parallel=1` row is
640 ms against 333 ms with eight, so the fair comparison — one thread
each — is 0.42x, and the rest of the gap is `memcmp` against a
bounds-checked byte loop. The keyed rows are the worst because GNU
finds a key's bounds once per line and this program finds them per
comparison. **Our external merge is faster than our in-memory sort**
(1.37 s against 1.53 s for 100 MB): ten 10 MB runs sort in cache where
one 100 MB index does not, which says where a faster in-memory sort
would come from.

**Memory, per input size** (peak RSS, `/usr/bin/time`):

| input | boreutils | GNU |
|---|---:|---:|
| 10 MB, in memory | 39 MB | 22 MB |
| 100 MB, in memory | 322 MB | 304 MB |
| 100 MB, `-S 10M` (external) | 41 MB | 12 MB |
| 1 GB, `-S 10M` (external) | 42 MB | 12 MB |
| 1 GB, the default budget (four runs) | 808 MB | 3,005 MB |

The external rows are flat in the input, which is the region per run
doing its work, and they got there by measurement: the first draft read
past the budget, and a list that crosses a power of two doubles, so 1 GB
at the default budget peaked at 1,060 MB and at `-S 10M` grew to 61 MB.
**The external merge is seen, not asserted**: under `strace`, 100 MB at
`-S 10M` created 11 `sortXXXXXX` files and unlinked all 11 (GNU: 32 and
32), and `-T` naming a directory that does not exist makes both programs
fail with `cannot create temporary file in '…'` — a differential case,
which a sort that never spilled could not pass.

The small-surface set — `tee`, `printf`, `printenv`, `pwd`, `sleep`
and `nproc` — is bu14's, and the wave asked for `env` beside them. **`env`
is not here**, because its job is to run COMMAND in a modified
environment and wolf 0.2.25 has no way to do that: no exec, no unset or
clear, no child working directory, a spawned child's standard input
wired to the null device, and a signal death that loses its number
(wolf-lang#534, with the witness). Its print-only half would be
`printenv` with a sorted listing, which is not the utility.

The six each have a header that says what they cannot do, and each such
thing is a filed issue rather than a quiet difference:

- **`tee`** refuses `-i` by name (SIGINT cannot be ignored), and every
  broken-pipe branch of `-p` and `--output-error` dies of SIGPIPE where
  GNU carries on (wolf-lang#423). The non-pipe half of those modes — a
  full disk, a closed descriptor, a file that cannot be opened — is
  implemented and has cases, and the cases see the FILES it writes:
  `tools/difftest` gained a scratch directory per case for this, gated
  by two planted differences that must fail by name.
- **`printf`** has every conversion GNU 9.11 has, `%N$` and `*`
  included, and its floating conversions are exact against the HOST's
  `long double`: x87 on linux x86-64 (`printf %.20f 0.1` is
  `0.10000000000000000000`), IEEE double on macOS
  (`0.10000000000000000555`), rounded and printed in big integers. Two
  random runs of 2,300 and 2,500 floating and integer conversions
  against GNU on kasumi found no difference.
- **`printenv`** prints a named variable exactly and the bare listing
  sorted (wolf-lang#535).
- **`pwd`** is physical by default as GNU's is; `-L` decides whether
  `$PWD` names the working directory from its type, size, time and
  listing, because there is no inode to compare (wolf-lang#536).
- **`sleep`** sleeps in whole milliseconds, rounding up.
- **`nproc`** counts what `os_cpus` counts, which agrees with GNU under
  an affinity mask and differs under a FRACTIONAL cgroup quota, where it
  rounds down and GNU up (wolf-lang#537; the whole `nproc` file under
  `CPUQuota=150%` is 55 passed and 23 failed, under 200% 78 of 78).

kasumi (linux x86-64, 16 cpus) at load 1.2–1.4, release tier built by
wolf 0.2.20 with the host's clang 22.1.8, GNU coreutils 9.11-2, all
taken between 16:20 and 16:30 EDT on 2026-10-02 — an hour before a
system upgrade moved kasumi to clang 23.1.1 and GNU coreutils 9.12, so
both sides of every row are on the same side of it. The start-up rows are `hyperfine -N` over 300 runs, so
the ratio is real at a fraction of a millisecond; `true` (249 µs
against 177 µs, 0.71x) is the floor every wolf binary here pays. The
`printf` rows are 10,000 arguments built by the shell; `tee` is 256 MiB
of text.

| bench | boreutils | GNU | vs GNU |
|---|---:|---:|---:|
| `sleep 0`, start-up | 258 µs | 227 µs | 0.88x |
| `nproc`, start-up | 290 µs | 231 µs | 0.80x |
| `pwd`, start-up | 261 µs | 209 µs | 0.80x |
| `printenv PATH`, start-up | 261 µs | 204 µs | 0.78x |
| `printf x`, start-up | 270 µs | 208 µs | 0.77x |
| `sleep 0.1` | 100.5 ms | 100.6 ms | 1.00x |
| `sleep 0.0105`, between two milliseconds | 11.4 ms | 10.9 ms | 0.95x |
| `printf '%d\n'`, 10,000 integers | 6.0 ms | 4.1 ms | 0.68x |
| `printf '%x\n'`, 10,000 integers | 6.5 ms | 4.0 ms | 0.61x |
| `printf '%s\n'`, 10,000 words | 5.7 ms | 4.9 ms | 0.86x |
| `printf '%.6f\n'`, 10,000 decimals | 29.8 ms | 8.1 ms | 0.27x |
| `printf '%g\n'`, 10,000 decimals | 41.1 ms | 7.9 ms | 0.19x |
| `printf '%e\n'`, 10,000 decimals | 34.8 ms | 7.8 ms | 0.22x |
| `tee`, no file, to `/dev/null` | 32.5 ms | 22.6 ms | 0.70x |
| `tee FILE` | 124 ms | 158 ms | **1.27x** |
| `tee FILE FILE2` | 265 ms | 305 ms | **1.15x** |

**`printf`'s floating rows cost a big-integer conversion each way, and
were 0.03x before one change.** The first measurement read 0.04x, 0.03x
and 0.04x (218 ms, 227 ms and 220 ms): every argument was divided by a
power of five bit by bit. Dividing by a one-limb divisor in one pass —
every decimal with ten or fewer digits after its point — took them to
0.19x–0.27x, with both random runs re-taken on the faster binary and
still clean. glibc converts in hardware and prints with its own exact
printer; this program has no hardware float in the loop at all, which
is why it can match two different `long double`s.

**`tee` to a file is AHEAD of GNU**, and only there: GNU's copy into a
file swung by ±29 ms across five runs where ours held ±4 ms. Peak RSS
over 256 MiB is 2.9 MB against GNU's 2.2 MB, one `region` per 256 KiB
chunk.

**`ls` is faster than GNU at listing and slower at stat'ing**, and the
difference is one system call per name. kasumi (linux x86-64, load
under 1), release tier, GNU 9.11, `tools/bench --scale 10 --runs 20 ls`
twice (`notes/bu18-ls.md`): `flat/` is 100,000 names, `deep/` 316
directories of 316.

| ls | boreutils | GNU | GNU / boreutils |
|---|---:|---:|---:|
| `flat/`, one per line | 34.4 ms | 78.1 ms | **2.27x** |
| `flat/`, `-C` | 37.5 ms | 92.8 ms | **2.48x** |
| `flat/`, `-S` | 110.9 ms | 106.5 ms | 0.96x |
| `flat/`, `-t` | 111.3 ms | 76.9 ms | 0.69x |
| `-R` of `deep/` | 84.3 ms | 34.9 ms | 0.41x |
| start-up, `-d` of one directory | 0.4 ms | 0.4 ms | tie |

A plain listing stats nothing on either side, and here it sorts names
`fs_read_dir` already sorted. `-S` and `-t` are one stat per name on
both sides. `-R` is the gap: GNU knows a directory from the type the
kernel returns with each name, and wolf's listing returns names only,
so this program must ask of every entry whether it is a directory
(wolf-lang#626). Peak RSS over the 100,000 names is 37 MB against GNU's
28 MB, and `-R` holds 2.8 MB against 2.2 MB: one `region` per
directory, so a walk keeps only the directories it is inside (the first
draft held every listing it had made, 70 MB).

| utility | status | vs GNU |
|---|---|---|
| `true` | done | start-up only |
| `false` | done | start-up only |
| `echo` | done | 1.04x (macOS) |
| `basename` | done | 1.04x (macOS) |
| `dirname` | done | start-up only |
| `yes` | done | 2.74x (macOS), 0.63x (linux) |
| `cat` | done | start-up 1.18x (macOS), 0.97x (linux); bulk copy 0.64x (macOS), **0.73x to 0.91x** (linux, `fs_copy_chunk` since bu19; was 0.04x to 0.08x) |
| `wc` | done | `-w` 1.27x, `-l` 0.92x (macOS, load 13.9); 0.88x, **0.51x** (linux; `-l` through `bytes_count` since bu19, was 0.17x); `-c < f` start-up on both sides since bu15 |
| `head` | done | `-n 1` start-up on both sides; `-n -K` of a file 0.79x since bu15 (was 0.09x), 0.34x through a pipe (linux, bu19; was 0.26x) |
| `tail` | done, `-f` and `--follow[=WORD]` included | a file 0.31 ms against GNU's 0.21 ms since bu15 (was 114 ms); pipe `-c` 0.88x to 0.99x, `-n` **1.82x to 7.11x** since bu19 (`bytes_count`; was 0.57x to 0.64x) (linux) |
| `cut` | done, without 9.11's `-w`, `-F` and `-O` | 0.27x to 0.71x (linux; lines through `bytes_find` since bu19) |
| `tr` | done | 0.34x translating, **3.72x** translating and squeezing (linux) |
| `uniq` | done | 0.46x to **1.03x** (linux) |
| `seq` | done | 0.07x on integers, **1.27x to 1.96x** everywhere else (linux) |
| `nl` | done | 0.51x to **1.20x** (linux) |
| `tac` | done | 0.18x on a stream, **2.09x to 2.79x** under `-r` (linux) |
| `paste` | done | 0.35x to 0.57x (linux) |
| `fold` | done | **1.07x to 5.15x** (linux) |
| `expand` | done | **1.01x to 8.47x** (linux) |
| `unexpand` | done | **1.00x to 9.23x** (linux) |
| `sort` | done: `-bdfhiMnr`, `-k`, `-t`, `-u`, `-s`, `-c`/`-C`, `-m`, `-o`, `-z`, the external merge; not `-g`, `-V`, `-R`, `--debug`, `--files0-from`, `--compress-program` | 0.10x to 0.45x (linux) |
| `tee` | done; `-i` refused, and `-p`/`--output-error` without their broken-pipe branches (wolf-lang#423) | 0.70x to **1.27x** (linux) |
| `printf` | done: every conversion, `%b`, `%q`, `%N$`, `*`; floats exact in the host's `long double` | 0.19x to 0.86x; start-up 0.77x (linux) |
| `printenv` | done; the bare listing sorted (wolf-lang#535) | start-up 0.78x (linux) |
| `pwd` | done; `-L` without an inode (wolf-lang#536) | start-up 0.80x (linux) |
| `sleep` | done, to the millisecond | start-up 0.88x; `sleep 0.1` 1.00x (linux) |
| `nproc` | done; a fractional cgroup quota rounds down (wolf-lang#537) | start-up 0.80x (linux) |
| `ls` | done for names: the formats, sorting, `-F`/`-p`, `-q`, `-N`, `-R`, `-L`/`-H`, and GNU's terminal defaults (bu19); the long format, `-i`, `-s`, `-u`, `-c`, `-U` refused (wolf-lang#625, #626, #536), a link that resolves taken for its target, and a terminal's own width not asked (wolf-lang#643) | **2.27x** listing, 0.41x to 0.96x stat'ing (linux) |
| `env` | not shipped: no exec (wolf-lang#534) | — |

## Drop-in readiness

Can a script call the boreutils program where it called GNU's? This
table answers it per utility, from the evidence and from nothing else.

- **GNU options** are the entries GNU 9.11's own `--help` lists (a short
  and long spelling of one option are one entry), counted as covered
  when a passing differential case exercises the option and this
  program does not refuse it. An option that appears only in a case
  where GNU refuses it too — `sort -ng` — is not counted as covered.
- **Cases** are kasumi's, at this commit: passed / skipped, none failed.
  CI's macOS leg runs the same cases and skips the `/dev/full` ones as
  well, and the `/proc` and `/sys` ones (`requires`, bu15).
- **vs GNU** is the band of the rows in the tables above, kasumi only,
  GNU's time over ours. A start-up row is `hyperfine -N` over 300 runs.
- **The verdict is mechanical.** *Drop-in* when every option is covered
  and every skip is one of the two hosts' C libraries or devices
  disagreeing with each other. *Drop-in for scripts that avoid X* when an
  option is missing or refused, or a skip is this program's own. *Not
  yet* when the utility's central job does not hold. Slowness never
  lowers a verdict; it is the third column.

| utility | GNU options | cases | vs GNU (kasumi) | verdict |
|---|---:|---:|---|---|
| `true` | 2 / 2 | 13 / 0 | start-up 0.71x | drop-in |
| `false` | 2 / 2 | 11 / 0 | start-up 0.72x | drop-in |
| `echo` | 5 / 5 | 45 / 0 | start-up 0.80x | drop-in |
| `basename` | 5 / 5 | 48 / 0 | start-up 0.80x | drop-in |
| `dirname` | 3 / 3 | 27 / 0 | start-up 0.80x | drop-in |
| `yes` | 2 / 2 | 18 / 0 | 0.63x | drop-in |
| `cat` | 12 / 12 | 119 / 0 | 0.27x to 0.97x | drop-in for scripts that never make an input its own output: `cat f >> f` and `cat < f >> f` refuse in GNU (`input file is output file`, status 1) and grow `f` without end here, because nothing in wolf can tell that two descriptors name one file (wolf-lang#424, #536); no case can reach it |
| `wc` | 10 / 10 | 158 / 2 | 0.04x to 0.99x | drop-in; the skips are the hosts' `wcwidth` |
| `head` | 7 / 7 | 160 / 0 | 0.14x to 0.90x | drop-in |
| `tail` | 12 / 14 | 183 / 2 | 0.45x to 7.11x; a file at start-up (0.31 ms against 0.21 ms) | drop-in for scripts that avoid 9.11's `--debug` (refused) and `--max-unchanged-stats` (accepted, no case); the skips are follows that never end |
| `cut` | 10 / 13 | 124 / 0 | 0.27x to 0.71x | drop-in for scripts that avoid 9.11's `-F`, `-w` and the short `-O` (`--output-delimiter` works) |
| `tr` | 6 / 6 | 146 / 0 | 0.34x to 3.72x | drop-in |
| `uniq` | 13 / 13 | 124 / 1 | 0.45x to 1.03x | drop-in; the skip is the hosts' `/dev/stdout` |
| `seq` | 5 / 5 | 122 / 6 | 0.07x to 1.96x | drop-in for scripts that avoid `-f %a`; where GNU's `long double` loops or misrounds, `seq` is exact instead |
| `nl` | 13 / 13 | 104 / 2 | 0.51x to 1.20x | drop-in for scripts that avoid a BRE interval, group or back reference in `-b`, `-h` or `-f p…` |
| `tac` | 5 / 5 | 99 / 3 | 0.18x to 2.79x | drop-in for scripts that avoid `-r` with a group or an alternation |
| `paste` | 5 / 5 | 94 / 0 | 0.35x to 0.57x | drop-in |
| `fold` | 6 / 6 | 100 / 2 | 1.07x to 5.15x | drop-in; the skips are the hosts' `strerror(ERANGE)` |
| `expand` | 5 / 5 | 88 / 0 | 1.01x to 8.47x | drop-in |
| `unexpand` | 6 / 6 | 98 / 0 | 1.00x to 9.23x | drop-in |
| `sort` | 24 / 31 | 326 / 0 | 0.10x to 0.45x | drop-in for scripts that avoid `-g`, `-V`, `-R`, `--random-source`, `--debug`, `--files0-from` and `--compress-program`, each refused by name |
| `tee` | 5 / 6 | 62 / 7 | 0.70x to 1.27x | drop-in for scripts that avoid `-i` (refused) and do not need `-p` or `--output-error` to survive a reader that leaves early (wolf-lang#423) |
| `printf` | 2 / 2, and all 19 conversions | 270 / 0 | 0.19x to 0.86x | drop-in |
| `printenv` | 3 / 3 | 33 / 4 | start-up 0.78x | drop-in for scripts that name their variables; the bare listing is sorted (wolf-lang#535) |
| `pwd` | 4 / 4 | 44 / 1 | start-up 0.80x | drop-in for scripts that avoid `-L` with a `$PWD` naming a same-time twin of the working directory (wolf-lang#536) |
| `sleep` | 2 / 2 | 61 / 0 | start-up 0.88x, `sleep 0.1` 1.00x | drop-in |
| `nproc` | 4 / 4 | 78 / 0 | start-up 0.80x | drop-in outside a fractional cgroup cpu quota (wolf-lang#537) |
| `ls` | 33 / 60 | 262 / 30 | 0.41x to 2.48x; start-up a tie | drop-in for scripts that read NAMES and avoid the long format and what implies it (`-l -g -n -o --full-time`), `-i`, `-s`, `-u`, `-c`, `-U`/`-f`, `-v`, the quoting styles but `-N`, the colour and filtering options (each refused by name), and do not need `-F`, `-p`, `-S`, `-t` or `-R` to tell a link that resolves from its target (wolf-lang#625, #626, #536); on a terminal, one 80 wide or reporting no size (wolf-lang#643) |
| `env` | 0 / 14 | not shipped | — | not yet: no exec (wolf-lang#534) |

**16 drop-in, 12 drop-in for scripts that avoid a named thing, 1 not
yet** (`wc` became drop-in at bu19, when the host's reason arrived). The same evidence read across: no shipped utility fails a case,
and every skip that is this program's own names the wolf issue behind
it.

**How much of GNU coreutils this is.** GNU coreutils 9.11 documents
**103 utilities** (its info manual's `invocation` nodes, the four SHA-2
sums counted as one and `[` as `test`; Arch's build installs 102
binaries and leaves out `arch`, `chcon`, `runcon`, `hostname`, `kill`
and `uptime`). boreutils ships **28 of them, 27%**, and `env` is the
29th row above. Effort is not what blocks most of the other 76: wolf
0.2.26 has no surface for them, and each gap boreutils has met is filed
upstream with its witness. The OS surface lane's first cut, s199's
wolf-lang#426 and #424 (seek, tell, the positional read, and the
standard descriptors), shipped in 0.2.22, and `tail`, `head` and `wc`
use it (bu15).

- **#346**, no permission surface: `chmod`, `install -m`, `mkdir -m`,
  `mkfifo`/`mknod -m`, `mktemp`'s private file, `cp -p`.
- **#405** (closed, wolf 0.2.26): descriptors 0, 1 and 2 are read and
  written directly; every utility here does (bu19).
- **#407** (closed, wolf 0.2.26): `os_error`/`os_error_text` give the
  host's reason; every utility here says it (bu19). The net and os
  families do not set it yet (wolf-lang#609).
- **#411** (closed, wolf 0.2.26): `bytes_count`/`bytes_find`; `wc -l`,
  `head`, `tail`, `nl`, `uniq` and `cut` find lines with them (bu19).
  There is no backward scan, so `tail`'s walk back from the end still
  compares a byte at a time.
- **#416**, a streaming read allocates and the ambient region never
  frees: worked around here with one `region` per chunk.
- **#417** (closed for files, wolf 0.2.26): `fs_copy_chunk`; `cat`'s
  plain path uses it (0.73x to 0.91x on linux, from 0.04x to 0.08x).
  Its read/write rung loses the bytes it read when the write fails
  (**#642**), which `cat` works out from the failure's shape.
- **#643**, no way to ask a terminal its size: `ls -C` on a terminal
  wider or narrower than 80; `stty size`, `tput cols`.
- **#644**, a region's exit frees to `malloc`: a streaming program's
  system time follows glibc's trim heuristics (`cut` on short lines
  moved +42% from an unrelated start-up change).
- **#423**, no signal disposition but four meanings: `tee -p`/`-i`
  here; `timeout`, `kill`, `nohup` and `env --ignore-signal` beyond.
- **#424** (closed, wolf 0.2.22): `fs_fstat`, `fs_seek`, `fs_tell` and
  `fs_read_at` see descriptors 0, 1 and 2; `wc -c` and `tail` on a
  redirected regular file use them (bu15). `cat`'s input-is-output
  refusal still waits on #536.
- **#426** (wolf 0.2.22): seek, tell and the positional read exist;
  `tail`, `head` and `wc` use them (bu15). `tac` does not yet; `dd
  skip=`/`seek=` could; `truncate` and `shred` need a truncate call
  that does not exist.
- **#534**, no exec and no inherited stdin for a child: `env`, `nice`,
  `nohup`, `timeout`, `chroot`, `stdbuf`.
- **#535**, the environment listed only sorted: `printenv` and `env`.
- **#536**, no file identity: `cp`/`mv`/`ln`'s same-file refusals,
  `du`'s hard links, `ls -i`, `stat`, `pwd -L`.
- **#537**, `os_cpus` rounds a fractional quota down: `nproc`.
- **#538**, `wrapping[u64]` prints signed and cannot be divided
  natively: worked around in `src/bore/u64.lu`.
- **#625**, no `lstat`, no `readlink`, and no stat record past kind,
  size and modification time (mode, link count, owner, group, blocks,
  atime, ctime): `ls -l` and every `ls` option that must tell a link
  from its target, `stat`, `readlink`, `realpath`, `du`, `find`-shaped
  walks, `cp -P`, `test -h`.
- **#626**, `fs_read_dir` sorts, fails on one name that is not UTF-8,
  and gives no entry type: `ls -U`/`-f`, and every walk pays a stat per
  entry (`ls -R` is 0.41x for it).

Beyond those, the host builtin table at 0.2.25 has no call that creates
a link (`ln`, `link`), changes a mode, an owner or a time (`chmod`,
`chown`, `chgrp`, `touch`), names a user or a group (`id`, `whoami`,
`groups`, `logname`, `users`, `who`, `pinky`), formats calendar time
(`date`), or asks a terminal its name or settings (`tty`, `stty`;
`os_isatty` exists since 0.2.26). Those are not filed yet; each will be, with
its witness, by the lane whose utility meets it first (B6, the census).
