# bu10 — the pair at 0.2.18

Lane note and contract. **Class:** small (boreutils), **Opus**. **Wave:**
50. One oracle: the differential against GNU 9.11, before and after, by
verdict list. One deliverable: the pin at wolf 0.2.18 / lupin 0.1.41,
with every site 0.2.18 newly refuses named and fixed. Template: bu09's
contract (`notes/bu09-the-pair-and-the-449-revert.md`).

§1, §2 and §3 were written 2026-09-28, after the base was measured at
0.2.17 and before any build, difftest or memory measurement at 0.2.18.

## 1. Forbidden, absolutely

- No `rm` outside `~/lanes/bu10/` on kasumi and `/private/tmp/bu10`; no
  deletion in any tree this lane did not create; never another owner's
  target dir.
- No `git add -A`; no edit to another lane's file; no `~/.claude`.
- No build on nomad-1: every build, difftest and RSS run is on kasumi.
- No merge, no rebase-merge; no `2>/dev/null` on a checkout.
- No "seen red" or "seen compiling" without a run id, sha, log path or
  digest in the same paragraph.
- The pin comes from the RELEASE ARCHIVE by digest, never a clone or
  `~/.local/bin`; every member hashed by name (`_wolf` is the zsh
  completion script and hashes the same at every pin).
- Never read, copy or translate GNU coreutils source (the licence rule).
- Kill only this lane's own pids, never a pattern or a process group.
- No commit or PR trailers of any kind.
- A site 0.2.18 refuses is fixed in the shape the release note names
  (a store back before each return, or a `copy`), never silenced.

## 2. Inputs, re-derived against origin (2026-09-28)

| the contract says | origin says | verdict |
|---|---|---|
| boreutils trunk `74069bd` (bu09) | `74069bd`, "notes: where bu09's CI evidence lives"; trunk push run 36276866119 success | holds |
| pins today | `wolf-toolchain.toml`: wolf 0.2.17 `02afce84`, lupin 0.1.40 `54f85e69`, std `14f0ab2` | holds |
| wolf **0.2.18** = `ec56a08f`, release 397723077 | tag `v0.2.18` → tag object `d9732fbe` → commit `ec56a08f04ff318ea659fd58683f7ae4f22dc7a5`; release 397723077, not a draft, four assets | holds |
| lupin **0.1.41** = `0cfc0cf`, release 397709135 | tag `v0.1.41` → tag object `0390e810` → commit `0cfc0cfc89af5fd2aeb71d46c86742745b902869`; release 397709135, not a draft, five assets | holds |
| wolf-lang#464 (s184) and #460 (eg01) ship in 0.2.18 | #464 CLOSED 2026-09-27T07:12:58Z, #460 CLOSED 2026-09-27T02:35:41Z; s184's merge `355a90cf` is an ancestor of `v0.2.18` (compare: ahead 6, behind 0); the 0.2.18 CHANGELOG's "Read this before you bump the pin" names exactly these two refusals | holds |
| the std pin, re-derived against 0.2.18 first (B151) | wolf-std trunk IS `14f0ab2` (compare `14f0ab2...trunk`: ahead 0, behind 0), so there is one candidate and no choice to make; whether it compiles under 0.2.18 is a build, and a build at 0.2.18 is §3a's measurement, so it is predicted below rather than probed before this commit | one candidate; measured in §3a |
| boreutils at trunk, 0.2.17 | kasumi, `run-state.sh base` at `74069bd`: 21 utilities built, `wolf test: 1 passed`, `wolf fmt --check` clean, `BUILD_EXIT=0`; **`difftest: 2094 passed, 0 failed, 20 skipped`**; oracle asserted (`GNU coreutils 9.11`, `LC_ALL=C _POSIX2_VERSION=200112`, the `uniq +1 /dev/null` probe OK). Sorted verdict list, 2,114 lines, sha256 `b97c0e91b8d203737eb42c10234517f2ffbcdb7e6d0ba1b70e185b8a3dfc5817` — **the same digest as bu09's four states** (`~/lanes/bu10/base-build.log`, `base-difftest.log`, `base-verdicts.txt`) | holds |

