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
tools/texttest            # shuffle shape plants and bounded codec round-trips
tools/checksumtest        # independent digest answers, manifests and bounded memory
tools/checksumtest --large # >4 GiB answers on release and dev (build both tiers first)
tools/killtest --gnu DIR  # kill where it sends: a throwaway container a case
tools/killprobe --gnu K P # kill -l and -t of every number 0..140000 and a sample above, against GNU
tools/timeouttest --gnu DIR # timeout where it runs a command: a throwaway container a case
tools/idtest --gnu DIR    # the identity tools as root and as users: the same
tools/bench --scale 0.01  # hyperfine against GNU on generated inputs
```

GNU coreutils is the oracle and must be installed: natively on linux,
`brew install coreutils` on macOS, where the harness uses the
`g`-prefixed names. It must be the version `gnu-oracle.toml` names, and
`tools/difftest` says so and stops when it is not — see **The oracle of
record** below. Since `kill` (bu23) an installed coreutils is not
enough on any host: no distribution's package holds coreutils' own
`kill` (the one on your PATH is procps' or util-linux's, and the one
your shell runs is its builtin), so `tools/fetch-oracle` builds the
oracle with it and `tools/difftest` refuses any other `kill`.

The oracle build also enables GNU's optional `arch`, `hostname` and
`uptime`, and verifies their version identities. The `--without-selinux`
build does not install `chcon` or `runcon`; those two have separate,
explicitly field-only GNU 9.4 checks, not GNU 9.11 parity claims.

**Windows is out of scope**: the oracle of record is a unix build of GNU
coreutils, and CI runs on linux and macOS. (The reason used to be that
the only byte-exact route to standard input and output was reopening
`/dev/stdin` and `/dev/stdout`; since wolf 0.2.26 boreutils reads
descriptor 0 and writes descriptor 1 directly, bu19.)

## Standard output, and the exit convention

Every boreutils program uses the shared byte-output helpers, buffered or
streaming, and honours one convention, stated in full at the top of `src/bore/bore.lu`
and measured black-box against GNU:

- **A write that fails is status 1 and one diagnostic** (`expr` follows
  GNU by using status 3 for its output errors). `basename a/b
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

