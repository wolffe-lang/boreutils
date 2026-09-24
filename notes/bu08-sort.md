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