### The archives, by digest

Downloaded from the two release pages on kasumi and hashed there
(`~/lanes/bu10/archives.sha256`); each equals the digest GitHub's release
API publishes for the asset. Windows is out of scope and not pinned.

| archive | sha256 |
|---|---|
| wolf-0.2.18-aarch64-apple-darwin.tar.gz | `b8f360456490826726301df3f25ef7d2610ab262e5938702add0baa0920ec3f9` |
| wolf-0.2.18-x86_64-unknown-linux-gnu.tar.gz | `da027bf9da4c5a9dfa42c4ac6c7da3072ffce84922916650f024af83701e6bd4` |
| wolf-0.2.18-aarch64-unknown-linux-gnu.tar.gz | `fe6adec8711a037783cf51757d558bf963b063f92c9125e6a93f015009e4ea16` |
| lupin-0.1.41-aarch64-apple-darwin.tar.gz | `2b8c14b00a80e50ac0b8d619f9cb66b386eaffc75b779d1b9ccd225ba5c1fe84` |
| lupin-0.1.41-x86_64-unknown-linux-gnu.tar.gz | `18848901a5202162c9d0c3001a62fa3ac57276d8c0fce9c2d4f43d8d50b4e8d4` |
| lupin-0.1.41-aarch64-unknown-linux-gnu.tar.gz | `58028bc9db0ccf837f627e6bde7418d715a69bc87eaa6b8c69b2f39c242f4561` |

Members by name (`~/lanes/bu10/members/*.members`):

| member | darwin-arm64 | linux-x64 | linux-arm64 |
|---|---|---|---|
| `wolf` | `1b90e0dd…` | `a9556245…` | `535b157b…` |
| `libwolf_rt.a` | `8b8c95a8…` | `5360ecd6…` | `9594d11e…` |
| `wolf-cimport-worker` | `b79781bc…` | `b2525d00…` | `05248d23…` |
| `_wolf` (zsh completion) | `2d1e4801…` | `2d1e4801…` | `2d1e4801…` |
| `lupin` | `5750da96…` | `c5a65edf…` | `618159b6…` |

`_wolf` hashes `2d1e48018333…` in all three, as at 0.2.16 and 0.2.17.
Identity lines, from the linux-x64 archives (`~/lanes/bu10/identity.txt`):
`wolf 0.2.18 (wolfgang, pin ec56a08)` / `paired with lupin 0.1.41
(reference interpreter), pin 93a5fe5` and `lupin 0.1.41 (wolf-interp,
reference interpreter at pin 93a5fe5)`.

### The static inventory: where 0.2.18's two refusals could land

0.2.18 refuses two shapes 0.2.17 compiled (its CHANGELOG, "Read this
before you bump the pin"):

- **#464**: a function that moves out of a `mut` parameter (whole, a
  field, an element, a map value) and returns without storing back.
- **#460**: a read of a moved element after an index store elsewhere
  in the container revived it.

What `src/` at `74069bd` offers each:
- `grep -rnwE 'move|take' src` finds **27 lines, every one a comment**:
  no `move` or `take` expression anywhere, and no `take` parameter.
- A scan of every function with a `mut` parameter for a read-out of that
  parameter or one of its fields/elements (`= p`, `= p.f`, `= p[i]`,
  `return p…`) finds 10 lines, all `int` or `bool` (`Copy`): `ring.lu`
  :64, :99 (`r.cap`), `cat.lu` :299–302, :407 (`st.line_start`,
  `pending_cr`, `blanks`, `num`), `paste.lu` :344, :349 (`r.pos`,
  `r.len`), `sort.lu:2105` (`rd.slot`, `int`). A `Copy` read-out is not
  a move, so none is #464's shape.

The scan is a heuristic over text; the compiler is the oracle, and the
per-utility probe in §3a counts with `--error-limit=0`.

