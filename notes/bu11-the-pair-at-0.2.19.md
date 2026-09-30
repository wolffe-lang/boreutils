# bu11 — the pair at 0.2.19

Lane note and contract. **Class:** small (boreutils), **Opus**. **Wave:**
52. One oracle: the differential against GNU 9.11, before and after, by
verdict list. One deliverable: the pin at wolf 0.2.19 / lupin 0.1.42,
every site that names the pin moved, and any new diagnostic or
behaviour change fixed here or reported. Template: bu10's contract
(`notes/bu10-the-pair-at-0.2.18.md`).

§1, §2 and §3 were written 2026-09-30, after the base was measured at
0.2.18 and before any build, difftest or memory measurement at 0.2.19.

## 1. Forbidden, absolutely

- No `rm` outside `~/lanes/bu11/` on kasumi and `/private/tmp/bu11`; no
  deletion in any tree this lane did not create; never another owner's
  target dir.
- No `git add -A`; no edit to another lane's file; no `~/.claude`.
- No build on nomad-1: every build, difftest, RSS and bench run is on
  kasumi, `CARGO_BUILD_JOBS=4`.
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

## 2. Inputs, re-derived against origin (2026-09-30)

| the contract says | origin says | verdict |
|---|---|---|
| boreutils trunk `d7909754` (bu10) | `d790975`, "notes: say where bu10's member lists went"; trunk push run 36505228346 success | holds |
| pins today | `wolf-toolchain.toml`: wolf 0.2.18 `ec56a08f`, lupin 0.1.41 `0cfc0cfc`, std `14f0ab2` | holds |
| wolf **0.2.19**, release 400208356 | tag `v0.2.19` (a tag object, `ba0b43a7`) → commit `c2401f05f37794a078d2acf62f837dad98e5950d`; release 400208356, not a draft, not a prerelease, four assets | holds |
| lupin **0.1.42**, release 400022505 | tag `v0.1.42` (a tag object) → commit `8e2516dc47bf808512388cc687e070981d331d98`; release 400022505, not a draft, not a prerelease, five assets | holds |
| the pairing | 0.2.19's `CHANGELOG.md` and the archive's `--version` line 2: "paired with lupin 0.1.42 (reference interpreter), pin ec56a08" — lupin's spec pin is now wolf v0.2.18, one release behind, not two | holds |
| the std pin, re-derived against 0.2.19 first (B151) | wolf-std trunk IS `14f0ab2` (compare `14f0ab2...trunk`: ahead 0, behind 0), so there is one candidate; whether it compiles under 0.2.19 is §3a's measurement | one candidate; measured in §3a |
| boreutils at trunk, 0.2.18 | kasumi, `run-state.sh base` at `d790975`: 21 built, `wolf test: 1 passed`, fmt clean, `BUILD_EXIT=0`; **`difftest: 2094 passed, 0 failed, 20 skipped`**, oracle asserted (`GNU coreutils 9.11`, `LC_ALL=C _POSIX2_VERSION=200112`, the `uniq +1 /dev/null` probe OK). Sorted verdict list 2,114 lines, sha256 `b97c0e91b8d203737eb42c10234517f2ffbcdb7e6d0ba1b70e185b8a3dfc5817` — **bu10's and bu09's digest**. `probe.sh base` at 0.2.18: 21 × `rc=0 errors=0 warnings=0` (`~/lanes/bu11/base-build.log`, `base-difftest.log`, `base-verdicts.txt`, `base-probe.txt`) | holds |

### The archives, by digest

Downloaded from the two release pages on kasumi and hashed there
(`~/lanes/bu11/archives.sha256`); each equals the `digest` GitHub's
release API publishes for the asset. Windows is out of scope and not
pinned.