Every shipped utility below is byte-for-byte identical to GNU coreutils 9.11 on
its differential corpus, except where a case says otherwise and is
skipped with its reason. The combined corpus holds **16,549 cases across 105 case files**; `kill` has
365 more that SEND, each run in a container of its own (`tests/kill/`,
`tools/killtest`: **365 passed, 0 failed** on hasu at bu30, groups,
`kill 0` and `kill -1` among them), `timeout` 163 more that run a
command (`tests/timeout/`, `tools/timeouttest`: **150 passed, 0
failed** on hasu at bu30, and 13 skipped there: twelve that need a
core written as a file, which run on CI's ubuntu runner, and one of
macOS's), and the six identity tools 1,126 more that
run as root and as users or change an owner (`tests/ids/`,
`tools/idtest`: 28 of them only on CI's macOS runner). The prior text-tool measurement in an unprivileged Ubuntu 24.04 container on hasu
(linux x86-64, CPUs 0–5), at wolf 0.2.35 / lupin 0.1.56 with bundled
std `2386522e`, answers **8,005 passed, 0 failed, 157 skipped** on both
release and dev (before: 7,020 / 0 / 130). Six utilities add 1,012 cases:
985 pass and 27 explicitly name the two refused behaviours below. Random
`mktemp` names are checked by fixed prefix, suffix, replaced X count,
alphabet, object kind and private mode, never compared byte for byte.
`tty` has standard-input pty cases, separate from standard-output ptys.

The newest tools are `split`, `csplit`, `fmt`, `pr`, `ptx`, `od`,
`expr`, `numfmt`, `factor` and `basenc`. Their **2,140 registered cases**
contain 2,129 GNU comparisons and 11 explicitly named exceptions.
One factor case contains a separate deterministic corpus of **10,000
full-range unsigned 64-bit integers**. The toolchain remains wolf **0.2.35** / lupin **0.1.56**, bundled
std `2386522e`; the oracle remains **GNU coreutils 9.11**, `LC_ALL=C` and
`_POSIX2_VERSION=200112`.

`split` supports byte, line, bounded-record and numbered/round-robin
partitions, automatic alphabetic/numeric/hex suffix growth, and shell
filters. Its two named GNU divergences are documented below and checked
independently. `csplit` uses the vendored clean-room BRE engine, preserves
unterminated input, and compares both byte counts and resulting files.
For files they create themselves, both splitters refuse paths that resolve
to the input inode before truncation; GNU csplit instead loses its input in the collision described
below.
`fmt` has indentation, prefix, sentence and fresh generated word-length
corpora; `pr` fixes input mtimes for header comparisons and checks form
feeds, columns, line numbers and tab stops. `ptx` implements GNU-mode
context indexing and roff/TeX output, with `-G` explicitly refused.
`od` covers character/integer formats and IEEE half, bfloat16, binary32,
binary64 and x87 decimal output through the repository's own exact
floating formatter. `numfmt` measures halfway rounding and host
long-double arithmetic, including field delimiters, invalid-input modes,
conversion/printing range boundaries and UTF-8 format literals.

`factor` combines trial division, deterministic Miller–Rabin and an
independent Montgomery/Brent–Pollard-rho design. `expr` evaluates the full
token grammar with lazy Boolean operations and anchored first captures;
its arithmetic operands and results have up to 64 magnitude bits, with a
separate sign. Pure string operations and decimal comparisons do not have
that arithmetic limit. Unsupported arithmetic and larger factor inputs
are refused by name rather than wrapped or truncated
([wolf-std#100](https://github.com/wolffe-lang/wolf-std/issues/100)).
`basenc` shares the existing base64/base32 codec and adds the URL/hex
alphabets, hexadecimal, both bit orders and Z85. GNU 9.11's additional
`--base58` and `numfmt --debug` are explicitly not implemented.

The new independent witnesses run through the existing `tools/texttest`
CI entrypoint. They check the named refusals and GNU divergences, a
32 MiB Z85 round trip, live round-robin output before EOF, input-inode
preservation, and bounded numeric/context-record allocations. Non-round-robin
`split` partitions, `csplit`, `fmt`, `pr`, `ptx` and `od` currently retain
input in memory; this pass makes no constant-memory claim for those readers.
No new utility has been speed-benchmarked.

The identity/terminal family adds fifteen command binaries representing
fourteen utility units: `date`, `test` and `[`, `uname`, `hostname`,
`hostid`, `arch`, `uptime`, `users`, `who`, `pinky`, `pathchk`, `stty`,
`chcon` and `runcon`. Its 3,658 differential cases use fixed date inputs,
constructed Linux utmp records and input ptys. The container-only
`tests/identity-terminal/check.py` compares complete termios state,
not just exit status, and checks synthetic live/stale login records.
`selinux-field.py` separately labels every comparison against GNU 9.4;
`access-not-yet.py` checks ordinary kernel-access parity and the two
GNU-shared differing-id limitations.
Linux CI runs all three inside a disposable Ubuntu 24.04 container.

The preceding text-tool pass added `base64`, `base32`, `comm`, `join`, `tsort` and
`shuf`. Both codecs stream in bounded chunks, including malformed padding
and decode groups split across reads. `comm` supports suppressed columns,
custom delimiters, order diagnostics and totals; `join` supports selected
fields, Cartesian groups, unpaired records, headers and automatic output
fields. Comparisons are under `LC_ALL=C`. These two merge tools currently
retain their records in memory. `shuf` checks compare sample count,
membership and multiplicity independently on each side, including output
files, never random order. It supports the full unsigned 64-bit input
range. Head counts saturate at INT64_MAX (9,223,372,036,854,775,807),
independently of the unsigned range endpoints. It refuses `--random-source` by name: GNU's general byte-draw rule
has not been derived. `tsort` matches GNU's byte order on all 29,849
labelled DAGs of three through five nodes and 36,815 edge-order variants,
and supports simple/disjoint cycles. Once all zero-indegree nodes have
been emitted, a cyclic residual must have exactly one live incoming and
one live outgoing edge per node; complex cyclic components and cycles
with outgoing tails are refused by name. The measured GNU answers and
those refusals are retained in `notes/bu31/refusals.jsonl`.

Before the disk/process pass, the combined tree had **10,380 differential cases** across **70 case files**,
counted directly from the checked-in TOML records. All six text tools and
the checksum family are included. The checksum pass adds nine command binaries and **2,218 cases**: 2,213
passed and five named skips on both native tiers. That earlier whole differential
combined corpus was **10,218 passed, 0 failed, 162 skipped** in the hasu B Ubuntu
24.04 container. The new commands are `cksum`, `sum`, `md5sum`, `sha1sum`,
`sha224sum`, `sha256sum`, `sha384sum`, `sha512sum` and `b2sum`. Their
algorithms are written from POSIX's CRC definition, RFC 1321, FIPS 180-4
and RFC 7693. Twelve wolf test programs include published short/long
vectors and synthetic 128-bit counter carries; the million-`a` program
runs through the toolchain's explicit native fallback when its checked
step budget is exhausted. Ten independent executable tests per tier
cover encoded manifests, escaped names, malformed bytes and bounded RSS.
A separate `--large` test independently hashes a sparse input of
4,295,032,833 bytes and compares all seven digest commands on both tiers;
the two CRCs and BSD/SysV sums compare with GNU on that input too.

The disk/process pass adds `du`, `dd`, `install`, `mknod`, `shred`,
`dir`, `vdir`, `dircolors`, `chroot`, `nice`, `nohup` and `stdbuf`:
**317 new differential cases**, with 19 named surface/implementation skips.
The complete rootless Ubuntu 24.04 run on hasu (CPUs 6–11) at
`a443350` passed **10,516 cases, 0 failed, 181 skipped** on both
release and dev; the full unit and auxiliary gates passed too. The
separate four-CPU process integration passed **74 checks, 0 failed,
0 skipped**.
`ls`, `dir` and `vdir` share one listing engine; the latter two default to
`-C -b` and `-l -b`. The color database is emitted with original comments;
a separate semantic check feeds it to GNU and verifies identical color rules.
The container-only integration suite (`python3 -I tests/disk-process/check.py`,
with `BORE_DISK_CONTAINER=1`) tests tty descriptors, hangup survival, injected
read failures, short records, EBCDIC compositions, overwrite pass shapes,
random sources and dynamic/static/wolf buffering witnesses. Run it only in a
throwaway Ubuntu container, with both tiers built.

`df` is **blocked**, not shipped: wolf 0.2.35 has no `statfs`/`statvfs`
record (wolf-lang#686), despite PAX implementing those Linux calls. The
compiler witness is `tests/gaps/bu34/statvfs/main.lu`; a blocked PAX row for
its ext2 `/dev/vda2` root and tmpfs `/tmp` is drafted in
`tests/gaps/bu34/pax-df.toml`, not run here. `chroot` likewise refuses its
central operation, because `os_chroot` does not exist. `nice` reads Linux
niceness from `/proc/self/stat` and can execute an explicit `-n 0`; other
adjustments refuse rather than silently executing unchanged. `stdbuf`
requires an explicit `BORE_STDBUF_AWARE=1` opt-in from children honoring
`_STDBUF_*`; it does not claim to affect arbitrary libc or wolf programs.
GNU's preload affects dynamic libc streams but not static libc or raw wolf IO.

Named limits remain: `du --files0-from` and custom time directives outside
`%F %T %Y %m %d %H %M %S %s %%`; `dd`'s unavailable open flags,
`conv=nocreat`, and buffers above 16 MiB; `install`'s strip/SELinux/debug
options; `mknod b/c/u` (wolf-lang#705); `shred`'s default block rounding
(no `st_blksize`, #684), name wiping (#706), schedules above 25 passes,
and write-only operands without `-f` (no non-creating writable open without
read access). Use `shred -x` and `--remove=unlink` for its supported shape.
`shred -f` changes permissions only after open failure; the pinned O_RDWR
surface temporarily needs owner read/write, then the GNU recovery mode 0200
is immediately restored on the live descriptor. No overwrite utility promises
physical erasure on flash, CoW, snapshots or backups.

The pin alone preserved **6,668 / 0 / 120** on both tiers, as at
0.2.34 (bu29, `notes/bu29-the-pin-0234.md`). The container-suite
figures above were re-measured on hasu; inouttest is 104 / 0 / 0 and
roottest 178 / 0. `timeout` now disables
its own core with `os_core_off()` before re-raising; the three core rows
compare directly with GNU, with `-s 33` still a named design difference.
The edition before
bu28 said 6,784 cases and 6,664 passed, 0 failed, 120 skipped at wolf
0.2.32, and `tools/timeouttest` 124 passed, 0 failed (bu27's figures
are in `notes/bu27-the-groups.md`). The edition before bu27 said
6,645 cases and 6,383 passed, 0 failed, 262 skipped, and
`tools/killtest` 338 passed, 0 failed (bu24's and bu26's figures are in
`notes/bu24-the-ids.md` and `notes/bu26-the-kill-cases.md`). The edition before bu24 said 6,514
cases and 6,252 passed, 0 failed, 262 skipped, and `tools/killtest`
335 passed, 0 failed (bu23's figures are in `notes/bu23-the-kill.md`).
The edition before bu23's `kill` said 5,646 cases and 5,527 passed, 0
failed, 119 skipped (bu22's figures and CI's are in
`notes/bu22-the-modes-and-links.md` and its PR). The edition before
bu22's `chmod`, `touch`, `ln`, `mkdir -m` and
`cp -p` said: a run on kasumi (linux x86-64) at this pin answers
**4,476 passed, 0 failed, 118 skipped** of 4,594, the same list on the
release and the dev tier, and CI's
macOS leg skips the `/dev/full` and `/proc` cases besides, because
macOS has neither, and the cases that print an owner's NAME, because a
Mac's accounts are not in `/etc/passwd`: run 38124071375 answers 4,477
and 117 skipped on ubuntu and 4,337 and 257 skipped on macOS, none
failed (bu21's figures are in `notes/bu21-the-file-changers.md`). (The previous edition of this
sentence, before bu21's five utilities that change the file system,
said 3,855 cases, 3,788 and 67 on kasumi, and 3,789 and 66 on ubuntu
and 3,649 and 206 on macOS, run 38116093735; before bu20's long format and its three utilities, it said 3,077
cases, 3,017 and 60 on kasumi; before bu19, 3,048 cases, 2,986 and 62; before
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

**`ls` had thirty skips, every one wolf's, and wolf 0.2.27 answered
twenty-eight of them** (bu20). s218's `fs_stat`, `fs_lstat`,
`fs_read_link` and `fs_read_dir_entries` give a file's whole record, a
link's own identity and target, and the directory's own order, so the
long format and what implies it, `-s`, `-i`, `-u`, `-c`, `--time`,
`-U`, and every option that must tell a link from its target are
ordinary cases now: the file holds 710, and kasumi answers 694 and 16
skips. Six of the sixteen are `-f` and `-aU`, where `.` and `..` stand
in the directory's own order and the listing call leaves them out
(wolf-lang#692: right on btrfs, tmpfs and APFS, wrong on ext4); two are
a terminal whose own width is not 80 (wolf-lang#643); one is `-Z`, a
security context (no extended attribute, wolf-lang#685); the four former option gaps (`--author`, `--block-size`,
`--time-style=+FORMAT`, `-Q`) now run (bu36); and three are
block devices this host does not have.

**`stat`, `readlink` and `env` add twenty-one skips, and none is a C
library's** (bu20). `stat`'s eight: `-f` twice (no file-system record,
wolf-lang#686), `-` (no record of an open handle, #536), `%o` (no I/O
block size, #684 — the default and terse formats run, with that one
field masked on both sides), `%C` (#685), and three block devices this
host lacks. `readlink` has none. `env`'s thirteen: five listings that
start from the inherited environment, which wolf lists only sorted
(#535); an entry with an empty name, which `os_exec` refuses; a script
found through an empty `PATH` component, which sees `./name` where
GNU's sees `name` (#689); and six options not written yet (`-S`, `-v`,
the four signal options), refused by name.

**`kill` adds one skip, a non-UTF-8 argument (#406)** (bu27). Until
bu27 it added 143 on linux: every case naming a signal the host has and
wolf had no meaning for. Since wolf 0.2.31 (s241) a host signal is sent
as `-N`, `os_signal_last` and `os_signal_realtime` say how the host
numbers them and `os_signal_text` gives their words, so `kill` knows
every signal the host numbers (linux's `STKFLT`, `POLL`, `PWR` and the
real-time range by GNU's names, macOS's `EMT`, `IO`, `INFO`) and `-t`
prints the third column. `tools/killprobe` holds `-l` and `-t` to GNU
over 240,578 numbers on both hosts, in every CI run since bu28, with no
row by design: since wolf 0.2.33 `os_signal_text(0)` gives signal 0's
words (`Unknown signal 0`), so the 912 rows a tier that read as signal 0
(`EXIT`, 128, 256, …), and 84 cases' masks, are gone. The cases that SEND
are not skipped: where this `kill` answers otherwise by design (a `kill
0` from process group 1, which wolf never signals),
`tests/kill/cases.toml` states both answers and both are asserted.

**`timeout` adds seven skips, all on macOS**, where GNU 9.11 warns
`setitimer: Invalid argument` for a DURATION past its timer's range and
this timeout says nothing (bu27). Since wolf 0.2.33 (bu28) it sends
its group a fault or host signal (`-s SEGV`, `-s RTMIN`, `-s 16`) as
GNU's does, ignoring it first, where it refused them (125); it dies of
the signal its command died of, a fault's included, where it exited
139; and it says `the monitored command dumped core`. It never starts a command on a lane's host:
`tools/difftest` runs only its cases that cannot (usage, invalid
durations and signals, 126 and 127), and the rest run in
`tools/timeouttest`.

**The file changers add thirty-five skips, and every one is a thing wolf
cannot do to a file or an option not written** (bu21, bu22). Since wolf
0.2.28 (s230) a mode can be given at creation and changed, a link of
either kind made, a time set and the umask read, and `chmod`, `touch`,
`ln`, `mkdir -m` and `cp -p` are written on them (bu22). `mkdir` and
`rmdir` have none. `chmod` has none on linux (on macOS, seven: GNU
changes a link's own mode there and wolf has no call for it). `touch` now shares date's clean-room free-form grammar, including relative
items, English month names and `MM/DD/YYYY`, plus independent `-r -d`
reference times. Its four remaining skips are `touch -` twice (times by
handle, wolf-lang#714), noon and unknown grammar. See
[the date grammar](docs/touch-date-grammar.txt). `ln`'s three: `-b`, `--backup`, `-S`, not
written. `rm`'s three: `--no-preserve-root` twice, refused on
purpose, and `--preserve-root=all`, not written yet. `mv`'s eight:
`--exchange` (no rename that swaps, #706) and seven for `-u`, `-b`,
`-S` and `--debug`, not written yet. `cp`'s nineteen: `-a`, `-d` and
`--preserve=links`, `xattr`, `context`, `all` (hard links among the
sources are not tracked; no extended attribute, #685); `-s` and `-l`,
not written; one fifo (#705); five for `--sparse` and `--reflink` with
anything but `auto` (#703); and five options not written yet. The
OWNER is the one thing `cp -p` cannot keep (#701): a copy whose owner
or group came out other than its source's says so by name, status 1.
Every refusal is BY NAME, status 1, and leaves nothing wrong behind.
**And `rm -r /` is refused as GNU refuses it, which is run, not read:**
`tools/roottest` hands `/` and its spellings to both tiers of `rm` in
a throwaway container — no mount, no network, as a user and as root
inside — beside GNU 9.11, thirty cases with `mv`'s and `cp`'s, a
sentinel tree summed before and after (`tests/root/cases.toml`; CI's
ubuntu leg).

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

**The long format, and what else a record buys (bu20, wolf 0.2.27).**
kasumi, release tier, GNU 9.11, `hyperfine -N`, 15 runs, every side of
a row in one call, at this branch's head `9633593` from a clean tree
(`~/lanes/bu20/bench.sh`, log `~/lanes/bu20/ev/bench.log`; the trees are
`tools/bench --scale 10`'s). The load was NOT quiet — 2.3 when the run
began and 8 when it ended, other lanes building — so the σ of the later
rows is wide and a difference under 10% is not a finding. "0.2.26" is
trunk's `ls` before this lane.

| ls, 100,000 names | 0.2.26 | this `ls` | GNU | GNU / this |
|---|---:|---:|---:|---:|
| `flat/`, one per line | 38.2 ms | **29.0 ms** | 57.8 ms | **1.99x** |
| `flat/`, `-C` | 43.1 ms | **34.2 ms** | 67.0 ms | **1.96x** |
| `flat/`, `-S` | 147.6 ms | 161.6 ms | 109.3 ms | 0.68x |
| `flat/`, `-t` | 140.0 ms | 151.5 ms | 91.1 ms | 0.60x |
| `-R` of `deep/` | 100.3 ms | **28.9 ms** | 27.2 ms | 0.94x |
| `flat/`, `-l` | refused | 196.5 ms | 239.7 ms | **1.22x** |
| `flat/`, `-n` | refused | 185.0 ms | 250.2 ms | **1.35x** |
| `flat/`, `-s` | refused | 153.8 ms | 139.7 ms | 0.91x |
| `flat/`, `-i` | refused | 166.8 ms | 118.1 ms | 0.71x |
| `flat/`, `-F` | a link taken for its target | 151.0 ms | 115.7 ms | 0.77x |
| `flat/`, `-U` | refused | 26.0 ms | 16.1 ms | 0.62x |
| `flat/`, `-lU` | refused | 155.1 ms | 199.7 ms | **1.29x** |
| `-lR` of `deep/` | refused | 122.1 ms | 214.1 ms | **1.75x** |

Read the `-l` rows with their floor beside them. **The floor of a long
listing is one stat per name, and both sides are on it:** `strace -c`
counts 99,998 `statx` for GNU and 100,003 for this `ls` over the same
99,998 names. But GNU makes a SECOND call per name, 99,998
`llistxattr`, to decide the `+` it prints after a mode for an ACL
(201,751 system calls in all, against 100,327 here). This `ls` cannot
make that call (wolf-lang#685), so part of the 1.22x is work not done,
not work done faster; where GNU has no second call (`-s`, `-i`, `-F`)
this `ls` is 0.71x to 0.91x. `-R` went from 0.27x to level because a
directory is known from the type the listing hands back, and a plain
listing got faster because names `fs_read_dir` already sorted are no
longer sorted again. `-S` and `-t` are slower than GNU and no faster
than 0.2.26: they read the whole record where 0.2.26 asked for the size
or the time alone, and in exchange sort a link by the link's own size
and time, as GNU does. Peak RSS for `-l` of the 100,000 names is **174
MB against GNU's 29 MB**: every list in a listing's region grows by
doubling and nothing is given back until the listing ends, and no call
can reserve a list's room (wolf-lang#416). A plain listing holds 33 MB
(0.2.26: 37 MB; GNU: 28 MB).

| start-up and small work (kasumi, load 8, at `9633593`) | boreutils | GNU | GNU / boreutils |
|---|---:|---:|---:|
| `stat -c %s` of one file (`hyperfine -N`, 300 runs) | 279 µs | 215 µs | 0.77x |
| `stat -c '%s %n'` of 10,000 files | 19.4 ms | 13.3 ms | 0.69x |
| `stat -t` of 10,000 files | 29.2 ms | 22.0 ms | 0.75x |
| `readlink` of one link (300 runs) | 275 µs | 211 µs | 0.77x |
| `env true` (300 runs) | 438 µs | 341 µs | 0.78x |

**The file changers (bu21, wolf 0.2.27).** kasumi (btrfs), release
tier, GNU 9.11, `tools/bench` with its new `prepare` step — every timed
run starts from a tree put back by the host's own `cp` or `rm` — ten
runs a side, at `546a656` (`~/lanes/bu21/bench.sh`, log
`~/lanes/bu21/ev/bench.log`). **The load was between 5 and 9,
other lanes building, so a difference under 10% is not a finding.**

| bench | boreutils | GNU | GNU / boreutils |
|---|---:|---:|---:|
| `cp` of one 1 GiB file | 18.2 ms | 18.1 ms | 1.00x |
| `cp -r` of `deep/`, 99,856 files in 316 directories | 1,680 ms | 1,208 ms | 0.72x |
| `cp -r` of `flat/`, 100,000 files in one directory | 1,811 ms | 1,353 ms | 0.75x |
| `rm -r` of a copy of `deep/` | 933 ms | 893 ms | 0.96x |
| `rm -r` of a copy of `flat/` | 982 ms | 999 ms | 1.02x |
| `mkdir -p`, a thousand deep | 21.0 ms | 7.8 ms | 0.37x |
| `mkdir -p` of a hundred deep, twice | 1.8 ms | 1.4 ms | 0.78x |
| `rmdir -p`, a hundred deep | 1.1 ms | 1.0 ms | 0.94x |
| `mv` of a hundred files into a directory | 2.2 ms | 2.0 ms | 0.92x |
| start-up, `mkdir -p .` (`hyperfine -N`, 300 runs) | 331 µs | 238 µs | 0.72x |
| start-up, `rmdir` of a missing name | 358 µs | 257 µs | 0.72x |
| start-up, `rm -f` of a missing name | 320 µs | 279 µs | 0.87x |
| start-up, `mv -n` of a missing name | 350 µs | 354 µs | 1.01x |
| start-up, `cp -n` of a missing name | 391 µs | 358 µs | 0.92x |

(The `rm -r` of `flat/` row is the first of two later takes, 982 and 987
ms against 999 and 1,000 — `~/lanes/bu21/ev/bench-rm-again.log`. In the
run of record that one row read 2,029 ms against 958, with a σ of 128,
while another lane's build took the load from 5 to 9; the three other
takes of it, one from an earlier run at load 12, are all within 3% of
GNU.)

Read each row with what both sides ask the kernel for. **One 1 GiB
file is the cost of asking, not of copying:** on btrfs GNU's clone
`ioctl` and `fs_copy_chunk`'s `copy_file_range` both end in shared
extents, a few tens of milliseconds for a gigabyte; on a file system
that cannot share, both sides copy in the kernel and the row would be
the disk's. **`rm -r` is level with GNU** though it names whole paths
where GNU names entries relative to an open directory (wolf-lang#707):
`strace -c` over 10,000 files in 100 directories counts 10,000
`unlink` and 101 `rmdir` here against GNU's 10,101 `unlinkat`, and 205
`statx` — one per directory and link, never one per file, because the
listing says which entries are plain. **`cp -r` is three quarters of
GNU's speed, and most of the gap is the builtin's:** per file GNU makes
about seven system calls and this `cp` nineteen, eleven of them inside
`fs_copy_chunk` — a duplicate of both handles for every call, and a
second call with a confirming read to learn that a two-byte file has
ended (wolf-lang#709). **`mkdir -p` a thousand deep is 0.37x:** one
`mkdir(2)` per prefix means the kernel walks 1 + 2 + … + 1,000
components, where GNU changes directory as it goes; a path of ordinary
depth is start-up on both sides.

## Checksums on a 256 MiB input

Hasu, Linux x86-64, CPUs 6–11 inside Ubuntu 24.04, 12 GiB cap; wolf
0.2.35 release tier against GNU 9.11. These are three-run medians on a
warm, sparse zero-filled file, rebuilt at `d6f0fbb` before the text-tool
rebase and portable errno-diagnostic changes; the digest algorithms are
unchanged. Speed is recorded, not gated. The digest
engine retains one 64 KiB input chunk and at most 128 pending bytes;
peak RSS is gated separately on 8 MiB and 256 MiB inputs.

| algorithm / command | boreutils | GNU | GNU / boreutils |
|---|---:|---:|---:|
| POSIX CRC / `cksum` | 563.3 ms | 26.4 ms | 0.05x |
| BSD / `sum` | 343.3 ms | 323.5 ms | 0.94x |
| SysV / `sum -s` | 249.9 ms | 35.6 ms | 0.14x |
| CRC32B / `cksum -a crc32b` | 503.0 ms | 29.8 ms | 0.06x |
| `md5sum` | 974.7 ms | 311.5 ms | 0.32x |
| `sha1sum` | 1006.1 ms | 293.7 ms | 0.29x |
| `sha224sum` | 1779.3 ms | 613.5 ms | 0.34x |
| `sha256sum` | 1761.3 ms | 611.7 ms | 0.35x |
| `sha384sum` | 1089.5 ms | 434.6 ms | 0.40x |
| `sha512sum` | 1086.5 ms | 436.1 ms | 0.40x |
| `b2sum` | 986.6 ms | 239.0 ms | 0.24x |

These are scalar standards implementations, not hardware-dispatched
ones. `cksum -a sha3`, `-a sm3` and hardware `--debug` refuse by name.
All checksum file names must be UTF-8; a valid checksum-list record
whose name needs a raw-byte path refuses explicitly because wolf's
`fs_open` takes a `str` path. A non-UTF-8 byte in a `#` comment is still
ignored. MD5 and SHA-1 remain compatibility checksums, not choices for
new security-sensitive designs.

## Command status

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
| `ls` | done: the formats, the long format and its family (`-l -g -n -o -G --full-time --time-style`), `-s`, `-i`, `-u`, `-c`, `--time`, sorting and the unsorted orders, every mark of `-F`, `-q`, `-N`, `-R`, `-L`/`-H`, GNU's terminal defaults; not the `+`/`.` after a mode (wolf-lang#685), a terminal's own width (#643), or where `.` and `..` stand under `-f` (#692) | **1.22x to 1.99x** plain, in columns and long; 0.60x to 0.91x where each name is stat'ed and GNU asks nothing more (linux) |
| `stat` | done: the default and terse formats, `-c`/`--printf` with every directive but `%o` and `%C`, `-L`; not `-f` (wolf-lang#686) or `-` (#536) | start-up 0.77x; 10,000 operands 0.69x to 0.75x (linux) |
| `readlink` | done: the target, and `-f`, `-e`, `-m` by a walk written here | start-up 0.77x (linux) |
| `env` | done by exec: `-i`, `-u`, `NAME=VALUE`, `-C`, `-a`, `-0`, 125/126/127; the inherited environment in sorted order (wolf-lang#535); not `-S`, `-v` or the signal options | `env true` 0.78x (linux) |
| `mkdir` | done: `-p`, `-v`, `-Z`, `-m` (as GNU makes it: under no mask, fixed after only where the MODE says) | start-up 0.72x; `-p` a thousand deep 0.37x (linux) |
| `rmdir` | done: `-p`, `-v`, `--ignore-fail-on-non-empty` | start-up 0.72x (linux) |
| `rm` | done: `-f`, `-r`, `-d`, `-v`, `-i`, `-I`, `--interactive`, `--one-file-system`; a link never followed; `/`, `.` and `..` refused; not `--no-preserve-root` (on purpose) or `--preserve-root=all` | start-up 0.87x; `-r` of 100,000 files 0.94x to 1.02x (linux) |
| `mv` | done: one rename, into a directory, `-f`, `-i`, `-n`, `-v`, `-T`, `-t`, `--strip-trailing-slashes`, `--no-copy`; ANOTHER FILE SYSTEM REFUSED by name (a copy would lose the mode, the times, the owner, the links); not `-u`, `-b`, `--exchange` (#706) | start-up 1.01x (linux) |
| `cp` | done: bytes by `fs_copy_chunk`, a new file with its source's mode from the first instant, `-r`, `-L`, `-H`, `-P`, a link under `-r` copied as a link, `-p`, `--preserve=mode,timestamps`, `--no-preserve`, `-f`, `-i`, `-n`, `-v`, `-T`, `-t`, `--remove-destination`; not the owner (#701), `-a`, `-d`, `--preserve=links/xattr/context/all`, `-s`, `-l`, a fifo under `-r` (#705), `--sparse`/`--reflink` beyond `auto` (#703) | start-up 0.92x; 1 GiB 1.00x; `-r` of 100,000 files 0.72x to 0.75x (linux, btrfs; bu21's figures, not re-taken) |
| `chmod` | done: octal and symbolic modes, a mode given as an option, `-c`, `-f`, `-v`, `-R`, `-H`, `-L`, `-P`, `-h`, `--reference`, `--preserve-root` | not benched |
| `touch` | done: `-a`, `-m`, `--time`, `-c`, `-h`, `-r`, `-t`, `-d` for epoch, ISO, relative/calendar items, weekdays, English month names and slash dates, including `-r -d`, both times to the nanosecond; not `touch -` (#714), leap-second zones or unnamed grammar | not benched |
| `ln` | done: hard and symbolic, `-f` (a replace that never leaves the name missing), `-i`, `-n`, `-T`, `-t`, `-v`, `-P`, `-L`, `-r`, `-d`/`-F`; not `-b` | not benched |
| `kill` | done: `-s`, `--signal`, `-SIGNAL` by name or by this host's number, `-n`, signal 0, `-l`, `-t`/`-L` with the host's words, signal 0's included, exit statuses as signals, GNU's option rules; every signal the host numbers, real-time and host-only included; one process, a group (`-- -PGID`), this process's group (`0`) and every process (`-1`); not group 1 (`kill 0` from it) | not benched |
| `timeout` | done: `-f`/`--foreground`, `-k`/`--kill-after`, `-p`/`--preserve-status`, `-s`/`--signal`, `-v`/`--verbose`; 124/125/126/127/137 as GNU; timeout leads its own group and signals it at the expiry, then CONT, any signal (a fault's and a host signal's ignored in timeout first); signals sent to it passed on; a stopped command continued; ends by the signal its command died of; `the monitored command dumped core`; not passing on a fault or host signal sent to timeout itself | not benched |
| `id` | done: `-u`, `-g`, `-G`, `-n`, `-r`, `-z`, `-a`, the default line with `euid=`/`egid=`, USER operands by name or number; `-Z` refused as the oracle (no SELinux) refuses it; names from `/etc/passwd` and `/etc/group` only | not benched |
| `whoami` | done | not benched |
| `groups` | done: the process's groups and USERNAME operands | not benched |
| `logname` | done on linux: `/proc/self/loginuid`, then the utmp record of standard input's terminal; refused by name on macOS (no call for the kernel's login name) | not benched |
| `chown` | done: OWNER[:[GROUP]] by name or number, `USER:`, the old `.`, `--from`, `--reference`, `-c`, `-f`, `-v`, `-h`, `--dereference`, `-R` with `-H`/`-L`/`-P`, `--preserve-root` | not benched |
| `chgrp` | done: as `chown`, for the group | not benched |
| `mkfifo` | done: named pipes and `-m`; `-Z`/`--context` refused (no SELinux surface) | not benched |
| `link` | exactly two operands; source symlinks refused on macOS (no atomic-follow fs_link surface) | not benched |
| `unlink` | done: exactly one operand; directories never removed, links themselves removed | not benched |
| `truncate` | `-s` with suffixes and `+ - < > / %`, `-r`, `-c`; `-o` refused (#684), FIFOs refused (no non-blocking writable open), and `-c` races an unlinked operand (no non-creating writable open) | not benched |
| `sync` | readable operand files and directories, `-d` with the stronger full sync; bare `sync`, `-f`, and write-only operands refused by name (missing global/filesystem syncs and non-creating writable open) | not benched |
| `mktemp` | done: templates, `-d`, `-u`, `-q`, `-p`/`--tmpdir`, `-t`, explicit and inferred suffixes; kernel randomness and exclusive creation | not benched |
| `realpath` | done: `-E`, `-e`, `-m`, `-L`, `-P`, `-q`, `-s`, `-z`, `--relative-to`, `--relative-base` | not benched |
| `tty` | done: terminal name and `-s`; Linux `/proc/self/fd/0`, Darwin's immediate `/dev` character devices matched by identity | not benched |
| `base64` | done: streaming encode/decode, wrap, ignore-garbage and exact invalid-input prefixes | not benched |
| `base32` | done: streaming encode/decode, wrap, ignore-garbage and exact padding diagnostics | not benched |
| `comm` | done: columns, order checks, delimiters, NUL records, totals and alternating shared stdin | not benched |
| `join` | done: selected fields, unpaired rows, output lists/auto, separators, ignore-case, headers and order checks | not benched |
| `tsort` | done for DAGs and residual unions of simple cycles; complex cyclic components and cycles with outgoing tails refused | not benched |
| `shuf` | done: echo, full-u64 ranges, count, repeat, output and NUL records; random-source refused by name | not benched |
| `cksum` | POSIX CRC, crc32b, BSD/SysV, MD5, SHA-1/SHA-2 and BLAKE2b; `--base64`, `--raw`, tags, reverse form and verification modes; not SHA-3, SM3 or hardware `--debug`; UTF-8 names only | 0.05x to 0.94x (hasu) |
| `sum` | BSD and SysV, `-r` and `-s` | 0.14x to 0.94x (hasu) |
| `md5sum` | RFC 1321; binary/text markers, tags, NUL output, verification modes and escaped UTF-8 names | 0.32x (hasu) |
| `sha1sum` | FIPS 180-4 SHA-1; the checksum command modes, UTF-8 names | 0.29x (hasu) |
| `sha224sum` | FIPS 180-4 SHA-224; the checksum command modes, UTF-8 names | 0.34x (hasu) |
| `sha256sum` | FIPS 180-4 SHA-256; the checksum command modes, UTF-8 names | 0.35x (hasu) |
| `sha384sum` | FIPS 180-4 SHA-384; the checksum command modes, UTF-8 names | 0.40x (hasu) |
| `sha512sum` | FIPS 180-4 SHA-512; the checksum command modes, UTF-8 names | 0.40x (hasu) |
| `b2sum` | RFC 7693 BLAKE2b, variable digest lengths and the checksum command modes, UTF-8 names | 0.24x (hasu) |
| `split` | byte, line, bounded-record and numbered/round-robin partitions; suffix growth, filters and named GNU divergences below | not benched |
| `csplit` | numeric/BRE patterns, offsets and repetitions; suffix formats, counts, cleanup and empty suppression | not benched |
| `fmt` | paragraph/sentence reflow; width, goal, prefixes, split-only, tagged/crown margins and spacing | not benched |
| `pr` | fixed-mtime headers, pagination/form feeds, across/down/merged columns, numbering and tab/control formats | not benched |
| `ptx` | GNU-mode keyword contexts, selection/reference options, roff and TeX; traditional `-G` refused | not benched |
| `od` | character/integer and IEEE floating dumps, endian selection, offsets, strings and duplicate suppression | not benched |
| `expr` | complete token grammar, lazy Booleans and anchored BRE captures; integers beyond 64 magnitude bits refused (wolf-std#100) | not benched |
| `numfmt` | all unit families, field ranges, rounding, padding/formats, headers, invalid modes and NUL records; `--debug` refused | not benched |
| `factor` | every unsigned 64-bit input, sorted factors and exponents; larger integers refused (wolf-std#100) | not benched |
| `basenc` | eight encodings, decoding, garbage handling and wrapping; `--base58` refused | not benched |
| `uname` | raw Linux kernel fields via procfs, canonical field order; raw macOS fields refused (#907) | not benched |
| `df` | blocked by wolf-lang#686; compiler witness and proposed PAX row retained | — |
| `du` | allocation/apparent/inode traversal; named files0/time-format limits | not benched |
| `dd` | bounded block copies, conversions, EIO recovery and signal reports; named open limits | not benched |
| `install` | modes, owners, parents, compare and backups; strip/SELinux/debug refused | not benched |
| `mknod` | FIFO nodes; device nodes blocked by #705 | not benched |
| `shred` | exact-size overwrite through 25 passes; rounding/name-wipe/open limits | not benched |
| `dir` | shared ls engine, default -C -b | not benched |
| `vdir` | shared ls engine, default -l -b | not benched |
| `dircolors` | shell assignments and functional database; original database comments | not benched |
| `chroot` | not yet: central operation refuses, no os_chroot | not benched |
| `nice` | not yet: Linux reader and explicit -n 0; priority changes refuse | not benched |
| `nohup` | hangup ignored across exec; terminal streams and HOME fallback | not benched |
| `stdbuf` | not yet for arbitrary children; explicit environment-aware opt-in only | not benched |

| `date` | C-locale conversions, flags/widths, ISO/RFC output, file/reference inputs, calendar/weekday/relative grammar and named TZif/POSIX zones; named limits below | not benched |
| `test` | POSIX argument-count/precedence grammar, GNU predicates, arbitrary-size integer comparisons; kernel access with GNU-compatible differing-id behavior below | not benched |
| `[` | shared test grammar plus the required closing bracket | not benched |
| `hostname` | Linux nodename; setting and raw macOS fields refused | not benched |
| `hostid` | Linux persisted ID or files-first hosts IPv4 derivation; DNS-only lookup refused | not benched |
| `arch` | uname's machine field | not benched |
| `uptime` | Linux procfs load/uptime and utmp boot/count precedence | not benched |
| `users` | sorted Linux login names, duplicate sessions retained | not benched |
| `who` | Linux utmp record kinds, options, headers, idle/message status and terminal selection | not benched |
| `pinky` | Linux login summaries and /etc/passwd long output; DNS lookup refused | not benched |
| `pathchk` | portable character set, POSIX minimum limits, leading-hyphen rule and native read-only kernel checks | not benched |
| `stty` | exact supported termios setters and size reader; all missing settings refused by name | not benched |
| `chcon` | SELinux-disabled failure paths only; field-only GNU 9.4, not GNU 9.11 parity | not benched |
| `runcon` | current LSM label from procfs; context changes refused, status 125 on failure; never executes a command; field-only GNU 9.4 | not benched |

## Differences from GNU

Recorded, not matched: each is a place where boreutils answers otherwise
than GNU coreutils 9.11 and was ruled to stay that way, with the evidence
that measured it. The differences are explicit, including the safe refusal for csplit input
collisions below. Named-difference cases have independent witnesses; no
expected output is rewritten to silence an oracle disagreement. Other
refusals are identified in each utility's row above.

- **A streaming filter appended onto its own input** (boreutils#37,
  ruling #87). `tail -c +1 f >> f`, and `nl`, `cut`, `tr`, `fold`,
  `expand` and `head -c` the same way, read what they have just written:
  boreutils' write as they read, so each copies until the disk or a
  file-size limit stops it, at any size. GNU's stop after one pass on a
  file small enough to be read whole before the first write (a 9-byte
  file becomes 18 bytes, `nl`'s 33), and on a larger one — 5,714 bytes
  and up in the probe — fill the disk as boreutils' do. The difference is
  that small file's single pass, a buffer's size rather than a rule: GNU
  has no input-is-output check for these utilities (`cat` has one, and
  boreutils' `cat` refuses as GNU's does, bu25), and none is added here.
  `paste` parts the other way at 5,714 bytes (GNU's fills, boreutils'
  stops after one pass); `uniq`, `tac` and `cat -n` answer alike. Evidence:
  bu25's probe `notes/bu25/probes/p4.sh`, each run in a 16 MiB tmpfs in a
  throwaway container, GNU's `ev/probe-p4-gnu.log` (sha256 `f3a4f2aa…`)
  and boreutils' `ev/probe-p4-w1rel.log` (`2ec931a1…`), copied into
  `notes/bu28/ev/`, and boreutils' answered again at wolf 0.2.33
  (`notes/bu28/ev/probe-p4-head-release.log`).
- **One signal, not two** (bu28). GNU's `timeout` sends its command its
  own copy of a signal and then sends the group the command is in, so the
  command gets two; under load they now and then arrive apart, and a
  command that traps the signal runs its trap twice (measured: 2 of 360
  runs on one cpu). This one sends a command still in its group (read
  from `/proc/PID/stat` on linux) the signal once, by the group send, and
  only a command that left the group, or one whose group cannot be read
  (macOS), its own copy too.
- **`timeout -s 33`** (bu28). glibc keeps 32 and 33 for itself; GNU's
  timeout, sending either to the group it leads, dies of it. This one
  dies of 32 and lives through 33, on which its process holds a handler
  it never installed (`SigCgt`, measured): one `tests/timeout/` row.


### Date, access and terminal limits

`date` implements every documented C-locale conversion, case/padding flag,
field width and colonized zone form. The parser accepts the documented
ISO, slash/dot/calendar-month, RFC-style, pure-number, weekday and relative
items, `@seconds`, numeric zones, and an input `TZ="RULE"`. It refuses
unsupported grammar by name, including obsolescent ambiguous zone words.
`--debug`'s parser transcript is not yet implemented; `--set`, numeric
clock setting and `--resolution` lack clock surfaces. The live clock has
millisecond precision; fixed inputs and reference times retain nanoseconds.
Widths above 1,000,000, calendar years above 2,000,000,000 and epochs beyond
63,000,000,000,000,000 seconds are explicit implementation limits. Named
zones use the existing TZif/POSIX reader; leap-second `right/` tables are
refused, including a named table missing from the installed zone database.
Darwin's measured GNU9.11 default `%-N` uses six digits, unlike Linux's
nine, and its C-locale `%c`/`%Ec` zero-pad early years to four digits.
The formatter selects these measured host rules; all eight former field
skips are retired. Explicit `%N` widths and other flags remain unchanged.
GNU 9.11 accepts an unterminated date comment through end of input; this
matches the binary, despite the manual saying parentheses must balance.

`test -r/-w/-x` ask the kernel's `fs_access` when real and effective uid/gid
agree. Ordinary ACLs, read-only mounts, immutable files and root's execute
rule therefore use the kernel's answer. When ids differ, the predicates
use effective ids/groups and mode bits, matching the measured GNU 9.11
fallback. GNU itself has this set-id limitation: both
programs can reject an ACL-granted read or accept a read-only-mount write
that the actual open would refuse. The independent witnesses distinguish
these shared limits from ordinary parity; no GNU-vs-boreutils disagreement
is invented. The effective-access API request is
`notes/bu35-evidence/effective-access-issue.txt`; the real-id API already
exists at the pin (wolf-lang#820).

`stty` sets exactly `echo`, `icanon`, `isig`, `ixon`, `iexten`, `icrnl`,
`opost`, `istrip`, `min` and `time`, plus the `cbreak` alias. `size` reads
rows/columns; `-F` opens read-only and nonblocking without creating a file.
Full reports/snapshots (`-a`, `-g`, default and restore), other flags,
special-character setters, speeds, line discipline, rows/cols setters,
combinations such as `raw`/`sane`, and drain selection are refused by name.
The test names 148 unavailable settings/aliases, plus a saved restore form;
the exact list by termios field is `notes/bu35-evidence/termios-issue.txt`.
No unsupported flag is silently left unchanged.

`users`, `who`, `pinky` and `uptime` read the documented 384-byte Linux
x86-64 utmp ABI; other layouts are explicitly refused. An explicit FILE retains stale sessions; default `users`/`who`
and uptime counts omit positive pids absent from procfs. `pinky` keeps
those sessions, as GNU does. Other host layouts, raw non-UTF-8 record text,
DNS canonicalization and account services outside `/etc/passwd` are named
limits. `uname`/`hostname` read Linux raw fields from procfs; the raw-field
builtin remains missing on macOS (#907). `hostid` refuses DNS-only hosts
rather than substitute a hash or an invented zero.

## Drop-in readiness

Can a script call the boreutils program where it called GNU's? This
table answers it per utility, from the evidence and from nothing else.

- **GNU options** are the entries GNU 9.11's own `--help` lists (a short
  and long spelling of one option are one entry), counted as covered
  when a passing differential case exercises the option and this
  program does not refuse it. An option that appears only in a case
  where GNU refuses it too — `sort -ng` — is not counted as covered.
- **Cases** are Linux measurements: existing rows from kasumi, the small-file and checksum rows from hasu; passed / skipped, none failed.
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

| utility | GNU options | cases | vs GNU (kasumi unless stated) | verdict |
|---|---:|---:|---|---|
| `true` | 2 / 2 | 13 / 0 | start-up 0.71x | drop-in |
| `false` | 2 / 2 | 11 / 0 | start-up 0.72x | drop-in |
| `echo` | 5 / 5 | 45 / 0 | start-up 0.80x | drop-in |
| `basename` | 5 / 5 | 48 / 0 | start-up 0.80x | drop-in |
| `dirname` | 3 / 3 | 27 / 0 | start-up 0.80x | drop-in |
| `yes` | 2 / 2 | 18 / 0 | 0.63x | drop-in |
| `cat` | 12 / 12 | 119 / 0, and 104 / 0 in containers (`tools/inouttest`) | 0.27x to 0.97x | drop-in on linux, GNU's input-is-output refusal included (bu25); on macOS drop-in for scripts that avoid reading a READ-WRITE standard output's own file at or behind its offset (`cat f 1<> f`), which is refused there where GNU copies, because no call reads a descriptor's append flag (wolf-lang#722); on a linux with no `/proc` nothing is refused (#536) |
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
| `ls` | 51 / 60 | 734 / 14 (hasu bu36) | 0.60x to 1.99x; the long format 1.22x beside a GNU that also asks for each name's ACL | drop-in for scripts that avoid `-v`, quoting styles beyond `-N`/`-b`/`-Q`, `-Z`, the colour and filtering options (each refused by name), do not list files with ACLs in the long format (no `+`, wolf-lang#685), and do not need `.` and `..` placed by `-f` on ext4 (#692); owners named from `/etc/passwd` and `/etc/group` only; on a terminal, one 80 wide or reporting no size (#643) |
| `stat` | 7 / 8 | 152 / 8 | start-up 0.77x; 0.69x to 0.75x over many operands | drop-in for scripts that avoid `-f` (wolf-lang#686), `-` (#536), `%C`, and `%o` or the default format's `IO Block:` field, which prints `?` (#684) |
| `readlink` | 10 / 10 | 100 / 0 | start-up 0.77x | drop-in |
| `env` | 8 / 14 | 90 / 13 | `env true` 0.78x | drop-in for scripts that avoid `-S`, `-v` and the signal options (each refused by name), and do not read the ORDER of the environment they did not start from `-i` (wolf-lang#535) |
| `mkdir` | 7 / 7 | 262 / 0 | start-up 0.72x; a thousand deep 0.37x | drop-in |
| `rmdir` | 5 / 5 | 70 / 0 | start-up 0.72x | drop-in |
| `rm` | 11 / 12 | 218 / 3 | start-up 0.87x; `-r` 0.94x to 1.02x | drop-in for scripts that avoid `--no-preserve-root` (refused on purpose: this `rm` does not remove `/`) and `--preserve-root=all`; at a terminal, "write-protected" is the owner's write bit (#633); a tree deeper than the host's path limit is not removed (#707) |
| `mv` | 11 / 18 | 134 / 8 | start-up 1.01x | drop-in for scripts that stay on ONE file system (a move to another is refused, where GNU copies and removes) and avoid `-u`, `-b`, `-S`, `--exchange` and `--debug`, each refused by name; `-n` is a look and then a rename (#706) |
| `cp` | 19 / 36 | 228 / 19 | start-up 0.92x; 1 GiB 1.00x; `-r` 0.72x to 0.75x | drop-in for scripts that avoid `-a`, `-d`, `--preserve=links`/`xattr`/`context`/`all`, `-s`, `-l`, a special file met under `-r`, `--sparse`/`--reflink` beyond `auto`, `-u`, `-b`, `--parents`, `--attributes-only` and `-x`, each refused by name, and do not `-p` a file owned by someone else (the owner is refused by name, #701) |
| `chmod` | 14 / 14 | 532 / 0 | not benched | drop-in on linux; on macOS a link named by `-h`/`-P` or met by `-R` is left alone where GNU changes its own mode |
| `touch` | 11 / 11 | 181 / 4 (hasu bu36) | not benched | drop-in for scripts whose `-d` dates fit the [documented grammar](docs/touch-date-grammar.txt); `touch -` (#714), leap-second zones, noon and unknown date words remain named refusals |
| `ln` | 13 / 16 | 145 / 3 | not benched | drop-in for scripts that avoid `-b`/`--backup`/`-S` (refused by name) |
| `kill` | 5 / 5 | 894 / 1, and 365 / 0 that send | not benched | drop-in for scripts that do not `kill 0` from process group 1 (a container's first process and what it starts without job control; refused by name) |
| `timeout` | 7 / 7 | 116 / 0 (7 skipped on macOS), and 150 / 0 that run a command (13 skipped on kasumi, run on CI) | not benched | drop-in for scripts that do not send timeout itself a fault or host-only signal, nor `-s 33` its group (glibc's own: GNU's timeout dies of it, this one lives) |
| `id` | 7 / 8 | 64 / 0, and 428 / 0 as root and as users | not benched | drop-in where the accounts are in `/etc/passwd` and `/etc/group` (not macOS's directory service, LDAP or NIS); `-Z` is refused as GNU without SELinux refuses it |
| `whoami` | 0 / 0 | 10 / 0, and 19 / 0 | not benched | drop-in where the accounts are in `/etc/passwd` |
| `groups` | 0 / 0 | 12 / 0, and 62 / 0 | not benched | drop-in where the accounts are in `/etc/passwd` and `/etc/group` |
| `logname` | 0 / 0 | 11 / 0, and 46 / 0 | not benched | drop-in on linux; refused by name on macOS |
| `chown` | 13 / 13 | 17 / 0, and 373 / 0 as root and as users | not benched | drop-in where the accounts are in `/etc/passwd` and `/etc/group`; `-v` on a link to nothing it follows says `failed to change ownership of 'F' to …` where GNU prints an uninitialized owner |
| `chgrp` | 13 / 13 | 17 / 0, and 170 / 0 | not benched | as `chown` |
| `mkfifo` | 3 / 5 | 32 / 2 | not benched (hasu cases) | drop-in for scripts that avoid SELinux contexts (`-Z`/`--context` refused by name) |
| `link` | 2 / 2 | 17 / 0 on Linux; two source-symlink cases skipped on Darwin | not benched (hasu cases) | drop-in for scripts that avoid source symlinks on macOS; fs_link never follows them, unlike macOS link(1) |
| `unlink` | 2 / 2 | 16 / 0 | not benched (hasu cases) | drop-in |
| `truncate` | 5 / 6 | 92 / 4 | not benched (hasu cases) | drop-in for scripts that avoid `-o`/`--io-blocks` (#684), FIFOs, and `-c` where another process removes or replaces the operand during the stat/open window |
| `sync` | 3 / 4 | 15 / 4 | not benched (hasu cases) | drop-in for scripts that name readable operands and avoid `-f`/`--file-system`; write-only operands are refused by name |
| `mktemp` | 8 / 8 | 49 / 0 | not benched (hasu cases) | drop-in |
| `realpath` | 12 / 12 | 116 / 0 | not benched (hasu cases) | drop-in |
| `tty` | 3 / 3 | 12 / 0 | not benched (hasu cases) | drop-in |
| `base64` | 5 / 5 | 218 / 0 | not benched (hasu) | drop-in |
| `base32` | 5 / 5 | 218 / 0 | not benched (hasu) | drop-in |
| `comm` | 10 / 10 | 150 / 0 | not benched (hasu) | drop-in under LC_ALL=C |
| `join` | 15 / 15 | 233 / 0 | not benched (hasu) | drop-in under LC_ALL=C |
| `tsort` | 2 / 2 | 69 / 26 | not benched (hasu) | drop-in for DAGs and residual unions of simple cycles; complex cyclic components and cycles with outgoing tails refused by name |
| `shuf` | 8 / 9 | 97 / 1 | not benched (hasu) | drop-in for scripts that avoid --random-source, refused by name |
| `cksum` | 15 / 16 | 383 / 3 | 0.05x to 0.94x (hasu) | drop-in for UTF-8 file names and scripts that avoid `-a sha3`, `-a sm3` and hardware `--debug`, each refused by name |
| `sum` | 4 / 4 | 58 / 0 | 0.14x to 0.94x (hasu) | drop-in; command-line file names are UTF-8 |
| `md5sum` | 12 / 12 | 253 / 2 | 0.32x (hasu) | drop-in for UTF-8 file names; valid raw-byte name records refuse by name |
| `sha1sum` | 12 / 12 | 248 / 0 | 0.29x (hasu) | drop-in for UTF-8 file names |
| `sha224sum` | 12 / 12 | 248 / 0 | 0.34x (hasu) | drop-in for UTF-8 file names |
| `sha256sum` | 12 / 12 | 248 / 0 | 0.35x (hasu) | drop-in for UTF-8 file names |
| `sha384sum` | 12 / 12 | 248 / 0 | 0.40x (hasu) | drop-in for UTF-8 file names |
| `sha512sum` | 12 / 12 | 248 / 0 | 0.40x (hasu) | drop-in for UTF-8 file names |
| `b2sum` | 13 / 13 | 279 / 0 | 0.24x (hasu) | drop-in for UTF-8 file names |
| `du` | scoped above | 65 / 0 | not benched (hasu) | drop-in for scripts that avoid the named limits above |
| `dd` | scoped above | 71 / 8 | not benched (hasu) | drop-in for scripts that avoid the named limits above |
| `install` | scoped above | 33 / 4 | not benched (hasu) | drop-in for scripts that avoid the named limits above |
| `mknod` | scoped above | 12 / 3 | not benched (hasu) | drop-in for scripts that avoid the named limits above |
| `shred` | scoped above | 21 / 2 | not benched (hasu) | drop-in for scripts that avoid the named limits above |
| `dir` | scoped above | 18 / 0 | not benched (hasu) | drop-in for scripts that avoid the named limits above |
| `vdir` | scoped above | 18 / 0 | not benched (hasu) | drop-in for scripts that avoid the named limits above |
| `dircolors` | scoped above | 27 / 0 | not benched (hasu) | drop-in for scripts that avoid the named limits above |
| `chroot` | scoped above | 3 / 1 | not benched (hasu) | not yet |
| `nice` | scoped above | 9 / 1 | not benched (hasu) | not yet |
| `nohup` | scoped above | 12 / 0 | not benched (hasu) | drop-in |
| `stdbuf` | scoped above | 9 / 0 | not benched (hasu) | not yet |
| `split` | 15 / 15 | 196 / 3 | not benched (hasu) | documented correct behavior at the two named GNU defects below; other measured modes compare directly |
| `csplit` | 9 / 9 | 118 / 3 | not benched (hasu) | refuses input-inode collisions without losing data, unlike GNU; other measured modes compare directly |
| `fmt` | 9 / 9 | 329 / 0 | not benched (hasu) | drop-in under LC_ALL=C |
| `pr` | 26 / 26 | 144 / 0 | not benched (hasu) | drop-in under LC_ALL=C |
| `ptx` | 18 / 19 | 87 / 1 | not benched (hasu) | drop-in for GNU mode; `-G` refused by name |
| `od` | 21 / 21 | 150 / 0 | not benched (hasu) | drop-in on the measured native type layouts under LC_ALL=C |
| `expr` | 2 / 2, plus expression grammar | 433 / 1 | not benched (hasu) | drop-in for arithmetic operands/results through 64 magnitude bits; strings and comparisons are unrestricted, unsupported arithmetic is refused by name |
| `numfmt` | 17 / 18 | 209 / 1 | not benched (hasu) | drop-in under LC_ALL=C for scripts that avoid `--debug`, refused by name |
| `factor` | 3 / 3 | 59 / 1, including 10,000 random u64 values | not benched (hasu) | drop-in through 2^64−1; larger integers refused by name |
| `basenc` | 13 / 14, eight encodings | 404 / 1 | not benched (hasu) | drop-in for scripts that avoid `--base58`, refused by name |


| `date` | scoped above | 403 / 0 on Linux | not benched (hasu) | drop-in for the named C-locale grammar, formatting and zone scope above; clock setting/resolution and debug are refused |
| `test` | grammar and predicates | 1,490 / 0 | not benched (hasu) | drop-in; kernel access for equal ids and mode-bit fallback for differing ids both match GNU 9.11 |
| `[` | grammar and closing bracket | 1,490 / 0 | not benched (hasu) | drop-in; same measured access behavior as test |
| `uname` | all documented switches | 98 / 0 | not benched (hasu) | drop-in for Linux raw fields; macOS raw fields are refused (#907) |
| `hostname` | print only | 5 / 0 | not benched (hasu) | Linux print operation; setting and raw macOS name refused |
| `hostid` | scoped above | 6 / 0 | not benched (hasu) | Linux persisted ID or files-first hosts address; missing resolver refused |
| `arch` | common options | 5 / 0 | not benched (hasu) | drop-in |
| `uptime` | scoped above | 6 / 0 plus clock shape | not benched (hasu) | Linux procfs/utmp, with independent elapsed-time bounds |
| `users` | FILE and common options | 9 / 0 | not benched (hasu) | Linux utmp with UTF-8 text; default stale-pid filtering included |
| `who` | scoped above | 27 / 0 | not benched (hasu) | Linux utmp with UTF-8 text; --lookup needs a resolver |
| `pinky` | scoped above | 15 / 0 plus synthetic live sessions | not benched (hasu) | Linux utmp and /etc/passwd; --lookup needs a resolver |
| `pathchk` | -p, -P, --portability | 75 / 0 | not benched (hasu) | portable limits and measured native kernel checks; no pathconf builtin |
| `stty` | exact setters above | 29 / 0 plus full-state pty checks | not benched (hasu) | partial termios surface only; every other setting refused by name |
| `chcon` | SELinux-disabled paths | 9 field rows | not benched (hasu) | field-only GNU 9.4; no GNU 9.11 parity claim |
| `runcon` | current label / refused changes | 6 field rows | not benched (hasu) | field-only GNU 9.4, status 125; no GNU 9.11 parity claim |

**35 drop-in, 67 drop-in for scripts that avoid a named thing, 3 not yet, 2 SELinux-disabled field-only** (command rows, not the manual's grouped utility units; new checksum
rows explicitly require UTF-8 names). (bu28: `kill`'s two named things became one, and `timeout`'s four
became three narrower ones; bu27: `timeout` arrived with named things, and `kill`'s three
became two narrower ones; bu24: the six identity tools arrived with a named thing each —
accounts only in the two files, and `logname` on macOS; bu23: `kill` arrived with three named things, each a thing wolf
cannot express yet; bu22: `mkdir` became drop-in, and `chmod`, `touch` and `ln`
arrived with a named thing each; `rmdir` arrived drop-in at bu21 and
`mkdir`, `rm`, `mv` and `cp` with a named thing each; `readlink` arrived drop-in at bu20; `env`, the
one "not yet", shipped; `wc` became drop-in at bu19, when the host's
reason arrived). `cp`'s named things shrank at bu22: it copies a mode
and both times now, and refuses only what it cannot keep, by name. The same evidence read across: no shipped utility fails a case,
and every skip that is this program's own names its missing surface and
evidence, with an upstream issue where one is already filed.

**How much of GNU coreutils this is.** The full GNU coreutils 9.11 Linux
program set, including optional and SELinux commands, is **104 utility
units** when the four SHA-2 sums count as one and `[` folds into `test`.
boreutils has **107 command binaries, representing 103 of 104 units**;
**`df` is the exact remainder**, blocked on wolf-lang#686 (boreutils#52).
`chcon` and `runcon` are counted as reached only as the explicitly
SELinux-disabled, field-only paths described above, never as GNU 9.11
parity. A current label can still exist under AppArmor: runcon reads the
procfs bytes and appends one newline, preserving an existing newline; only
a failed read produces the current-context error. `chroot`, priority-changing `nice`, and arbitrary-child `stdbuf`
still lack their central operation; source coverage does not imply full
behavior coverage.

Erratum: the earlier 103-unit denominator was off by one; 107 source
binaries minus three SHA-2 duplicates and one bracket give 103 reached
units, and the missing `df` makes the denominator 104.

Existing issues carry witnesses; newly measured gaps below are listed for
upstream. The seek/standard-descriptor surfaces (wolf-lang#426/#424)
shipped in 0.2.22 and are used by `tail`, `head` and `wc`.

- **#346** (closed, wolf 0.2.28, s230): a mode at creation
  (`fs_open_perm`, `fs_create_dir_mode`) and a change of one
  (`fs_set_mode`); `chmod`, `mkdir -m`, `cp`'s new files and `cp -p`
  stand on them (bu22). `install -m`, `mkfifo -m`, `mktemp` can.
- **#633**, no user id and no `access`: `rm`'s and `mv`'s
  "write-protected" is the owner's write bit; `id`, `whoami`, `test -w`.
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
- **#423** and **#141** (closed, wolf 0.2.29, s232): every signal
  POSIX names has a meaning, a disposition can be read and set, and
  `os_signal_send`/`os_signal_number` reach any process and this
  host's numbering; `kill` stands on the last two (bu23). `tee -p`/`-i`
  here, `nohup` and `env --ignore-signal` can be written.
- **#739**, **#740**, **#741**, **#762** (closed, wolf 0.2.31, s241,
  ruling #79): the group send, every process, host signals by `-N`, a
  signal's words, the caller's own group. `kill`'s groups and `-t`'s
  words, and `timeout`, stand on them (bu27). Of what bu27 met, wolf
  0.2.33 (s246, wolf-lang#783, #784, #785, #787, ruling #88) answers
  four: one meaning ignored in the sending shape
  (`os_signal_ignore_one`), an end by a signal, a fault's included
  (`os_exit_signal`), a child's core (`os_wait_poll_core`) and signal
  0's words; `timeout` and `kill -t` stand on them (bu28). Still not:
  process group 1 (ruling #86: `kill 0` from it stays refused), hearing
  a send-only meaning or a host signal, and a process's own core limit
  or dumpability (`timeout`'s own end dumps where GNU's never does).
- **#424** (closed, wolf 0.2.22): `fs_fstat`, `fs_seek`, `fs_tell` and
  `fs_read_at` see descriptors 0, 1 and 2; `wc -c` and `tail` on a
  redirected regular file use them (bu15). `cat`'s input-is-output
  refusal waits on #536 and on a handle's open flags: GNU refuses only
  when the output was opened for append or stands past the input
  (bu22, boreutils#28).
- **#426** (wolf 0.2.22): seek, tell and the positional read exist;
  `tail`, `head` and `wc` use them (bu15). `tac` does not yet; `dd skip=`/`seek=` and `truncate` now use them; `shred` uses
  `fs_truncate` when removing a file.
- **#534** (closed, wolf 0.2.27): `os_exec` and `env_unset`; `env`
  runs its command by them (bu20). `nohup` now preserves ignored SIGHUP across exec. `nice`, `chroot`
  and arbitrary-child `stdbuf` still name their additional surface gaps.
- **#535**, the environment listed only sorted: `printenv` and `env`.
- **#536**, file identity: by PATH it is `fs_stat`'s device and inode
  since 0.2.27 (`ls -i`, `ls -RL`'s loops, `stat`); from an open HANDLE
  there is still none, so `cat f >> f` is not refused and `stat -`
  cannot be written.
- **#537**, `os_cpus` rounds a fractional quota down: `nproc`.
- **#538**, `wrapping[u64]` prints signed and cannot be divided
  natively: worked around in `src/bore/u64.lu`.
- **#625** and **#626** (answered by wolf 0.2.27's s218): `fs_stat`,
  `fs_lstat`, `fs_read_link`, `fs_read_dir_entries`. `ls -l` and its
  family, `stat` and `readlink` are written on them (bu20), and `ls -R`
  went from 0.27x to level with GNU. `realpath` now uses the walk too (bu30); `du` now walks those records; `test -h` and a `find`-shaped walk can too.
- **#684**, the record has no I/O block size: `stat`'s `%o` and
  `IO Block:`, and `shred`'s default block rounding.
- **#685**, no extended attribute: the `+` and `.` `ls -l` prints after
  a mode, `ls -Z`, `stat %C`; `getfacl`, `cp -a`'s attributes beyond.
- **#686**, no file-system record: `stat -f`, `df`.
- **#687**, a name that is not UTF-8 is listable and nothing else: `ls`
  reports and skips it, and so do `rm -r` and `cp -r` (bu21) — its
  directory then stays, and the status is 1. As an OPERAND it never
  arrives: the runtime aborts on the argument (#406).
- **#688** (closed, wolf 0.2.28): an `0o…` or `0b…` literal lowers on
  every tier; the modes here are still written in decimal.
- **#689** and **#682**, `os_exec` runs `./name` for an empty `PATH`
  component, and says nothing of why an exec failed: `env`.
- **#692**, the listing leaves out `.` and `..`: `ls -f` and `-aU`
  cannot place them where ext4 has them.
- **#698**, **#699** and **#700** (closed, wolf 0.2.28, s230):
  `fs_symlink`, `fs_link`, `fs_set_times`; `ln`, `touch`, `cp -p` and
  `cp`'s links stand on them (bu22). Setting times through a HANDLE is
  #714, which `touch -` waits on; a `mv` to another file system could
  now keep a mode and the times and does not yet.
- **#701**, no call changes an owner: `chown`, `chgrp`, `cp -p`'s
  owner (refused by name in that older pass). `install -o` now uses
  `fs_set_owner`, as the identity tools do.
- **#702** (closed, wolf 0.2.28): `fs_truncate` sets a handle's length;
  `truncate` is written on it (bu30), with `-o` still blocked by #684.
- **#703**, a hole can be written and not found, and a clone cannot be
  asked for: `cp --sparse` and `--reflink` beyond `auto`.
- **#704** (closed, wolf 0.2.28): `os_umask` sets the mask and answers
  the old one; reading it is setting it back (`bore.current_umask`),
  which `chmod`'s symbolic modes, `mkdir -p`'s parents and `-m` use.
- **#705**, device nodes still missing; `fs_mkfifo` arrived in 0.2.35
  and `mkfifo` is written on it. `mknod` and a special
  file under `cp -r`.
- **#706**, a rename always replaces: `mv -n` is a look and then a
  rename; `mv --exchange` cannot be written.
- **#707**, no call is relative to an open directory: `rm -r` and `cp
  -r` walk by path, so a tree deeper than the host's path limit is out
  of reach, and a directory swapped for a link mid-walk is followed.
- **#708**, the prelude's `min` is refused by every compiler tier, and
  W0304 forbids declaring one: written out where it is needed.
- **#709**, `fs_copy_chunk` costs eleven system calls around the one
  that copies a small file: `cp -r` at 0.72x to 0.75x.

Newly measured surface gaps (bu30, `notes/bu30/probes/surface.lu`):

- **Bare `sync` / `sync -f`** need global `sync(2)` and per-filesystem
  `syncfs(2)`. `fs_sync(fd)` and `fs_sync_dir(path)` flush only one object;
  both missing operations are refused by name, not approximated.
- **Raw `uname` fields** still need a builtin (#907): `os_name()` and
  `os_arch()` are normalized words, with no raw nodename/release/version.
  The shipped `uname` reads Linux's procfs fields; raw macOS fields remain
  refused by name. `hostname` uses the same Linux file, without a setter.
- **wolf-lang#684, a second consumer:** `truncate -o` needs `st_blksize`,
  not allocated space (`st_blocks`, record word 8). Neither path nor
  handle's 20-word stat record has it, so `-o` is refused by name.
- **Writable opens without create** are absent from modes 0–5 and from
  `fs_open_perm`. `truncate -c` can recreate a name removed after its
  stat; `sync` cannot safely retry a read-denied, write-only operand.
  The latter is refused by name, not opened with append/create. In
  `notes/bu30/probes/open-gap.lu`, stat + unlink + mode 2 prints
  `recreated=true`; mode 5 is read-only, and mode 6 is invalid.
- **Non-blocking writable opens** are absent too. GNU refuses a FIFO
  without a reader immediately; mode 2 would block. `truncate` refuses
  an observed FIFO by name before opening it, but a concurrent replacement
  after stat remains a race until the surface exists. The bounded
  witnesses are `notes/bu30/probes/review-oracle.py` and the FIFO cases.
- **`unlink` needs no further surface:** the empty-directory witness
  gets the host refusal from `fs_remove` (`Is a directory` on Linux,
  `Operation not permitted` on macOS), and the entry remains. The
  utility also checks `lstat`; its final removal is still file-only.

- **Following a hard-link source on macOS** needs an atomic follow option
  for `fs_link`. The pinned call never follows a final symlink on any
  host; GNU's macOS `link` does. Source symlinks are refused by name on
  macOS, not linked to the wrong inode or reported as a fabricated ENOENT.
  The host-scoped witnesses are the two link cases and
  `notes/bu30/ev/ci-macos-red.log` (run 39987951234).

### Named GNU 9.11 splitter divergences

These are explicit divergences, not changed differential expectations.
`tools/splittertest` checks the documented behavior independently.

| Case | GNU 9.11 witness | boreutils behavior |
|---|---|---|
| `split --hex-suffixes=f` | `printf 'one\ntwo\nthree\nfour\nfive\n' \| split --hex-suffixes=f -l1 - hex.` exits 0 but drops `one` and creates `hex.0f`, `hex.0i`, `hex.0x`, `hex.0 ` | Preserve every record; sequential hexadecimal suffixes `0f`, `10`, `11`, `12`, `13` |
| `split -e -n l/N` with more chunks than input bytes | `printf 'a\nb\n' \| timeout 3 split -e -n l/5 - hang.` writes two files and hangs (timeout exits 124); `l/10` also hangs | Finish with two nonempty files preserving all input bytes |
| `csplit` output aliases its input | `printf '1\n2\n3\n' > xx00; csplit xx00 2` prints `0`, exits 1 with a line-number error, and deletes `xx00`; with input `f` hard-linked to `xx00`, `f` is left empty | Exit 1 with `csplit: 'xx00' would overwrite input; aborting`; preserve the original inode's bytes, including hard links, symlinks and input descriptor 0 |


The documented split interface promises hexadecimal suffixes and says `-e`
does not generate empty output files with `-n`; csplit promises pieces of
the original input, not truncation and deletion of that input. The isolated witnesses ran in an Ubuntu
24.04 container on hasu, using the digest-built GNU 9.11 oracle. Evidence:
`/home/mfwolffe/lanes/bu33/ev/split-oracle-anomalies.log` and
`/home/mfwolffe/lanes/bu33/ev/split-input-collision.log`.
These preserve the documented behavior and publish GNU's disagreement,
rather than reproduce data loss or a hang.

The C-locale BRE engine in `src/re/` is vendored from the org's own
clean-room [scent](https://github.com/wolffe-lang/scent) at
`b6f63a4892cca631475cd0b87a0b648ce9b532a9`, under GPL-3.0-or-later with
the wolf Training Data Permission. It substitutes for the pinned std's
missing regex module ([wolf-std#99](https://github.com/wolffe-lang/wolf-std/issues/99));
no GNU implementation source was consulted.

### Numeric range witnesses

The missing general bigint surface is
[wolf-std#100](https://github.com/wolffe-lang/wolf-std/issues/100).
`expr 18446744073709551615 + 1` prints `18446744073709551616` in GNU
9.11; boreutils refuses the overflowing result with status 2 and names
the 64-bit magnitude limit and that issue. `factor -h
18446744073709551616` prints `18446744073709551616: 2^64` in GNU;
boreutils refuses it with status 1 and the same issue. Values through
`18446744073709551615` remain supported, including unsigned division and
primality controls near that endpoint. `tools/numbertest`, included in
`tools/texttest`, checks both the refusals and the supported side of the
boundary.

### Inherited Darwin qualification

Attribution run40165219687 compared trunk37e3825 and the identity-tool
head under fresh trunk/head GNU9.11 configurations and the active stage.
All six cells reproduce the same30 inherited failures: dir/vdir owner
names(11), numfmt print/range boundaries(7), od negative-NaN text(12).
Only those exact rows are loud Darwin skips; every other row stays live.
No inherited implementation or expected output was changed. The cells,
complete differences and issue drafts are in `tests/gaps/bu35/darwin-*.txt`.
Host GNU9.12 was not selected as the oracle. The extra install-program
flags and the identity pass's shared code do not move these verdicts.

The bu36 option checkpoint measures `ls` on hasu block B in Ubuntu 24.04, GNU 9.11: **734 passed / 0 failed / 14 named skips**, on both native tiers. It adds 38 cases and retires four option skips; account lookup, ACLs, directory order, devices and terminal-width qualifications remain. Numeric explicit block sizes and unit suffixes are supported; display-size environment variables are still not read.