### Drift, reported

1. **The wave row's "#464's rule may reach a helper that moved out of a
   `mut` parameter" names a shape the text of `src/` does not contain**:
   no expression moves anything by name. The only way it can still land
   is an implicit move of a non-`Copy` value the scan missed; §3a says
   what would show it.
2. lupin 0.1.41's own pin is still `93a5fe5` (wolf v0.2.16), as 0.1.40's
   was; that is the pairing the release declares and is recorded, not a
   defect.

## 3. Prediction, committed before any build at 0.2.18

**3a. The build.** At 0.2.18 / 0.1.41 / std `14f0ab2`, source unchanged:
- std `14f0ab2` compiles, and **all 21 utilities build under
  `--release --deny-warnings` with zero diagnostics**: no E1001 (#464,
  #460), no E1002, no new warning. Counted per utility with
  `--error-limit=0` so a count cannot plateau at 25 (ws42).
- `wolf test` 1 passed; `wolf fmt --check` clean (a formatter change at
  0.2.18 would show here).
- **Falsifier:** any diagnostic in any utility or in std. A refused
  site is fixed in the release note's shape — a store back before every
  return, or `copy` at the read — in its own commit, named here with
  file:line and its diagnostic, and seen compiling after.

**3b. The difftest.** **2094 passed, 0 failed, 20 skipped**, and the
sorted verdict list is **identical line for line** to the base's
(sha256 `b97c0e91…`). Why: no case runs the compiler (a case runs a
binary built ahead of time), and 0.2.18 changes what compiles, plus the
checked machine's store order (#452), which no native binary reaches.
**Falsifier:** any verdict line that moves.

**3c. Peak memory.** Nothing in 0.2.18 adds a copy or an allocation to
a program 0.2.17 accepted (#460/#464 only refuse; #452 moves the checked
machine only). Predicted: **every one of the 21 utilities' peak RSS at
the pin is within max(5 %, 2 MB) of its base (0.2.17) median**, on
kasumi with `/usr/bin/time -o … -f %M`, each value asserted non-empty
and numeric before any comparison, three rounds with the two states
interleaved, 64 MiB of generated text (seed 9, bu09's generator) where a
utility reads input, `LC_ALL=C`. **Falsifier:** any utility outside the
band.

## 4. Evidence index

All measurement on kasumi (CachyOS, x86_64, 16 cores), logs under
`~/lanes/bu10/`. Three trees, each a fresh clone of origin: **base** =
trunk `74069bd` at 0.2.17 / 0.1.40 / std `14f0ab2`; **pin** = `337f230`
(the pin commit, source unchanged) at 0.2.18 / 0.1.41 / std `14f0ab2`;
**head** = `c75bdd1` (the pin plus the README and `sink.lu` comments
restated at 0.2.18). Toolchains staged by `tools/fetch-toolchain` from
`~/lanes/bu10/arch/`, each archive digest-checked by the tool.

### 3a scored: the build

**Per utility, `--release --deny-warnings --error-limit=0`**
(`~/lanes/bu10/probe.sh`, `pin-probe.txt`, one log per utility in
`pin-probe/`): identity `wolf 0.2.18 (wolfgang, pin ec56a08)`, std
`14f0ab2c6a64e86240113e21c4da9f746380eb29`, the flag present, and **all
21 utilities `rc=0 errors=0 warnings=0`**. std `14f0ab2` compiles under
0.2.18 (every utility reaches `std.env`). **0.2.18 refuses no site in
boreutils; there is nothing to fix.**

Then `tools/build` + `tools/check-test` + `tools/check-fmt` at pin and at
head: 21 built, `wolf test: 1 passed`, fmt clean, `BUILD_EXIT=0`
(`pin-build.log`, `head-build.log`).

**The zero was seen to fire** (`~/lanes/bu10/plant.sh`, `plant.txt`):
the 0.2.18 CHANGELOG's two witnesses, each alone in its directory, built
by the same command and counted by the same `grep -cE '^error'`:

| witness | 0.2.17, plain | 0.2.17, `--deny-warnings` | 0.2.18, plain | 0.2.18, `--deny-warnings` |
|---|---|---|---|---|
| #464 (`var t = move xs` from a `mut` param) | rc 0, W1002, **prints `2`** | rc 2, `error[W1002]` | rc 2, **`error[E1001]` `xs` may return to the caller with its value moved away** | rc 2, `error[W1002]` only |
| #460 (`move xs[0]`; `xs[1] = [5]`; read `xs[0]`) | rc 0, **prints `2 2 1`** | rc 0, prints `2 2 1` | rc 2, **`error[E1001]` `xs[0].len` is used here after its value moved away** | rc 2, the same E1001 |

So the staged 0.2.18 carries both refusals and the probe's count sees
them; 21 zeros are a measurement, not a dark search.

**Found, not predicted, and filed: wolf-lang#469.** The last column's
#464 row is wrong in a way the CHANGELOG says was fixed: under
`--deny-warnings` 0.2.18 stops on W1002's "the body never writes it"
(promoted by `deny W1002`, help: "drop the `mut`") and **never reports
the E1001**; plain, it reports only the E1001, as the CHANGELOG says.
Nothing wrong is accepted (exit 2 either way). It matters here because
every boreutils build denies warnings: had a helper moved out of a
`mut` parameter, this repo would have been told to drop the `mut`.
Logs: `plant/w464/0.2.18-deny.log`, `plant/w464/0.2.18-plain.log`.

### 3b scored: the difftest

| tree | answer | sorted verdict list (2,114 lines) sha256 | log |
|---|---|---|---|
| base `74069bd` @0.2.17 | `difftest: 2094 passed, 0 failed, 20 skipped` | `b97c0e91b8d20373…` | `base-difftest.log` |
| pin `337f230` @0.2.18 | `difftest: 2094 passed, 0 failed, 20 skipped` | `b97c0e91b8d20373…` | `pin-difftest.log` |
| head `c75bdd1` @0.2.18 | `difftest: 2094 passed, 0 failed, 20 skipped` | `b97c0e91b8d20373…` | `head-difftest.log` |

The verdict list is every `ok` / `FAIL` / `SKIP` line, sorted
(`base-verdicts.txt`, `pin-verdicts.txt`, `head-verdicts.txt`);
`diff base-verdicts.txt pin-verdicts.txt` and `diff pin-verdicts.txt
head-verdicts.txt` both print nothing, and the full digest,
`b97c0e91b8d203737eb42c10234517f2ffbcdb7e6d0ba1b70e185b8a3dfc5817`, is
bu09's at all four of its states too. **The comparison was seen to
fire**: base's list with its first line dropped (`fire-check.txt`)
diffs against pin as `0a1 > ok   basename: a backslash operand in the
diagnostic`, exit 1. Each run asserted the oracle (`GNU coreutils
9.11`, `LC_ALL=C _POSIX2_VERSION=200112`, the `uniq +1 /dev/null` probe
OK). The binaries under test are not base's: every one of the 21
digests differs between base and pin (`rss-bins-base.txt`,
`rss-bins-pin.txt`).

### 3c scored: peak RSS

`~/lanes/bu10/rss.sh`, raw lines `rss-raw.txt` (`state util KB rc`, 126
lines, **0 `EMPTY`**; `/usr/bin/time` writes through `-o` and each value
is refused unless numeric). Three rounds, base and pin interleaved in
each, 64 MiB of generated text (`in.txt`, 67,108,907 bytes, sha256
`73c1f166…`, bu09's generator with seed 9, deleted after). `false`
exits 1 and `yes` 124 (bounded by `timeout 2`, so its `%M` is the
larger of `timeout` and `yes`) by design; every other run exits 0.
Load average 1.7 at the start (another owner's work), which the
interleaving is for.

| utility | workload | base KB | pin KB | pin vs base (median) |
|---|---|---|---|---|
| true | `--version` | 2372 2488 2396 | 2508 2500 2440 | +4.3 % (104 KB) |
| false | `--version` | 2348 2520 2460 | 2368 2372 2428 | −3.6 % (88 KB) |
| echo | 1,000 operands | 2596 2648 2520 | 2524 2484 2640 | −2.8 % |
| basename | a path, a suffix | 2440 2444 2480 | 2352 2492 2448 | +0.2 % |
| dirname | a path | 2416 2432 2416 | 2428 2436 2476 | +0.8 % |
| yes | 2 s to `/dev/null` | 2404 2372 2356 | 2408 2352 2368 | −0.2 % |
| cat | file | 2764 2792 2832 | 2828 2828 2740 | +1.3 % |
| cut | `-f1,3` file | 4076 4008 4108 | 4088 4128 4120 | +1.1 % |
| head | `-n 100000` file | 2928 2876 2996 | 2960 2948 2960 | +1.1 % |
| tail | `-n 100000` file | 36168 36148 36084 | 36180 36024 36068 | −0.2 % |
| nl | file | 12344 12292 13212 | 12388 12332 12332 | −0.1 % |
| seq | `1000000` | 3532 3568 3544 | 3624 3648 3552 | +2.3 % |
| uniq | file | 6196 6284 6336 | 6208 6252 6368 | −0.5 % |
| wc | file | 4256 4376 4256 | 4440 4372 4416 | +3.8 % (160 KB) |
| tr | `a-z A-Z` < file | 6892 6856 6876 | 6836 6976 6900 | +0.3 % |
| tac | file | 200516 200672 200668 | 201208 200692 201352 | +0.3 % |
| paste | file file | 4592 4544 4504 | 4536 4532 4524 | −0.3 % |
| fold | `-w 40` file | 4456 4536 4440 | 4564 4520 4552 | +2.2 % |
| expand | file | 3668 3648 3776 | 3784 3736 3764 | +2.6 % |
| unexpand | `-a` file | 3344 3328 3248 | 3336 3348 3236 | +0.2 % |
| sort | `-S 10M -T` file | 43716 44052 43824 | 43476 43404 43700 | −0.8 % |

**Every utility is inside max(5 %, 2 MB). 3c held.** The largest
relative move, `true`'s +4.3 %, is 104 KB on a 2.4 MB process, inside
its own spread across rounds (2372–2488 at base).

### Predictions, scored

| prediction | result |
|---|---|
| 3a: std `14f0ab2` and all 21 utilities build at 0.2.18 with zero diagnostics | **held** (21 × `rc=0 errors=0 warnings=0`; the count seen to fire on both witnesses) |
| 3a: `wolf test` 1 passed, `wolf fmt --check` clean | **held** at pin and head |
| 3b: verdict list identical, 2094/0/20 | **held** (base = pin = head, digest `b97c0e91…`) |
| 3c: peak RSS within band | **held** (21 of 21) |
| (not predicted) the diagnostic under `--deny-warnings` | a finding: #464's shape reports W1002, not E1001 (wolf-lang#469) |

### CI

A note cannot cite the run of the commit that carries it, so the CI
evidence at the head sha — run id, all three legs — is in the PR's
body, read with `gh run view`.

## 5. Done-when

- [ ] branch `bu10` on origin; this note's §1–§3 the branch's first commit
- [ ] pin: `wolf-toolchain.toml` at 0.2.18 / 0.1.41 / std `14f0ab2`,
      three digests per half, in its own commit
- [ ] every utility built at the pin with the diagnostic count cited
      (kasumi log); any refused site named and fixed
- [ ] difftest verdict lists: base = pin (= head, if a fix lands); diff
      empty, cited, and the comparison seen to fire
- [ ] peak RSS table: base / pin beside §3c
- [ ] PR open, unmerged; CI green on all three legs at the head sha
      (`gh run view`)
- [ ] §2 drift reported; five sections; kasumi build dirs pruned;
      worktree gone; no orphan pids
