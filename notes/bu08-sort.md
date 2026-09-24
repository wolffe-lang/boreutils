# bu08 — sort (B5), and the optional argument

Lane note. §2 and §3 were written 2026-09-24, before a line of `src/`
moved and before `sort` or GNU `sort` was timed or measured for memory
on any host.

## 2. Inputs, re-derived against origin (2026-09-24)

| the contract says | origin says | verdict |
|---|---|---|
| boreutils trunk `eac2a32` (bu07) | `eac2a3221dd83e2481c5d56be5c14144962c272d`, "notes: cite the in-branch green, since the amend orphaned the sha it named" | holds |
| pins wolf 0.2.16 / lupin 0.1.38 / std `070884c` | `wolf-toolchain.toml`: `version = "0.2.16"`, `version = "0.1.38"`, `rev = "070884c6e1e3…"`; `tools/fetch-toolchain` on kasumi re-checked both archive digests (`84e30c05…`, `828b5c55…`) and `wolf --version` answers `wolf 0.2.16 (wolfgang, pin 93a5fe5)` | holds |
| corpus 1,772 cases | `grep -c '^\[\[case\]\]' tests/cases/*.toml` sums to **1,772** | holds |
| 1,752 / 0 / 20 on kasumi | `tools/build` then `tools/difftest` at `eac2a32`, kasumi: `difftest: 1752 passed, 0 failed, 20 skipped` (log `~/lanes/bu08/base-difftest.log`) | holds |
| `bore.Sink` (B152) is the writer | `src/bore/sink.lu`, `sink` / `sink_push` / `sink_done`, sink last (wolf-lang#449) | holds |
| `[oracle.env]` / `[oracle.probe]` in `gnu-oracle.toml` | `LC_ALL = "C"`, `_POSIX2_VERSION = "200112"`; probe `uniq +1 /dev/null` → 1 | holds |
| the field leg's B98 ruling | `ci.yml` `field:` has step-level `continue-on-error` on the differential step only, then `tools/field-verdict` | holds |
| no seek/tell (wolf-lang#426) | OPEN | holds |
| no `strerror` (wolf-lang#407) | OPEN | holds |
| `print` write errors (wolf-lang#408) | OPEN | holds |
| boreutils#8: `tail --follow[=WORD]` rewritten by hand | OPEN; `src/tail.lu` `rewrite_follow`, applied to every argv word before `bore.parse` | holds |

### Drift, reported

1. **wolf-lang#449 is CLOSED upstream**, but its fix is not in the
   pinned 0.2.16, so the twelve workaround sites stay (the contract
   forbids reverting them) and every new call site in this lane takes
   the same shape: the `mut` writer or sink LAST.
2. **The GNU oracle has its own temporary-file surface, and the
   harness gives it none.** `tools/difftest` builds each case's
   environment from PATH plus `[oracle.env]`, so `TMPDIR` is unset on
   both sides and both fall back to `/tmp`. A case that needs a temp
   directory must name it (`-T`).
3. **`sort`'s usage status is 2, not 1**, which the guide's "usage
   errors exit 1 in the coreutils family" line does not cover — but an
   `argmatch` refusal (`--check=bogus`, `--sort=bogus`) is **1**.
   Measured on kasumi, GNU 9.11: `sort -o` → 2, `sort --check=bogus` → 1.

## 3. Prediction, committed before the first feature

### 3a. boreutils#8

`bore.optional(short, long)` retires **one** hand-rewrite: `tail`'s
`rewrite_follow`, which is applied at one `bore.parse` call site (two
loops feed it). No other existing utility declares an option GNU gives
an optional argument. `sort` becomes the second user
(`--check[=diagnose-first|quiet|silent]`). **Falsifier:** a second
existing site found that needs it, or `tail` still rewriting argv.

The red: the new `tail` cases below fail at trunk (a word after
`--follow=` is swallowed, so `--follow=bogus FILE` follows a regular
file until the case times out, and `--follow=name` on standard input
is not refused), and `src/bore_test.lu` does not compile.

### 3b. `sort`: cases

**170–230 differential cases.** `tac` has 102 for three options; `sort`
has seven named by the contract plus the modes (`-c`/`-C`/`-m`/`-o`),
`-s`, `-z`, `-d`, `-i`, `-S`/`-T` and the key grammar's refusals.

### 3c. `sort`: speed, predicted from the ORACLE'S BUILD

What the oracle is, from its documentation and `--help`, not from a
timing: GNU 9.11 `sort` sorts **in parallel on min(nproc, 8) threads**
(info manual, `--parallel`), so on kasumi (16 cores) it uses **8**;
it sizes its buffer from the input for a regular file, so 10 MB and
100 MB sort in memory; it merges at most 16 inputs at once. In the C
locale its comparison is `memcmp` of the line.

boreutils' `sort` is **one thread** (the lane does not take on
`scope`/`spawn` for this), holds the input in one `List[byte]` read in
256 KiB chunks, sorts an index with a merge sort (stable by
construction), and compares bytes in a wolf loop with bounds checks —
no `memcmp` surface.

| row | predicted ratio (GNU time / ours) | why |
|---|---|---|
| start-up, empty input | 0.8–1.2x | both are process start and a read of nothing |
| 10 MB, whole line, file | **0.10–0.30x** | 8 threads against 1, and a byte loop against `memcmp` |
| 100 MB, whole line, file | **0.06–0.20x** | GNU's thread advantage grows with the input; ours is O(n log n) on one core |
| 100 MB through a pipe | 0.06–0.20x | GNU cannot size its buffer from a pipe, but still sorts in memory at 100 MB |
| `-n`, 10 MB | 0.15–0.40x | GNU's numeric compare is a scan too, so the per-compare gap narrows |
| `-t -k` key, 10 MB | 0.10–0.35x | both re-find the key; GNU caches the first key's bounds |
| `--parallel=1`, 10 MB | **0.30–0.70x** | the fair row: one thread each, `memcmp` against a loop |
| external merge (`-S` small on both sides), 100 MB | 0.10–0.30x | both write runs to `$TMPDIR`; GNU's runs are compressed by nothing and sorted in parallel |

**Falsifier:** any measured ratio outside its band. On bu07's record
(one of five bands right) I expect at least two to miss, and the one I
am least sure of is the external row: our runs are sorted on one
thread but GNU's merge is single-threaded too.

### 3d. `sort`: peak memory, per input size

Ours holds the whole input in memory up to a **run budget**, sorts it,
and past the budget writes sorted runs to temp files and merges them.
The default budget is **256 MiB of input**; `-S SIZE` sets it (a floor
of 64 KiB). A `List` grows by doubling and an arena frees nothing
(wolf-std F-0011), so the held input costs about twice itself; each
run is built in a region that dies after the run is written.

| input | ours, predicted | GNU, predicted |
|---|---|---|
| 10 MB | 25–45 MB (2.5–4.5x the input) | 12–25 MB |
| 100 MB | 250–450 MB | 110–220 MB |
| 100 MB with `-S 10M` (external) | **30–60 MB**, flat in the input | 15–40 MB |

**Falsifier:** a measurement outside the band, or the external row
growing with the input (that would mean a run's region is not dying).

### 3e. The external merge, and how it is shown

A run is written to `$TMPDIR` (or `-T DIR`, or `/tmp`) as
`sortXXXXXX`, created with mode 4 (create-new), read back
sequentially, and removed. No seek is needed (wolf-lang#426 does not
bound it). Evidence is **counted**, not asserted: the number of temp
files created under a traced run (`strace -f -e trace=openat`) at a
stated `-S` and input size, for ours and for GNU, plus differential
cases in which `-T` names a directory that does not exist, so both
sides must fail with `cannot create temporary file in '…'` — which a
program that never touched a temp file cannot print.

## What the lane did, in the order it happened

### 1. boreutils#8 — the optional argument

`bore.optional(short, long)` is getopt_long's third state: a word only
when it is ATTACHED (`--follow=name`, `-yr`), never the next word.
`Parsed.given` says whether one was attached, which is how `--follow=`
(an empty word) differs from `--follow`. `bore.argmatch` matches the
word as GNU's argmatch does (exact, or a prefix of choices that all mean
one thing; the empty word is ambiguous) and `bore.argmatch_error` prints
GNU's three-part refusal (`invalid argument` / `Valid arguments are:` /
`Try`), status 1.

`tail`'s hand rewrite (`rewrite_follow`) is gone; `--follow` is
`bore.optional("", "follow")` and `-f` its own short flag. Eighteen new
`tail` cases, and the ones that terminate only because GNU refuses were
the red: `--follow=bogus FILE` followed a regular file until the case's
timeout, and `--follow=name` on standard input was not refused.

| | commit | evidence |
|---|---|---|
| red | `757fd83` | kasumi: `difftest: 117 passed, 12 failed, 2 skipped` over `tail` (`~/lanes/bu08/red-8-tail.log`); CI run **36029702653**: both gauntlet legs fail at `wolf test` (`error[E0301]: module 'bore' has no item named 'optional'`), and the field leg, which runs the differential without `wolf test`, lists the same 12 `FAIL tail:` lines |
| green | `aa6e7f1`, `132c09b` | kasumi `129 passed, 0 failed, 2 skipped`; CI run **36029854007**, all three legs `success` |

**§3a scored: right, and one more than predicted.** One hand rewrite
retired (`tail`), and `sort --check[=WORD]` is the second user — both as
predicted. The third was not predicted: `sort`'s obsolete `-y` takes an
OPTIONAL attached word (measured: `sort -yr` does not reverse, `sort -y
-r` does), so `bore.optional("y", "")` is the only spelling that
matches GNU, and the differential found it (`y takes an attached word`).

### 2. `sort`, one option group at a time, each red first

Seven pairs of commits. The cases of each group were committed and
pushed first and went red on CI against the previous stage's program;
the feature commit after it went green. The numbers are the ubuntu
gauntlet's `difftest` line (macOS runs the same corpus; its legs were
queued behind the org's runner limit — see the PR for the head's).

| group | red commit, run, ubuntu `difftest` | green commit, run, ubuntu `difftest` |
|---|---|---|
| whole lines (and the skeleton `ea0b0ba`, run 36032980197 green, which wrote its input unsorted) | `6d178f5`, **36034112311**: 1801 passed, **24 failed** | `4867b77`, **36034899437**: 1825 passed, 0 failed |
| `-r -u -s` | `b34dc5f`, **36035752586**: 1828 passed, **17 failed** | `926f292`, **36035806544**: 1845 passed, 0 failed |
| `-n -h -M --sort` | `b55c8e3`, **36035853682**: 1850 passed, **37 failed** | `0e59430`, **36035904696**: 1887 passed, 0 failed |
| `-f -d -i -b` | `97d8ffe`, **36035959850**: 1891 passed, **27 failed** | `dce17c1`, **36036013701**: 1918 passed, 0 failed |
| `-t -k` | `c9b98b5`, **36036066951**: 1936 passed, **49 failed** | `085327f`, **36036116698**: 1985 passed, 0 failed |
| `-c -C -m -o -z` | `5481507`, **36036170135**: 2003 passed, **49 failed** | `d4da50a`, **36036221342**: 2052 passed, 0 failed |
| the external merge | `2505c6f`, **36036274940**: 2081 passed, **13 failed** | `f37435c`, **36036323186**: 2094 passed, 0 failed |

Every red run failed at the step `the differential suite against the
oracle of record` (checked per job). The same seven reds and greens were
measured on kasumi before the push, with the same counts
(`~/lanes/bu08/stages/{own,next}.v*.log`).

The external merge's red is the honest shape of that feature: an
in-memory sort produces the same BYTES as a merge of runs, so the red
cases are the ones only a spill can fail — `-T` naming a directory that
does not exist under `-S 64K` (both sides must print `cannot create
temporary file in '/nonexistent/dir'`) — and the `-S`, `--batch-size`
and `--parallel` refusals.

### 3. The external merge, seen

Traced on kasumi, 100 MB of generated text at `-S 10M -T DIR`
(`~/lanes/bu08/strace-{ours,gnu}.txt`):

| | temp files created (`O_CREAT\|O_EXCL`) | unlinked | left in DIR after |
|---|---:|---:|---:|
| boreutils | **11** | 11 | 0 |
| GNU 9.11 | 32 | 32 | 0 |

```
openat(AT_FDCWD, "tmpo/sortt4v3wu", O_RDWR|O_CREAT|O_EXCL|O_CLOEXEC, 0666) = 5   (ours)
openat(AT_FDCWD, "tmpg/sortK1qgd5", O_RDWR|O_CREAT|O_EXCL|O_CLOEXEC, 0600) = 4   (GNU)
```

The two differ in the mode, and that is a finding, not a style: wolf
has no surface to create a file with a mode, so a run is `0666` less the
umask where GNU's is `0600`. Commented on **wolf-lang#346** (comment
5819424810) as a second consumer; stated in `src/sort.lu`'s header.