| archive | sha256 |
|---|---|
| wolf-0.2.19-aarch64-apple-darwin.tar.gz | `8e9a9653ec320b513c8f6c05c4969ea2f84dc2160718e8a2b62a0c234c2233b6` |
| wolf-0.2.19-x86_64-unknown-linux-gnu.tar.gz | `9f3873d80118681a583a7bc00ead8d00186d447d2584aea75bc65a81f8238c8e` |
| wolf-0.2.19-aarch64-unknown-linux-gnu.tar.gz | `dcb418a959a3034ac17ff3a9a82ccb7dabd72fd70f437d7011496a7e91e83b78` |
| lupin-0.1.42-aarch64-apple-darwin.tar.gz | `756d6498dc424c54f638974db9e561c91251ac1592531ee258942f5e7ec3da0a` |
| lupin-0.1.42-x86_64-unknown-linux-gnu.tar.gz | `9856335aacbb26d22bd3fde867f28238c6ffde98e5d9fc15ecdedf4103998ab6` |
| lupin-0.1.42-aarch64-unknown-linux-gnu.tar.gz | `0cb937ec29a8ea7957f98b3f7c3cbe29f72d8b2def461b23ca55fc9a6370416e` |

Members by name (`~/lanes/bu11/*.members`, one file per archive, kept
beside the logs rather than inside the extracted trees this time):

| member | darwin-arm64 | linux-x64 | linux-arm64 |
|---|---|---|---|
| `wolf` | `c8bc428b…` | `3821bfaa…` | `cc279286…` |
| `libwolf_rt.a` | `a72a0ec9…` | `f7e7236d…` | `def2d9db…` |
| `wolf-cimport-worker` | `5ae6c076…` | `65498b6a…` | `4c065ff8…` |
| `_wolf` (zsh completion) | `2d1e4801…` | `2d1e4801…` | `2d1e4801…` |
| `lupin` | `efc8d31c…` | `03f4a710…` | `e95e5f0b…` |

Identity lines, from the linux-x64 archives (`~/lanes/bu11/identity.txt`):
`wolf 0.2.19 (wolfgang, pin c2401f0)` / `paired with lupin 0.1.42
(reference interpreter), pin ec56a08` and `lupin 0.1.42 (wolf-interp,
reference interpreter at pin ec56a08)`.

### What 0.2.19 changes, and where it could land here

Read from 0.2.19's `CHANGELOG.md` ("Read this before you bump the pin")
and from `git diff --name-only v0.2.18 v0.2.19` in wolf-lang, outside
tests and corpus: `wolf_mem` (`lower.rs`, `place.rs`), `wolf_wir`
(`lower.rs`, a comment; `midend/inline.rs`), `wolf_driver` (`main.rs`,
`test_cmd.rs`, `PAIRING`), `wolf_diag`, `docs/`, `spec/`. **No runtime
source moved.**

