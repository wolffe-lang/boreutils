# bu13 — the pair at 0.2.20

Lane note and contract. **Class:** small (boreutils), **Fable**. **Wave:**
52 ("Pins at 0.2.20"). One oracle: the differential against GNU 9.11,
before and after, by verdict list. One deliverable: the pin at wolf
0.2.20 / lupin 0.1.43, every site that names the pin moved, and any new
diagnostic or behaviour change fixed here or reported. Template: bu11's
contract (`notes/bu11-the-pair-at-0.2.19.md`, PR #16).

§1, §2 and §3 were written 2026-10-02, after the base was measured at
0.2.19 and before any build, difftest or memory measurement at 0.2.20.

## 1. Forbidden, absolutely

- No `rm` outside `~/lanes/bu13/` on kasumi and `/private/tmp/bu13`; no
  deletion in any tree this lane did not create; never another owner's
  target dir. kasumi `/home` is shared by three pin lanes: each item's
  trees are pruned the moment its evidence is written.
- No `git add -A`; no edit to another lane's file; no `~/.claude`.
- No build on this Mac: every build, difftest, RSS and bench run is on
  kasumi, `CARGO_BUILD_JOBS=4`, launched with `setsid`, waited on in a
  printing loop.
- No merge, no rebase-merge; no `2>/dev/null` on a checkout.
- No "seen red" or "seen compiling" without a run id, sha, log path or
  digest in the same paragraph.
- The pin comes from the RELEASE ARCHIVE by digest, never a clone or
  `~/.local/bin`; every member hashed by name (`_wolf` is the zsh
  completion script and hashes the same at every pin).
- Never read, copy or translate GNU coreutils source (the licence rule).
- Kill only this lane's own pids, never a pattern or a process group.
- No commit or PR trailers of any kind.
- A new diagnostic or behaviour change is fixed in boreutils or
  reported, never waived silently.
- A diagnostic count that reads only lines starting `error` misses an
  ICE (bu11's instrument note): every count here carries `rc=` and
  `ice=` beside `errors=`.

## 2. Inputs, re-derived against origin (2026-10-02)

| the contract says | origin says | verdict |
|---|---|---|
| boreutils trunk `0b273a03` (bu11) | `0b273a0`, "notes: bu11 evidence …"; PR #16 MERGED at that sha | holds |
| pins today | `wolf-toolchain.toml`: wolf 0.2.19 `c2401f05`, lupin 0.1.42 `8e2516dc`, std `14f0ab2` | holds |
| wolf **0.2.20**, release 401498582 | wolf-lang tag `v0.2.20` (a tag object, `db412213`) → commit `cdde128a30999652c9d70189664226b766a206f0`; release 401498582, not a draft, not a prerelease, published 2026-10-02T03:16Z, four assets (three unix archives and a windows one) | holds |
| lupin **0.1.43**, release 401010971 | wolf-interp tag `v0.1.43` (a tag object, `818ea0b0`) → commit `6d6cde553ba980527dcbebd4dbe81d63f898d658`; release 401010971, not a draft, not a prerelease, published 2026-10-01T13:46Z, five assets (three unix archives, a windows zip and a bare `lupin.exe`) | holds |
| the pairing | 0.2.20's `crates/wolf_driver/PAIRING`: `lupin-version = 0.1.43`, `lupin-pin = c2401f0`; the linux-x64 archive's `--version` line 2: "paired with lupin 0.1.43 (reference interpreter), pin c2401f0". lupin 0.1.43's spec pin is wolf v0.2.19 (`c2401f05`, the TAG): one release behind, as 0.1.42's was | holds |
| the std pin, re-derived against 0.2.20 first (B151) | wolf-std trunk IS `14f0ab2` (`rev-list --count 14f0ab2..origin/trunk` = 0), so there is one candidate; whether it compiles under 0.2.20 is §3a's measurement | one candidate; measured in §3a |
| boreutils at trunk, 0.2.19 | kasumi, `run-state.sh base` at `0b273a0`: 21 built, `test ./src/bore_test.lu::main ... ok`, `wolf test: 1 passed; 0 failed; 0 rejected; 0 unsupported`, fmt clean, `BUILD_EXIT=0`; **`difftest: 2094 passed, 0 failed, 20 skipped`**, oracle asserted (`GNU coreutils 9.11`, `LC_ALL=C _POSIX2_VERSION=200112`, the `uniq +1 /dev/null` probe OK). Sorted verdict list 2,114 lines, sha256 `b97c0e91b8d203737eb42c10234517f2ffbcdb7e6d0ba1b70e185b8a3dfc5817` — **bu11's, bu10's and bu09's digest**. `probe.sh base` at 0.2.19: 21 × `rc=0 errors=0 warnings=0 ice=0` (`~/lanes/bu13/base-build.log`, `base-difftest.log`, `base-verdicts.txt`, `base-probe.txt`) | holds |
| the six two-phase sites compile unchanged on 0.2.20 (ruling #17) | STATUS.md #17 (ruled 2026-09-30): a later argument may READ a place an earlier `mut` argument claims; writes, moves, re-claims and lends stay E1002. s186's PR (wolf-lang#485) lists the six as reads, clean at its head `e3ae62b5` with no edit; s192's PR says boreutils `0b273a03` builds 46 of 46 at its head. Neither is the RELEASE archive; §3a measures it there | holds as a claim about trunk heads; measured on the archive in §3a |

### The archives, by digest

Downloaded from the two release pages on kasumi and hashed there
(`~/lanes/bu13/archives.sha256`); each equals the `digest` GitHub's
release API publishes for the asset. Windows is out of scope and not
pinned.

| archive | sha256 |
|---|---|
| wolf-0.2.20-aarch64-apple-darwin.tar.gz | `c8a3f1a3785628ff055dc61a7ca5e48e212a431dca4bc05fe0e21cc2a46d6315` |
| wolf-0.2.20-x86_64-unknown-linux-gnu.tar.gz | `24855d5efae9515ac092f1db11613187838f018f017dc20416f70905fb816ce9` |
| wolf-0.2.20-aarch64-unknown-linux-gnu.tar.gz | `30f9fad962d9a4a84076549527800e226fd4078d179d68430ed3d1a75559a730` |
| lupin-0.1.43-aarch64-apple-darwin.tar.gz | `24d3e8f1650402c901fa13a1409b5096ce628964e2793b2c0f298a30b8a61190` |
| lupin-0.1.43-x86_64-unknown-linux-gnu.tar.gz | `e957c8def153f507520a1f7f98f7f391cd43e731ee73c25c6a7bdef4d3090d48` |
| lupin-0.1.43-aarch64-unknown-linux-gnu.tar.gz | `e0620310294706dc32dbb900be445a5f08a8b50fd18c16e4a9fe509b2beb2aa7` |

Members by name (`~/lanes/bu13/*.members`, one file per archive):

| member | darwin-arm64 | linux-x64 | linux-arm64 |
|---|---|---|---|
| `wolf` | `00b5459c…` | `3fb48c1d…` | `e421f54e…` |
| `libwolf_rt.a` | `d87f121a…` | `c011f2ae…` | `51c5951f…` |
| `wolf-cimport-worker` | `fe5825c3…` | `13a61554…` | `0248f2f3…` |
| `_wolf` (zsh completion) | `2d1e4801…` | `2d1e4801…` | `2d1e4801…` |
| `lupin` | `a8374eac…` | `3b0702c0…` | `9da20579…` |

Identity lines, from the linux-x64 archives (`~/lanes/bu13/identity.txt`):
`wolf 0.2.20 (wolfgang, pin cdde128)` / `paired with lupin 0.1.43
(reference interpreter), pin c2401f0` and `lupin 0.1.43 (wolf-interp,
reference interpreter at pin c2401f0)`.

### What 0.2.20 changes, and where it could land here

Read from 0.2.20's `CHANGELOG.md` ("Read this before you bump the pin")
and from `git diff --name-only v0.2.19 v0.2.20` in wolf-lang, outside
tests and corpus: `wolf_mem` (seven files), `wolf_sema` (`check.rs`,
`ctfe/eval.rs`), `wolf_wir` (`lower.rs` +435, `parse.rs`), `wolf_parse`
(`exprs.rs`), `wolf_ast`, **`wolf_rt/src/signal.rs` (+118)**,
`wolf_driver/PAIRING`, `docs/`, `spec/`. Unlike 0.2.19, one runtime
source file moved, so every native binary's `libwolf_rt.a` differs.

- **Refused now, compiled before** (the checker): a write, move,
  re-claim or lend of a `mut`-claimed place or `mut` receiver inside a
  later argument of the same call (E1002, #476/#487); a moded fn used
  as a value (#484); a call to a nested fn that omits its parameter's
  mode (E1007, #466); a read of a local after `W { local }` moved it
  (E1001, #486). Scanned in `src/` today: no struct-literal field
  shorthand (a grep for `Name { ident }` finds none); no nested `fn`
  with a `mut`/`take` parameter; no fn read as a value (the two
  bare-identifier assignments a scan found, `basename.lu:70` `names =
  one` and `seq.lu:962` `let _ = one`, are locals named `one`, not the
  eight `fn one(...)`s); the later arguments at every two-`mut`
  call line are claims of distinct places, not writes. s186 and s192
  built `0b273a03` with no diagnostic at their heads.
- **Compiled now, refused before**: a direct read of a claimed place in
  a later argument (ruling #17) and two claims through an offset or a
  loop index (EG3). The six sites s186 named (`head.lu:522`, `:613`
  `bore.ring_drop(mut r, bore.ring_len(r))`; `paste.lu:357`
  `ensure(mut f, f.len + n, keeper)`; `tail.lu:710`, `:726`, `:776`)
  compile at 0.2.19 (the base probe) and the ruling keeps them legal;
  nothing here waited on EG3.
- **The runtime** (#483): `os_signal_listen` has the drain thread
  unblock the signals a program arms; every other signal keeps the
  inherited mask. No boreutils program arms a signal (`grep -rn signal
  src` finds one comment, `bore.lu:51`; SIGPIPE is left alone,
  wolf-lang#423), so the new path is never entered here, and no
  differential case can see it.
- **The checked machine only** (#481, #479, #492): index operands,
  slice endpoints and `else` under a propagating `?`. The native
  binaries under test never run on it; `wolf test` does (one file,
  `src/bore_test.lu`, which has no `?`-under-`else` and no slice with
  a call endpoint).
- **The view-set receiver write-back** (#494) and the `0x` WIR lexer
  (#496): no `mut self.{…}` in `src/`; lowering never emits a scaled
  deref. s193 reported boreutils' binaries byte-identical across its
  change.
- The six README sentences and one `sink.lu` comment that say "wolf
  0.2.19 has no …" name wolf-lang#405, #407, #417, #426 and wolf-std
  F-0011 (wolf-lang#416). All five issues are OPEN today (API read
  2026-10-02), and the `v0.2.19..v0.2.20` diff under `spec/`, `docs/`
  and `wolf_rt` adds no seek, tell, splice, copy_file_range, sendfile,
  errno, strerror, capacity or truncate surface (grep of the added
  lines: the only hits are the self-pipe's comments).

### Drift, reported

1. **The task's "every site the pin names"**: outside
   `wolf-toolchain.toml` the pin is named in the same seven prose sites
   bu11 found (README :66, :88, :272, :342, :526, :570;
   `src/bore/sink.lu`:6), each a claim about what wolf lacks. They move
   to 0.2.20 only because the claim was re-checked above; `src/seq.lu`
   :208 names 0.2.16 as history and the `0.2.14` measurement notes
   stay.
2. The `[lupin]` comment in `wolf-toolchain.toml` says the pin lupin
   conforms to is "wolf v0.2.18"; at 0.1.43 it is v0.2.19 (`c2401f0`),
   still one release behind. Corrected with the pin.
3. bu11's §2 said "no runtime source moved" of 0.2.19; of 0.2.20 that
   sentence is false (`signal.rs`), which is why §3c and §3d are
   measured rather than argued.
4. The release's CHANGELOG is dated 2026-10-01 and the GitHub release
   was published 2026-10-02T03:16Z; the tag's commit is `cdde128a`,
   which the identity line prints as `pin cdde128`.
5. None in the numbers: every other input above held.

## 3. Prediction, committed before any build at 0.2.20

**3a. The build.** At 0.2.20 / 0.1.43 / std `14f0ab2`, source unchanged:
- std `14f0ab2` compiles, and **all 21 utilities build under
  `--release --deny-warnings --error-limit=0` with
  `rc=0 errors=0 warnings=0 ice=0`**. The six two-phase sites are
  among them, unchanged: **0 new diagnostics**.
- `wolf test` prints `test ./src/bore_test.lu::main ... ok` and
  `1 passed; 0 failed; 0 rejected; 0 unsupported`; `wolf fmt --check`
  clean.
- **The test is seen to fail** (s186's gap: a `1 passed` names no
  file): a copy of the tree with one `assert` in `src/bore_test.lu`
  made false (`want` altered on the first `check` line) gives
  `wolf test` exit 1 and a `FAILED` line naming `./src/bore_test.lu`,
  at 0.2.19 and at 0.2.20.
- **Falsifier:** any diagnostic in any utility or in std; a `wolf
  test` line that does not name `src/bore_test.lu`. A refused site is
  fixed in its own commit, named with file:line and its diagnostic,
  and seen compiling after; a behaviour change is reported.
- **The zero is seen to fire** on six witnesses built by the probe's
  command and counted by its grep, each alone in its directory, at
  both pins, `--deny-warnings` and plain. Five are wolf-lang's corpus
  rows at `v0.2.20`; the sixth is the `mut_value_return` program from
  `fn_value_modes_lanes.rs`:

  | witness | at 0.2.19 | at 0.2.20 |
  |---|---|---|
  | w2pr `memory/mut_claim_two_phase_reads.lu` | rc 2, `error[E1002]` | **rc 0, prints `2 4 23 1 3 5 2 3`** |
  | weg3 `memory/elem_offset_mut_pair.lu` | rc 2, `error[E1002]` | **rc 0, prints `2 12`** |
  | wblk `memory/mut_claim_arg_block_write.lu` | rc 0, prints `2` (the wrong answer) | **rc 2, `error[E1002]`** |
  | wrcv `memory/recv_claim_arg_write.lu` | rc 0, prints `1 9` (the wrong answer) | **rc 2, `error[E1002]`** |
  | wsh `memory/field_shorthand_moves.lu` | rc 0, prints `2 2` (the wrong answer) | **rc 2, `error[E1001]`** |
  | wfnv `mut_value_return` (a `mut int` fn returned as a value) | **rc ≠ 0, `errors=0`, `ice=1`** (the release-tier ICE the CHANGELOG names) | rc ≠ 0, `ice=0`, the first diagnostic line says a fn with `mut` or `take` parameters is used as a value |

  wfnv is the row that shows why `ice=` exists: at 0.2.19 its
  `errors=` column reads 0 while the build failed.

**3b. The difftest.** **2094 passed, 0 failed, 20 skipped**, the sorted
verdict list **identical line for line** to the base's (sha256
`b97c0e91…`). No case runs the compiler; the checker changes what
compiles, not what a compiled program does; the one runtime change is
on a path no utility enters. **Falsifier:** any verdict line that
moves. The comparison is seen to fire on the base list with its first
line dropped.

**3c. Peak memory.** Every one of the 21 utilities' peak RSS at the pin
within **max(5 %, 2 MB)** of its base (0.2.19) median; bu11's
instrument (`/usr/bin/time -o … -f %M`, non-empty and numeric asserted,
three rounds, states interleaved, 64 MiB seed-9 text, `LC_ALL=C`).
**Falsifier:** any utility outside the band.

**3d. The two-phase sites.** The three utilities that carry the six
sites run at the speed they ran at 0.2.19, on workloads that reach the
sites: `head -n -1000` (the ring at `head.lu:522`/`:613`), `tail -n
100000` (`tail.lu:710`/`:726`/`:776`) and `paste f f`
(`paste.lu:357`), 64 MiB input, `hyperfine -N --warmup 2 --runs 10`,
base and pin alternated, **pin mean within ±5 % of base mean** for
each. **Falsifier:** any of the three outside ±5 % in two consecutive
measurements (one is noise on a shared host).

## 4. Evidence index

All measurement on kasumi (CachyOS, x86_64, 16 cores, load 3–5 from
two sibling pin lanes), logs under `~/lanes/bu13/`. Three trees, each a
clone of origin: **base** = trunk `0b273a0` at 0.2.19 / 0.1.42 / std
`14f0ab2`; **pin** = `4fea18c` (the pin commit, source unchanged) at
0.2.20 / 0.1.43 / std `14f0ab2`; **head** = `8fe0017` (the pin plus the
README and `sink.lu` sentences restated at 0.2.20). Toolchains staged
by `tools/fetch-toolchain` from `~/lanes/bu13/arch/`, each archive
digest-checked by the tool (`*-build.log` quotes each `sha256 … OK`).
The trees, the extracted archives, the probe binaries and the 64 MiB
input were pruned after this section was written; `archives.sha256`,
the `*.members` lists, `plant/` (sources and logs, binaries removed)
and every log below are kept.

### 3a scored: the build

**Per utility, `--release --deny-warnings --error-limit=0`**
(`probe.sh`, `pin-probe.txt`, `head-probe.txt`, one log per utility in
`pin-probe/` and `head-probe/`): identity `wolf 0.2.20 (wolfgang, pin
cdde128)`, std `14f0ab2c6a64e86240113e21c4da9f746380eb29`, the flag
present, and **all 21 utilities `rc=0 errors=0 warnings=0 ice=0`**, at
pin and at head (the two probe files differ only in nothing: `diff` of
their utility lines is empty). The same probe at base (`base-probe.txt`,
0.2.19) prints the same 21 lines. std `14f0ab2` compiles under 0.2.20
(every utility reaches `std.env`). `head`, `paste` and `tail` are three
of the 21, so **the six two-phase sites (`head.lu:522`, `:613`,
`paste.lu:357`, `tail.lu:710`, `:726`, `:776`) compile unchanged on the
0.2.20 archive, 0 new diagnostics.** 0.2.20 refuses no site and warns
at none; there is nothing to fix.

Then `tools/build` + `tools/check-test` + `tools/check-fmt` at pin and at
head: 21 built, **`test ./src/bore_test.lu::main ... ok`**, `wolf test:
1 passed; 0 failed; 0 rejected; 0 unsupported; 0 filtered out`, fmt
clean (the three are one `&&` chain), `BUILD_EXIT=0` (`pin-build.log`,
`head-build.log`). The 21 binaries at pin and head are byte-identical
(`bins-pin.txt` = `bins-head.txt`), and all 21 differ from base's
(`bins-base.txt`): the prose commits moved no code.

**`wolf test` runs `src/bore_test.lu`, and was seen red** (s186's gap;
`testplant.sh`, `testplant.txt`). `wolf test` names the one test it
discovers, `./src/bore_test.lu::main` (the file has no `fn test_*`, so
it runs black-box as the one test named `main`, on the checked
machine). In a copy of each tree's `src/` with the first
`check_optional` line's `want` altered (`o=[x]` → `o=[PLANT]`, one line,
asserted), `tools/check-test` exits 1 with `test ./src/bore_test.lu::main
... FAILED (trap(assert))` and `wolf test: 0 passed; 1 failed`, at
0.2.19 and at 0.2.20 alike.

**The zero was seen to fire** (`plant.sh`, `plant/plant.txt`,
`plant/sources.sha256`): six witnesses, each alone in its directory,
built by the probe's command and counted by its grep, at both pins,
`--deny-warnings` and plain (the two modes agree in every cell, so one
column per pin below). Five are wolf-lang's corpus rows at `v0.2.20`;
`wfnv` is the `mut_value_return` program from `fn_value_modes_lanes.rs`.

| witness | 0.2.19 (`9f3873d8…`) | 0.2.20 (`24855d5e…`) | §3a said |
|---|---|---|---|
| w2pr `mut_claim_two_phase_reads.lu` | rc 2, `error[E1002]` "`a` is read for this call after `a` goes `mut` in it" | **rc 0, prints `2 4 23 1 3 5 2 3`** | held |
| weg3 `elem_offset_mut_pair.lu` | rc 2, `error[E1002]` "`xs[_]` … overlaps `xs[i]`" | **rc 0, prints `2 12`** | held |
| wblk `mut_claim_arg_block_write.lu` | rc 0, prints `2` | **rc 2, `error[E1002]` "`a` is written while `a` is lent `mut` to the call being evaluated"** | held |
| wrcv `recv_claim_arg_write.lu` | rc 0, prints `1 9` | **rc 2, the same E1002 for `xs`** | held |
| wsh `field_shorthand_moves.lu` | rc 0, prints `2 2` | **rc 2, `error[E1001]` "`xs.len` is used here after its value moved away"** | held |
| wfnv `mut_value_return` | **rc 0, no diagnostic, `ice=0`; the binary dies with SIGSEGV (exit 139, no output)** | **rc 4, `errors=0`, `ice=0`**: "cannot compile this yet — a fn with `mut` or `take` parameters used as a value (a fn type carries no modes; call it by name)" | **missed, both cells** |

So the staged 0.2.20 is the release the CHANGELOG describes in both
directions for the five corpus rows: it accepts ruling #17's reads and
EG3's offset pair, and refuses the write in a later argument, the
written receiver and the shorthand's moved local. **The sixth row is a
prediction published wrong.** §3a took the CHANGELOG's "was an ICE on
native and release" at its word and predicted `ice=1` at 0.2.19; on
the published 0.2.19 archive the program compiles silently and the
binary segfaults, which is a silent miscompile, not an ICE, and at
0.2.20 the refusal is a `[conf.exit]` 4 whose line starts `wolf build:
cannot compile this yet`, which neither `errors=` nor the ICE grep
counts (only `rc=` sees it). Reported on wolf-lang#484 (comment
5945614379) so the CHANGELOG's description of 0.2.19 is not relied on;
nothing is owed in boreutils, which has no fn read as a value.

**The `ice=` column was therefore seen to fire elsewhere**
(`plant-ice.sh`, `plant/w470/arch.txt`): bu11's w470
(`corpus/memory/mut_two_fields_one_region.lu` at `v0.2.19`, sha256
`014260bb…`) against the 0.2.18 linux-x64 archive, downloaded and
hashed `da027bf9…` = the release API's digest for release 397723077,
identity `wolf 0.2.18 (wolfgang, pin ec56a08)`: `rc=2 errors=0
warnings=0 ice=1 first=wolf build: ICE: mid-end broke the module`, deny
and plain. That is the row that shows why the column exists: `errors=`
reads 0 while the build failed.

### 3b scored: the difftest

| tree | answer | sorted verdict list (2,114 lines) sha256 | log |
|---|---|---|---|
| base `0b273a0` @0.2.19 | `difftest: 2094 passed, 0 failed, 20 skipped` | `b97c0e91b8d20373…` | `base-difftest.log` |
| pin `4fea18c` @0.2.20 | `difftest: 2094 passed, 0 failed, 20 skipped` | `b97c0e91b8d20373…` | `pin-difftest.log` |
| head `8fe0017` @0.2.20 | `difftest: 2094 passed, 0 failed, 20 skipped` | `b97c0e91b8d20373…` | `head-difftest.log` |

`diff base-verdicts.txt pin-verdicts.txt` and `diff pin-verdicts.txt
head-verdicts.txt` both print nothing (exit 0); the full digest,
`b97c0e91b8d203737eb42c10234517f2ffbcdb7e6d0ba1b70e185b8a3dfc5817`, is
bu11's, bu10's and bu09's too (`*-verdicts.sha256`). **The comparison
was seen to fire**: base's list with its first line dropped
(`fire-base-minus-first.txt`) diffs against pin as `0a1 > ok
basename: a backslash operand in the diagnostic`, `fire_rc=1`
(`fire-check.txt`). Each run asserted the oracle (`GNU coreutils 9.11`,
`LC_ALL=C _POSIX2_VERSION=200112`, the `uniq +1 /dev/null` probe OK)
and named the tree under test (`difftest: bore = …/pin/target/release`).
**3b held.**

### 3c scored: peak RSS

`rss.sh` (bu11's, retargeted), raw lines `rss-raw.txt` (`state util KB
rc`, 126 lines, **0 `EMPTY`**). Three rounds, base and pin interleaved
in each, 64 MiB of generated text (`rss-input.txt`: 67,108,907 bytes,
sha256 `73c1f166…`, bu11's and bu10's input to the byte). `false` exits
1 and `yes` 124 (`timeout 2`) by design; every other run exits 0.

| utility | workload | base KB | pin KB | pin vs base (median) |
|---|---|---|---|---|
| true | `--version` | 2448 2164 2364 | 2544 2492 2516 | +6.4 % (152 KB) |
| false | `--version` | 2448 2488 2372 | 2356 2352 2504 | −3.8 % (92 KB) |
| echo | 1,000 operands | 2636 2492 2440 | 2656 2640 2648 | +6.3 % (156 KB) |
| basename | a path, a suffix | 2524 2436 2500 | 2468 2280 2468 | −1.3 % |
| dirname | a path | 2488 2524 2440 | 2500 2408 2468 | −0.8 % |
| yes | 2 s to `/dev/null` | 2356 2400 2384 | 2384 2396 2348 | +0.0 % |
| cat | file | 2728 2788 2736 | 2844 2820 2764 | +3.1 % (84 KB) |
| cut | `-f1,3` file | 4020 4088 4144 | 4128 4184 3956 | +1.0 % |
| head | `-n 100000` file | 2940 2968 2924 | 2884 2844 3000 | −1.9 % |
| tail | `-n 100000` file | 36128 36116 36160 | 36148 35884 36084 | −0.1 % |
| nl | file | 12288 12416 12364 | 12260 12292 12368 | −0.6 % |
| seq | `1000000` | 3408 3540 3504 | 3652 3504 3536 | +0.9 % |
| uniq | file | 6220 6268 6100 | 6264 6316 6180 | +0.7 % |
| wc | file | 4272 4412 4348 | 4284 4396 4404 | +1.1 % |
| tr | `a-z A-Z` < file | 6908 6844 6976 | 6908 6964 6836 | +0.0 % |
| tac | file | 201148 199268 201184 | 199628 201412 201140 | −0.0 % |
| paste | file file | 4512 4272 4564 | 4532 4584 4508 | +0.4 % |
| fold | `-w 40` file | 4536 4508 4524 | 4352 4524 4548 | +0.0 % |
| expand | file | 3656 3704 3712 | 3808 3740 3724 | +1.0 % |
| unexpand | `-a` file | 3244 3368 3064 | 3288 3308 3344 | +2.0 % |
| sort | `-S 10M -T` file | 43692 43964 43472 | 43384 43120 43216 | −1.1 % (476 KB) |

**Every utility is inside max(5 %, 2 MB). 3c held.** The two moves
past 5 % (`true` +6.4 %, `echo` +6.3 %) are 152–156 KB on a 2.4–2.6 MB
process, inside the 2 MB floor and inside base's own spread across
rounds (`true` 2164–2448); `tail`, `tac` and `sort`, the utilities
that hold real memory, move by under 0.5 MB. The whole-runtime change
(#483) costs no resident page a boreutils program touches.

### 3d scored: the two-phase sites

`bench.sh`, `bench.txt`, one JSON and log per pass
(`bench-{head_n_1000,tail_n_100000,paste}-pass{1,2}.json`): `hyperfine
-N --warmup 2 --runs 10`, input as 3c (`bench-input.txt`), pass 2 runs
pin first.

| workload | pass 1 base / pin (ms) | pin/base | pass 2 base / pin (ms) | pin/base |
|---|---|---|---|---|
| `head -n -1000` 64 MiB | 197.6 / 185.0 | 0.936 | 174.7 / 169.0 | 0.967 |
| `tail -n 100000` 64 MiB | 348.1 / 346.0 | 0.994 | 316.2 / 332.2 | 1.050 |
| `paste f f` 64 MiB | 567.7 / 556.5 | 0.980 | 535.6 / 510.9 | 0.954 |

**3d held by its falsifier: no workload is outside ±5 % in two
consecutive measurements.** Two single-pass ratios sit at or past the
band, one in each direction: `head` pass 1 (0.936, the pin faster) and
`tail` pass 2 (1.050, the pin slower by 16 ms with a 27 ms standard
deviation); the other pass of each is inside. The spread is the host's
(standard deviations 5–48 ms, load 3–5 from two sibling pin lanes;
bu11's day had 1–3 ms), not the release's: no workload is slower at the
pin twice, and `paste`, the one site that pushes through the claimed
list, is faster at the pin in both passes. A third pass was attempted
and the harness refused the command; the verdict rests on the two
passes and the falsifier as written.

### Predictions, scored

| prediction | result |
|---|---|
| 3a: std `14f0ab2` and all 21 utilities build at 0.2.20 with `rc=0 errors=0 warnings=0 ice=0`; the six two-phase sites unchanged | **held** (21 × 4 zeros at pin and at head) |
| 3a: `wolf test` names `./src/bore_test.lu::main`, 1 passed; fmt clean; the plant goes red at both pins | **held** (`FAILED (trap(assert))`, exit 1, both pins) |
| 3a: the six witnesses | **five held, one missed both cells** (wfnv: 0.2.19's archive segfaults instead of ICEing; 0.2.20 refuses with exit 4 and no `error` line); the `ice=` column seen to fire on w470 at 0.2.18 instead |
| 3b: verdict list identical, 2094/0/20 | **held** (base = pin = head, digest `b97c0e91…`; the diff seen to fire) |
| 3c: peak RSS within band | **held** (21 of 21) |
| 3d: `head -n -1000`, `tail -n 100000`, `paste` within ±5 % | **held by the falsifier** (no workload outside twice; two single-pass crossings, one each way, recorded) |

### CI

**PR #17 run 36964596357 at `8fe0017`** (the head before this note's
evidence commit), all three legs success, read with `gh run view` and
each job's `--log`. Each leg's sorted verdict list (the differential
step's `ok`/`FAIL`/`SKIP` lines) was diffed against the same leg of
bu11's head run 36749293306, and **all three are identical** (2,114
lines each):
- gauntlet ubuntu: `difftest: 2094 passed, 0 failed, 20 skipped`,
  oracle 9.11, archives `24855d5e…` / `e957c8de…` OK, identity
  `wolf 0.2.20 (wolfgang, pin cdde128)`, `wolf test` 1 passed
- gauntlet macOS (the darwin-arm64 archives `c8a3f1a3…` / `24d3e8f1…`
  OK): `2077 passed, 0 failed, 37 skipped`
- field: `2053 passed, 15 failed, 46 skipped` against ubuntu's 9.4,
  advisory, the same 15 FAIL lines as bu11's
- on both gauntlets the planted red fires (`0 passed, 1 failed`,
  `difftest-selftest: the harness saw the planted difference`) and the
  report-survival step passes (`1 passed`)

The linux-arm64 digests are verified by hash only; no leg runs that
archive. The run at the final head sha is in the PR body (a note cannot
cite the run of the commit that carries it).

## 5. Done-when

- [x] branch `bu13` on origin; this note's §1–§3 the branch's first
      commit (`7d89fe9`)
- [x] pin: `wolf-toolchain.toml` at 0.2.20 / 0.1.43 / std `14f0ab2`,
      three digests per half, in its own commit (`4fea18c`)
- [x] every prose site naming 0.2.19 re-checked and moved (`a041fca`
      README ×6, `8fe0017` `sink.lu`)
- [x] every utility built at the pin, 0 diagnostics (`rc`, `errors`,
      `warnings`, `ice`), the count seen to fire both ways; the six
      two-phase sites witnessed unchanged; `wolf test` seen to name
      `src/bore_test.lu` and seen red on a plant
- [x] difftest verdict lists: base = pin = head; diff empty; the
      comparison seen to fire; CI legs compared to bu11's run
      36749293306
- [x] peak RSS and the two-phase-site bench beside §3c and §3d
- [ ] PR open, unmerged; CI green on all three legs at the head sha
      (`gh run view`) — in the PR body
- [x] §2 drift reported; five sections; the wfnv miss reported on
      wolf-lang#484; kasumi build dirs pruned (logs kept); no orphan
      pids
- [ ] worktree gone (after the PR body is final)
