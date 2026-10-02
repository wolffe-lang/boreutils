# bu14 — the small-surface set, and the drop-in readiness table

Lane note and contract. **Class:** feature (boreutils), **Opus**. **Wave:**
53, subwave 53c. One oracle: the differential against GNU coreutils 9.11
under `[oracle.env]` (B44, B73), through `tools/difftest`. One
deliverable: the small-surface utilities `tee`, `printf`, `env`,
`printenv`, `pwd`, `sleep` and `nproc`, each written from the allowed
sources, differential-tested, benched on kasumi and added to the README
— minus any whose OS surface wolf 0.2.20 lacks, filed upstream with a
witness — and a **drop-in readiness table** in the README for every
utility. Templates: bu08 (a utility lane, `notes/bu08-sort.md`) and bu13
(the contract shape, `notes/bu13-the-pair-at-0.2.20.md`).

§1, §2 and §3 were written 2026-10-02, after the base was measured and
the GNU binaries were run black-box, and before a line of any new
utility was written or any bench was run.

## 1. Forbidden, absolutely

- **Never read, copy or translate GNU coreutils source** (the licence
  rule). Each utility is written from POSIX.1-2024, GNU's `--help`, the
  info manual's option descriptions (`info '(coreutils) X invocation'`
  on kasumi) and black-box runs of the GNU 9.11 binary; uutils (MIT)
  and toybox (0BSD) as design references only. GNU's `--help` prose is
  not copied: `--help` and `--version` take GNU's shape in our words and
  their cases compare the exit status only.
- No `rm` outside `~/lanes/bu14/` and `/tmp/bu14p/` on kasumi and
  `/private/tmp/bu14` plus this session's scratchpad here; no deletion
  in any tree this lane did not create; never another lane's target
  dir. kasumi `/home` is shared by four lanes: trees are pruned as
  their evidence is written.
- No `git add -A`; no edit to another lane's file; no `~/.claude`.
- No build on this Mac. Every build, difftest and bench is on kasumi,
  `CARGO_BUILD_JOBS=4`, launched with `setsid`, waited on in a printing
  loop. GNU binaries MAY be run black-box here (Homebrew's `g`-prefixed
  9.11), which is how the macOS column of a probe is read.
- No merge, no rebase-merge; no `2>/dev/null` on a checkout.
- No "seen red" or "seen passing" without a run id, sha, log path or
  digest in the same paragraph.