Multi-level merges are covered by cases (`--batch-size=2`, and 24 × 90
KB at `-S 64K`, more runs than one batch of 16), and the 1 GB rows
below merged ~100 runs in two levels.

### 4. Speed, scored (kasumi, load 2–3, 5 runs, head `0c7ebfe`'s code)

| row | predicted | measured | verdict |
|---|---|---:|---|
| start-up | 0.8–1.2x | 0.8 ms vs 0.4 ms (0.5x; under the tool's 1 ms floor) | wrong, below |
| whole lines, 10 MB | 0.10–0.30x | 0.30x | right (at the edge) |
| whole lines, 100 MB | 0.06–0.20x | 0.22x | wrong, above |
| through a pipe, 100 MB | 0.06–0.20x | 0.22x | wrong, above |
| `-n`, 10 MB | 0.15–0.40x | 0.30x | right |
| `-t -k`, 10 MB | 0.10–0.35x | 0.14x | right |
| `--parallel=1`, 10 MB | 0.30–0.70x | 0.44x | right |
| external, 100 MB | 0.10–0.30x | 0.45x | wrong, above |

**Four of eight.** The reason the three large rows are above their
bands is one fact the prediction did not have: GNU's eight threads buy
it less than 2x (640 ms at `--parallel=1` against 333 ms), so the gap is
mostly `memcmp` against a checked loop, not threads. And our external
merge beats our own in-memory sort (1.37 s against 1.53 s at 100 MB),
because ten 10 MB runs sort in cache where one 100 MB index does not.
The first bench run, at load 4–5 before the memory fix, gave the same
ratios to within 0.03 (`~/lanes/bu08/bench-0.1.md`).

### 5. Memory, scored (peak RSS, `/usr/bin/time`)

| input | ours predicted | ours measured | GNU predicted | GNU measured |
|---|---|---:|---|---:|
| 10 MB | 25–45 MB | 39 MB, right | 12–25 MB | 22 MB, right |
| 100 MB | 250–450 MB | 322 MB, right | 110–220 MB | **304 MB, wrong** |
| 100 MB, `-S 10M` | 30–60 MB | 41 MB, right | 15–40 MB | **12 MB, wrong** |
| 1 GB, `-S 10M` | flat | 42 MB, flat | — | 12 MB |
| 1 GB, default budget | — | 808 MB | — | 3,005 MB |

**The falsifier fired first, and it was right.** The first measurement
of 1 GB at `-S 10M` was **61 MB against 41 MB for 100 MB** — the
external row growing with the input, which §3d named as the sign of a
defect. Two were found: a run read past its budget (a list that crosses
a power of two doubles; at the default budget that took 1 GB to
**1,060 MB**), and each merge batch's readers stayed in the ambient
region. Commit `0c7ebfe` bounds every read by what the budget has left
and gives each batch a region: 42 MB for 1 GB, 808 MB at the default.

## Corrections

- **README's corpus sentence was wrong at `eac2a32`**: it said 1,753
  passed and 19 skipped; kasumi answered 1,752 and 20, which is also
  what this contract's §2 said. Corrected from this lane's run.
- **Four commits of this lane were pushed with the wrong messages and
  replaced** (`0a68510`, `0f72f81`, `242c73b`, `533cc06`): a zsh array
  is 1-indexed, so each commit took the previous stage's message and one
  stage's content was folded into the next. The branch was reset to the
  skeleton and force-pushed with a lease, the stages rebuilt one commit
  each, and the four orphaned runs cancelled (36033115707, 36033164889,
  36033216465, 36033268587). None of those shas is cited as evidence.
- **§3b was wrong**: 324 `sort` cases against a band of 170–230.
- **§3d's GNU memory was wrong in both directions** (above), because
  GNU sizes its buffer from the input and holds a 100 MB file whole.
