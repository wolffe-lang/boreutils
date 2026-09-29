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

*(Written after the measurement.)*

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