- The pin does not move: wolf 0.2.20 / lupin 0.1.43 / std `14f0ab2`.
- Kill only this lane's own pids, never a pattern or a process group.
  (A black-box probe of GNU `sleep` with `0xAd`, `0x1p0d`, `1e999999`,
  `infinity` and `INF` operands slept for real; each was killed by its
  own pid, 561122, 575158, 575239, 578224, 578389, all children of this
  lane's ssh session 561091. Every later probe runs under `timeout`.)
- No commit or PR trailers of any kind.
- No silent workaround: a gap is filed upstream with a witness and
  named where a reader meets it; a behaviour this program cannot match
  is a stated skip in the case file or a refusal by name, never an
  imitation that happens to pass.
- No "drop-in" claim in the readiness table that the cases do not back.

## 2. Inputs, re-derived against origin (2026-10-02)

| the contract says | origin says | verdict |
|---|---|---|
| boreutils trunk `7c3e2da` | `7c3e2daa385e96c3a1ea628144498c8e3c413057`, "notes: bu13 evidence …"; PR #17 MERGED; worktree `/private/tmp/bu14` on branch `bu14` at it | holds |
| pins wolf 0.2.20 / lupin 0.1.43 | `wolf-toolchain.toml`: `wolf 0.2.20 (wolfgang, pin cdde128)`, lupin `0.1.43`, std `14f0ab2c`; kasumi `tools/fetch-toolchain` re-checked `sha256 24855d5e… OK` (`~/lanes/bu14/base-build.log`) | holds |
| "all 2,094+ existing cases still pass" | kasumi, trunk `7c3e2da`: `tools/build && tools/check-test && tools/check-fmt` → `BUILD_EXIT=0`, `wolf test: 1 passed`; `tools/difftest` → **`difftest: 2094 passed, 0 failed, 20 skipped`**, oracle asserted (9.11, `LC_ALL=C _POSIX2_VERSION=200112`, the `uniq +1` probe OK). Sorted verdict list 2,114 lines, sha256 `b97c0e91b8d203737eb42c10234517f2ffbcdb7e6d0ba1b70e185b8a3dfc5817` — bu13's, bu11's, bu10's and bu09's digest (`~/lanes/bu14/base-difftest.log`, `base-verdicts.txt`) | holds |
| "the existing 22" utilities | `src/*.lu` minus `bore_test.lu`: **21** — `true false echo basename dirname yes cat wc head tail cut tr uniq seq nl tac paste fold expand unexpand sort`; bu13's evidence says "all 21 utilities" | **drift: 21, not 22** |
| the upstream issues #405, #407, #411, #416, #417, #423, #424, #426, #346 | all nine OPEN (`gh issue view`, 2026-10-02), titles as the README names them | holds |
| the oracle on kasumi | `coreutils 9.11-2` (Arch), `tee (GNU coreutils) 9.11`; on this Mac Homebrew's `gprintf (GNU coreutils) 9.11` | holds |
| "how many of GNU coreutils' utilities exist at all" | the 9.11 info manual on kasumi has **103** `X invocation` nodes for utilities (105 nodes, minus "Modified command" and "Multi-call"; the four SHA-2 sums share one node and `[` is `test`'s); Arch's build installs **102** binaries in `/usr/bin` (`pacman -Ql coreutils`), which omits `arch`, `chcon`, `runcon`, `hostname`, `kill`, `uptime` and adds `[`, `dir`/`vdir` and the four SHA-2 names | measured; the README states which count it uses |

### What each new utility needs from wolf, measured

The host builtin table at `v0.2.20` (`spec/11-os.md` §7, `[os.host.sigs]`)
is the whole OS surface; `crates/wolf_rt/src/os.rs` at `v0.2.20` is how
the native tier answers it. Four witnesses were built on kasumi from the
staged 0.2.20 archive (`~/lanes/bu14/wit/*/main.lu`, run log
`~/lanes/bu14/wit/witness.txt`):

| utility | needs | wolf 0.2.20 has | verdict |
|---|---|---|---|
| `sleep` | a sub-second sleep | `time_sleep_ms(int)` | fits; milliseconds are the resolution (GNU's is nanoseconds), stated |
| `nproc` | the schedulable count; the installed count; `OMP_*` | `os_cpus()` (Rust's `available_parallelism`), `env_get`, `fs_read_dir` | fits, with one measured divergence: under a FRACTIONAL cgroup quota `os_cpus` floors where GNU rounds up — `systemd-run --user --scope -p CPUQuota=150%`: wolf **1**, GNU **2**; at 250%: wolf **2**, GNU **3**. Affinity agrees (`taskset -c 0-2`: 3 and 3) |
| `pwd` | the physical directory; whether `$PWD` names it (`-L`) | `os_cwd()`; `fs_fstat` answers `[kind, size, mtime]` only — no device or inode | fits for `-P` (GNU's default); `-L` can only compare `[kind, size, mtime]` and the listing, which is a heuristic, not identity. To be filed |
| `printenv` | one variable; the whole environment IN ITS ORDER | `env_get`; `env_vars()` is **sorted** (`os.rs`: "`K=V` lines, SORTED (determinism over environ order)") | named variables fit; the bare listing cannot keep environ's order — `env -i B=1 A=2`: wolf `A=2 B=1`, GNU `printenv` `B=1 A=2`. To be filed |
| `tee` | stdin bytes; files in write and append modes; `-i` ignores SIGINT; `-p` and `--output-error` ignore SIGPIPE and see EPIPE | `/dev/stdin` reopen (#405), `fs_open_mode` modes 1 and 2; the signal set is RELOAD/TERMINATE/QUIT/UPGRADE only (#423) | fits except `-i` (no INT meaning) and every pipe branch of `-p`/`--output-error` (#423) |
| `printf` | nothing from the OS: formatting, 64-bit integers, `long double` | `int`, `wrapping[u64]`, `List` | fits; GNU's floating conversions go through the HOST's `long double` (x86-64: 64-bit mantissa; macOS arm64: 53), so they are emulated exactly in big integers |
| `env` | run COMMAND in a modified environment: exec, unset, clear, chdir, argv0, signal dispositions, the child's exit status or signal | `os_spawn` wires the child's stdin to the null device (`[os.proc.spawn]`); no exec, no unset, no clear, no chdir, no argv0; `os_wait` answers a signal death as the bare `signal` row. Witness: `echo hello \| spawn` → `cat exited 0`, nothing read, where `echo hello \| env cat` prints `hello`; `sh -c 'kill -TERM $$'` → `the signal row, no number` | **DROPPED.** The command half is the utility; to be filed |

### Drift, reported

1. **21 utilities exist, not 22** (above). The readiness table will
   have 21 + the new rows.
2. **`env` is dropped**, not because one option is missing but because
   its central job — exec COMMAND with stdin, a modified environment and
   its exit status passed through — has no wolf spelling at all. Its
   print-only half would be `printenv` with a sorted listing, which is
   not the utility.
3. The wave row says "POSIX-only" and "`rev`-free"; `rev` is not a GNU
   coreutils utility and none of the seven is POSIX-only (`nproc` and
   `printenv` are GNU's own). Read as: the seven named, and nothing else.
4. **The harness cannot see a file a utility writes.** `tools/difftest`
   compares stdout, stderr and the exit status, and every case runs in
   the repository root, so `tee FILE` could only be tested through
   `/dev/stdout`. This lane extends the harness (below) and gates the
   extension with a planted difference, rather than test `tee` blind.

## 3. Prediction, committed before the first line of a utility

**3a. The set.** Six utilities ship — `tee`, `printf`, `printenv`,
`pwd`, `sleep`, `nproc` — and `env` is dropped with an upstream issue
and its witness. Four upstream issues are filed (env's surface, the
sorted `env_vars`, the missing file identity, `os_cpus`' rounding) and
`tee`'s two signal needs are added to wolf-lang#423 as a comment.
**Falsifier:** a seventh ships, or one of the six cannot.

**3b. The harness extension.** A case may name a SCRATCH directory: the
harness makes one fresh directory per case, populates it from the case
(`scratch` files, `scratch_dirs`, `scratch_links`), runs each side in it
(or in `cwd` under it) one after the other at the SAME path, and
compares the tree it leaves behind as a fourth field, `files`.
`{scratch}` in `args` and `env` is that path. Two planted differences in
`tests/selftest/` (a file that exists on one side only; a file whose
content differs) must FAIL by name, and `tools/difftest-selftest` must
require both. **Falsifier:** either plant passes; any existing verdict
moves.

**3c. The existing corpus does not move.** At the head, the 21 existing
utilities' verdict lines are identical to base's, line for line (digest
`b97c0e91…` over those 2,114 lines), on kasumi, and CI's three legs
report the same lines for them as bu13's head run 36964596357.
**Falsifier:** any existing verdict line differs.

**3d. Cases.** New cases, all passing on kasumi except stated skips:

| utility | cases | skips predicted, and why |
|---|---|---|
| `sleep` | 25–40 | 0 |
| `nproc` | 20–35 | 0 (the quota divergence is not reachable from a case; it is an evidence run) |
| `pwd` | 20–35 | 0–2 (a `-L` case only a real inode could decide) |
| `printenv` | 20–35 | 3–6: every bare listing (environ order) |
| `tee` | 40–70 | 4–8: `-i` (no SIGINT meaning), and every broken-pipe branch of `-p` and `--output-error` (#423) |
| `printf` | 200–320 | 2–8: glibc's `%I` flag on floating conversions, and anything the host's `long double` decides that the emulation does not reproduce |

Total **330–500 new cases**, **10–30 new skips** on kasumi. On macOS the
`/dev/full` cases skip as they already do.

**3e. printf's floating point is exact, per host.** Every `%f %e %g %a`
case passes on BOTH CI hosts with the host's `long double` emulated
(64-bit mantissa, x87 exponent range, on linux x86-64; IEEE double on
macOS arm64), including the subnormal and overflow edges and the
`Numerical result out of range` / `Result too large` wording, which is
each host's `strerror(ERANGE)`. **Falsifier:** any floating case that
passes on one CI host and fails on the other.

**3f. Speed, kasumi, release tier, against GNU 9.11** (`vs` is GNU's
time over ours, above 1.00 faster):

| bench | band | why |
|---|---|---|
| `sleep 0`, `nproc`, `pwd`, `printenv HOME`, `printf x` | **0.8–1.2x** | process start on both sides, as `echo` (1.04x) and `cat` start-up (0.97x) |
| `sleep 0.1` | **0.97–1.03x** | the sleep dominates; both round up to their own resolution |
| `printf '%d\n'` over 10,000 integers | **0.3–0.9x** | a parse and a decimal render per value against glibc's |
| `printf '%.6f\n'` over 10,000 decimals | **0.05–0.4x** | big-integer conversion both ways where glibc uses `long double` hardware and its own exact printer |
| `printf '%s\n'` over 10,000 words | **0.5–1.2x** | copying bytes |
| `tee FILE > /dev/null`, 256 MiB | **0.4–0.9x** | `cat`'s bulk copy to a file was 0.70x on linux; `tee` writes twice |
| `tee` with no file, 256 MiB into `/dev/null` | **0.15–0.6x** | `cat`'s 0.16x copy to `/dev/null`, without `cat`'s shortcut on either side |

**Falsifier:** any measured ratio outside its band. bu07 got one band
of five right and bu08 four of eight; I expect two to four of these
seven to miss, most likely the two `printf` numeric rows.

**3g. The readiness table.** One row per utility, 27 rows (21 + 6). The
verdict column is mechanical from the evidence: **drop-in** when every
GNU option is covered by a passing case and the only skips are the two
hosts' C libraries or `/dev/full`; **drop-in for scripts that avoid X**
when an option is refused or a stated behaviour differs; **not yet**
when the central job does not hold. Predicted: **9–13 drop-in**
(`true`, `false`, `echo`, `basename`, `dirname`, `yes`, `sleep`,
`nproc`, `printf`, and a few of the text tools whose every option has a
case), **12–17 with a named exception** (`cut` lacks 9.11's `-w -F -O`,
`sort` refuses `-g -V -R`, `tail`/`tac` are slow but correct, `tee -i`,
`printenv`'s listing, `pwd -L`), **0–2 not yet**. **Falsifier:** a
count outside the band.

## 4. Evidence index

All measurement on kasumi (CachyOS, x86-64, 16 cores, load 1.2–1.4
while benches ran), logs under `~/lanes/bu14/`. Three trees: **base** =
trunk `7c3e2da`; **head** = this worktree synced by rsync while
working; **final** = a fresh clone of origin at `bd11397` (the last
commit that moves code or cases), built by `tools/fetch-toolchain`
(`sha256 24855d5e… OK`) and `tools/build`. GNU is Arch's coreutils
9.11-2 on kasumi and Homebrew's 9.11 on this Mac (black-box only).

### 3a scored: the set — held

Six shipped (`7ef104d` sleep, `c578759` nproc, `de23e04` pwd, `e1bff37`
printenv, `83d8dcd` tee, `9e2c19e` printf); `env` dropped. Filed
upstream, each with its witness (`~/lanes/bu14/wit/*/main.lu`,
`witness.txt`, `witness-wrap.txt`; `ev/pwd-twin.txt`,
`ev/printenv-listing.txt`, `ev/nproc-quota-*.log`):

| issue | what | witness |
|---|---|---|
| wolf-lang#534 | no exec, no unset/clear, no child cwd; `os_spawn` null-wires stdin; `os_wait` loses the signal number — `env` | `echo hello \| spawn` → `cat exited 0`; GNU `env cat` → `hello` |
| wolf-lang#535 | `env_vars()` sorted, non-UTF-8 skipped — `printenv`'s listing | `env -i B=1 A=2`: wolf `A=2 B=1`, GNU `B=1 A=2` |
| wolf-lang#536 | no file identity — `pwd -L` | a `cp -a` twin, inodes 6154267/6154269, same size and mtime: boreutils prints the twin, GNU the physical name |
| wolf-lang#537 | `os_cpus` floors a fractional quota | `CPUQuota=150%`: 1 vs GNU 2; `250%`: 2 vs 3; `taskset -c 0-2`: 3 and 3 |
| wolf-lang#538 | `wrapping[u64]` interpolates signed on wolfgang, unsigned on lupin; division refused natively, traps on checked, works on lupin | native and `conform-run --json --checked` print `-1 -9223372036854775808`, lupin `18446744073709551615 9223372036854775808` |

and two comments: wolf-lang#423 (comment 5960914159: `tee -p`,
`--output-error` and `-i`) and wolf-lang#536 (comment 5961000205: `cat f
>> f` grows without end here and refuses in GNU, found while writing the
readiness table). #538 was not predicted: it surfaced in `nproc`.

### 3b scored: the harness extension — held

`tools/difftest` (`08eff09`) gives a case a scratch directory and a
`files` field; `tests/selftest/tee.toml` plants two differences
(`0f28f34`), and `tools/difftest-selftest` now requires every plant to
fail BY NAME. **Seen red**, `ev/selftest-planted.txt`: with `snapshot()`
planted to return nothing, the selftest REFUSES (`the plant 'tee: a file
one side writes' did not fail`, rc 1) — and the real `tee` cases still
pass 62/0/7 under that plant, which is why the plants exist. Unpatched
(`ev/selftest-unpatched.txt`): `0 passed, 3 failed`, `saw every planted
difference`, rc 0. The final tree's selftest, evidence and field-verdict
gates exit 0 (`ev/final/selftest.log`, `evidence.log`,
`field-selftest.log`).

### 3c scored: the existing corpus — held on kasumi

`ev/final/verdicts.txt` (2,674 lines, sha256 `8d354b9bb34f34a1…`); its
2,114 lines for the 21 existing utilities, `verdicts-existing.txt`, hash
`b97c0e91b8d203737eb42c10234517f2ffbcdb7e6d0ba1b70e185b8a3dfc5817`,
**base's digest to the byte** (`diff` empty, `diff_rc=0`). CI's legs at
`bd11397`, run 37060771131, against the same legs of bu13's head run
36964596357, the existing utilities' 2,114 verdict lines of each leg's
differential step extracted and sorted the same way
(`legverdicts.sh`, kept in the PR body): **ubuntu identical**
(sha256 `fde3f0d14a9399f6…` both), **field identical** (`7146d3ea…`
both, the same 15 FAIL lines), **macOS identical** (`9bb2cd72f8a2af50…`
both). **3c held.**

### 3d scored: cases

`ev/final/difftest.log`: **`difftest: 2642 passed, 0 failed, 32
skipped`**, oracle asserted (9.11, `LC_ALL=C _POSIX2_VERSION=200112`,
the `uniq +1` probe OK); `BUILD_EXIT=0`, `wolf test: 1 passed`, fmt
clean (`ev/final/build.log`).

| utility | predicted cases | cases | predicted skips | skips |
|---|---|---:|---|---:|
| `sleep` | 25–40 | **61** (miss) | 0 | 0 |
| `nproc` | 20–35 | **78** (miss) | 0 | 0 |
| `pwd` | 20–35 | **45** (miss) | 0–2 | 1 |
| `printenv` | 20–35 | **37** (miss) | 3–6 | 4 |
| `tee` | 40–70 | 69 | 4–8 | 7 |
| `printf` | 200–320 | 270 | 2–8 | **0** (miss: glibc's `I` flag was implemented, digits dropped, rather than skipped) |
| **total** | 330–500 | **560** (miss) | 10–30 | 12 |

Four per-utility counts and the total missed high: each of the small
utilities has more edge than its size suggested (`nproc`'s OpenMP
grammar alone is 37 cases). 16 cases name `gnu_min = "9.11"` (`49c9459`,
`bd11397`): ubuntu's 9.4 on the `field` leg has no `%N$`, takes an
empty number silently and refuses an `--ignore` past 2^64.

**Beyond the cases**, `printf` was compared with GNU on kasumi over
random arguments (`ev/fuzz/`, `fuzz-results-final.txt`, against the
final tree's binary `4979a998…`): **2,300 integer and floating
conversions (seed 1414) and 2,500 floating ones (seed 2026), 0
mismatches**; the 416 hand probes differ only in `--help`/`--version`
text.

### 3e scored: floats per host — held

Run 37060771131 at `bd11397`: the ubuntu gauntlet (x87 emulated) and the
macOS gauntlet (IEEE double emulated) both pass all 270 `printf` cases,
the `%a`, `%e`, `%f` and `%g` edge cases among them whose right answer
differs between the two hosts — `%.20f 0.1`, `1e309`, the x87
and double subnormals and maxima, `%a` in both libraries' layouts,
`-nan`, and `Numerical result out of range` against `Result too
large`. ubuntu: `difftest: 2642 passed, 0 failed, 32 skipped`; macOS
(`GNU coreutils 9.11 (prefix 'g') on Darwin arm64`): **`2618 passed, 0
failed, 56 skipped`**, the 24 more being every `/dev/full` case.

### 3f scored: speed

`ev/bench/startup-*.json` (`hyperfine -N --warmup 20 --runs 300`),
`ratios.txt`; `printf.md` (first), `printf-after.md`, `tee.md`
(`tools/bench --scale 0.25 --runs 5`), `startup.md`; `host*.txt` loads.

| bench | band | measured | |
|---|---|---|---|
| start-ups: `sleep 0`, `nproc`, `pwd`, `printenv PATH`, `printf x` | 0.8–1.2x | 0.88x, 0.80x, 0.80x, **0.78x**, **0.77x** | two of five below; `true` itself is 0.71x, the floor |
| `sleep 0.1` | 0.97–1.03x | 1.00x | held |
| `printf '%d\n'` × 10,000 | 0.3–0.9x | 0.68x | held |
| `printf '%.6f\n'` × 10,000 | 0.05–0.4x | **0.04x** first; 0.27x after `937f287` | missed as committed |
| `printf '%s\n'` × 10,000 | 0.5–1.2x | 0.86x | held |
| `tee FILE`, 256 MiB | 0.4–0.9x | **1.27x** | missed, the good way |
| `tee` no file, 256 MiB | 0.15–0.6x | **0.70x** | missed, the good way |

Three of seven rows held; I expected two to four to miss and four did.
The floating miss was a design cost found by measuring: every argument
was divided by 5^k bit by bit, and dividing by a one-limb divisor in one
pass took `%.6f` from 218 ms to 29.8 ms (`937f287`); both fuzz runs were
re-taken on the faster binary. Peak RSS of `tee FILE` over 256 MiB:
2.7–2.9 MB against GNU's 2.2 MB (`ev/bench/tee-rss.txt`).

### 3g scored: the readiness table

| verdict | predicted | counted |
|---|---|---:|
| drop-in | 9–13 | **15** (miss) |
| drop-in for scripts that avoid X | 12–17 | 12 |
| not yet | 0–2 | 1 (`env`) |

The miss is the text tools: `tr`, `uniq`, `paste`, `fold`, `expand`
and `unexpand` cover every GNU option with no skip of their own. One
existing verdict moved the other way while the table was being written:
`cat f >> f` refuses in GNU and grows `f` without end here (measured,
reported on wolf-lang#536), so `cat` is not drop-in. Option coverage was
computed from GNU's own `--help` against the case files, then corrected
by hand where a mechanical count lies: `sort -g/-R/-V` appear only in
cases GNU refuses too, and cut's `-M` is a range in GNU's help text, not
an option.

### CI

| run | head | ubuntu | macOS | field (9.4, advisory) |
|---|---|---|---|---|
| 37058558543 | `0f28f34` (four utilities, the harness) | `2372 passed, 0 failed, 32 skipped`; plants FAIL by name | cancelled in the queue (superseded) | — |
| 37059873503 | `9e2c19e` (+ printf) | `2642 passed, 0 failed, 32 skipped` | cancelled in the queue (superseded) | `2585 passed, 31 failed, 58 skipped`: the 16 new 9.4 differences, then bounded with `gnu_min` |
| **37060771131** | **`bd11397`** (every code and case change) | **success**, `2642 / 0 / 32` | **success**, `2618 / 0 / 56` | `2585 passed, 15 failed, 74 skipped`, bu13's same 15 |

The macOS legs queued for an hour behind the org's other macOS jobs;
the two superseded runs were cancelled by this lane to free the slot.
The run at the final head sha (README and notes only after `bd11397`)
is in the PR body: a note cannot cite the run of the commit that
carries it.

**The kasumi upgrade.** At 17:34 EDT on 2026-10-02 kasumi upgraded clang
22.1.8 → 23.1.1 and **GNU coreutils 9.11 → 9.12** (`/var/log/pacman.log`).
Every kasumi measurement above was taken between 15:39 and 16:44 EDT,
with clang 22.1.8 and GNU 9.11-2, so no row straddles it. From now on a
kasumi difftest must stage the oracle with `tools/fetch-oracle`; the
host's own GNU is no longer the oracle of record, and `tools/difftest`
will say so and refuse.

## 5. Done-when

- [x] branch `bu14` on origin; this note's §1–§3 its first commit
      (`c3baf54`)
- [x] six utilities, each with code and cases in one commit (`7ef104d`,
      `c578759`, `de23e04`, `e1bff37`, `83d8dcd`, `9e2c19e`); `env`
      dropped and filed (wolf-lang#534)
- [x] the harness's scratch directory (`08eff09`) and its plants
      (`0f28f34`), the gate seen red on a planted blind snapshot
- [x] benched on kasumi (`d71e062`, `ev/bench/`); README sections,
      status rows and the readiness table (`ce00291`)
- [x] existing verdicts identical to base on kasumi (`b97c0e91…`)
- [x] upstream: wolf-lang#534, #535, #536, #537, #538 filed; #423 and
      #536 commented
- [x] CI green on all three legs at `bd11397`, the last code commit
      (run 37060771131); the run at the final head sha in the PR body
- [ ] PR #18 open, unmerged, five sections in its body
- [ ] kasumi trees pruned (`base`, `head`, `final` target dirs); logs and
      `ev/` kept; no orphan pids
- [ ] worktree gone (after the PR body is final)