- **Widenings only in the checker.** Two `mut` claims on two literal
  elements (EG2), a member read beside an element claim (#472, 1(c)),
  and `len`/`count`/`is_empty` beside a moved element (#474) now
  compile. The CHANGELOG names no program 0.2.18 compiled that 0.2.19
  refuses. `grep -rnE 'E10[0-9][0-9]' src` finds only E1010 comments
  (wolf-lang#418, open and untouched by this release), so no site here
  carries a workaround for a shape 0.2.19 now accepts.
- **#469** (`--deny-warnings` hid #464's E1001 behind a W1002), filed by
  bu10, is fixed (closed 2026-09-30T02:11:36Z). Every boreutils build
  denies warnings, and the base build has zero warnings, so the change
  can only show on a witness.
- **#470**: the release-tier inliner no longer splices a call whose two
  `mut` formals bind one caller region (`formals_share_a_region`). Such
  a splice ICEs on 0.2.18, and 0.2.18 built all 21 utilities, so no
  boreutils call was being spliced in that shape; the check can only
  keep out of line a call that was already out of line. Eight call
  lines in `src/` pass two `mut` arguments (a one-line grep:
  `cat.lu`:324, :356, :371, :373, :378, :383 — `show`, `end_line`,
  `number`; `paste.lu`:394, :481 — `next_line`), which is where it
  would show.
- The six README sentences and one `sink.lu` comment that say "wolf
  0.2.18 has no …" name wolf-lang#405, #407, #417, #426 and wolf-std
  F-0011 (wolf-lang#416). All five issues are OPEN today, and the
  0.2.18..0.2.19 diff adds no seek, splice, copy_file_range, errno or
  capacity surface (grep of the added lines).

### Drift, reported

1. **The task says "every site the pin names moves"; outside
   `wolf-toolchain.toml` the pin is named in seven prose sites** (README
   :66, :88, :272, :342, :526, :570; `src/bore/sink.lu`:6), each a claim
   about what wolf lacks. They move to 0.2.19 only because the claim was
   re-checked above; `src/seq.lu`:208 names 0.2.16 as history and stays.
2. The `lupin` line in `wolf-toolchain.toml` says "the `rev` below is
   the commit the 0.1.40 TAG names" while pinning 0.1.41 — a stale
   comment from bu10; corrected with the pin.
3. None in the numbers: every other input above held.

## 3. Prediction, committed before any build at 0.2.19

**3a. The build.** At 0.2.19 / 0.1.42 / std `14f0ab2`, source unchanged:
- std `14f0ab2` compiles, and **all 21 utilities build under
  `--release --deny-warnings --error-limit=0` with zero diagnostics**.
- `wolf test` 1 passed; `wolf fmt --check` clean.
- **Falsifier:** any diagnostic in any utility or in std. A refused
  site is fixed in its own commit, named with file:line and its
  diagnostic, and seen compiling after; a behaviour change is reported.
- **The zero is seen to fire** on witnesses built by the same command
  and counted by the same grep: bu10's #464 witness under
  `--deny-warnings` reports **E1001** at 0.2.19 (W1002 at 0.2.18, #469);
  `swap(mut xs[0], mut xs[1])` is E1002 at 0.2.18 and builds at 0.2.19;
  the CHANGELOG's #470 witness ICEs at 0.2.18 release and prints `2 12`
  at 0.2.19.

**3b. The difftest.** **2094 passed, 0 failed, 20 skipped**, the sorted
verdict list **identical line for line** to the base's (sha256
`b97c0e91…`). No case runs the compiler, and 0.2.19 changes what
compiles and one inlining decision that §2 argues no boreutils call
reaches. **Falsifier:** any verdict line that moves.

**3c. Peak memory.** Every one of the 21 utilities' peak RSS at the pin
within **max(5 %, 2 MB)** of its base (0.2.18) median; bu10's
instrument (`/usr/bin/time -o … -f %M`, non-empty and numeric asserted,
three rounds, states interleaved, 64 MiB seed-9 text, `LC_ALL=C`).
**Falsifier:** any utility outside the band.

**3d. The #470 sites.** The two utilities whose calls pass two `mut`
arguments run at the speed they ran at 0.2.18: `cat -A`, `cat -n` and
`paste f f` on the 64 MiB input, `hyperfine --warmup 2 --runs 10`, base
and pin alternated, **pin mean within ±5 % of base mean** for each.
**Falsifier:** any of the three outside ±5 % in two consecutive
measurements (one is noise on a shared host).

## 4. Evidence index

*(written after the measurement)*

## 5. Done-when

- [ ] branch `bu11` on origin; this note's §1–§3 the branch's first commit
- [ ] pin: `wolf-toolchain.toml` at 0.2.19 / 0.1.42 / std `14f0ab2`,
      three digests per half, in its own commit
- [ ] every prose site naming 0.2.18 re-checked and moved
- [ ] every utility built at the pin with the diagnostic count cited
      (kasumi log), the count seen to fire; any refused site fixed
- [ ] difftest verdict lists: base = pin = head; diff empty, cited, and
      the comparison seen to fire
- [ ] peak RSS and the #470-site bench beside §3c and §3d
- [ ] PR open, unmerged; CI green on all three legs at the head sha
      (`gh run view`)
- [ ] §2 drift reported; five sections; kasumi build dirs pruned;
      worktree gone; no orphan pids
