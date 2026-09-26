# bu09 — the pair, and the #449 revert

Lane note and contract. **Class:** small (boreutils), **Opus**. **Wave:**
48. One oracle: the differential against GNU 9.11, before and after, by
verdict list. One deliverable: the pin at wolf 0.2.17 / lupin 0.1.40, and
every wolf-lang#449 workaround back in its natural shape with
`bore.put_last` / `bore.finish_last` deleted. Template: bu07's contract.

§1, §2 and §3 were written 2026-09-26, before a line of `src/` moved and
before any utility was measured for memory at either pin.

## 1. Forbidden, absolutely

- No `rm` outside `~/lanes/bu09/` on kasumi and `/private/tmp/bu09`; no
  deletion in any tree this lane did not create; never another owner's
  target dir.
- No `git add -A`; no edit to another lane's file; no `~/.claude`.
- No build on nomad-1: every build, difftest and bench runs on kasumi.
- No merge, no rebase-merge; no `2>/dev/null` on a checkout.
- No "seen red" or "seen compiling" without a run id, sha, log path or
  digest in the same paragraph.
- The pin comes from the RELEASE ARCHIVE by digest, never a clone or
  `~/.local/bin`; every member hashed by name (`_wolf` is the zsh
  completion script and hashes the same at every pin).
- Never read, copy or translate GNU coreutils source (the licence rule).
- Kill only this lane's own pids, never a pattern or a process group.
- No commit or PR trailers of any kind.
- A site that does not compile in its natural shape at 0.2.17 stays
  worked around and is reported; it is never forced.

## 2. Inputs, re-derived against origin (2026-09-26)

| the contract says | origin says | verdict |
|---|---|---|
| boreutils trunk (bu08) | `aa37bb9`, "README: the seventeen macOS-only skips are all /dev/full, diffed" | holds |
| pins today | `wolf-toolchain.toml`: wolf 0.2.16 `93a5fe50`, lupin 0.1.38 `ba357aa`, std `070884c` | holds |
| wolf **0.2.17** = `02afce84`, release 397045016 | tag `v0.2.17` → tag object `4da2f151` → commit `02afce84f05c7841856a10671b6d7924f79193cc`; release 397045016, not a draft, four assets | holds |
| lupin **0.1.40** = `54f85e6`, release 397033025 | tag `v0.1.40` → tag object `e9f76ec1` → commit `54f85e694d4c03e5cd40bef461f85ca0ac373332`; release 397033025, not a draft, five assets | holds |
| wolf-lang#449 is fixed in 0.2.17 | #449 CLOSED 2026-09-24T07:15:53Z; s178's `a565d4b9` is an ancestor of `v0.2.17` (compare: ahead 61, behind 0); the 0.2.17 CHANGELOG's "Read this before you bump the pin" says "Both downstreams' workarounds can be reverted under #449" | holds |
| the #449 witness | bu07's witness (`notes/bu07-…md` §1) built on kasumi: 0.2.16 archive → `error[E1002]: \`out\` goes \`mut\` in a call evaluated while \`out\` is lent \`mut\``; 0.2.17 archive → builds, prints `2` (`~/lanes/bu09/w449/`) | holds |
| boreutils at trunk, 0.2.16 | kasumi, `tools/build` + `tools/check-test` + `tools/difftest` at `aa37bb9`: 21 utilities, `wolf test: 1 passed`, **`difftest: 2094 passed, 0 failed, 20 skipped`** (`~/lanes/bu09/base-difftest.log`) | holds (2,114 cases, bu08's count) |

### The archives, by digest

Downloaded from the two release pages on kasumi and hashed there
(`~/lanes/bu09/arch/`); each equals the digest GitHub's release API
publishes for the asset.

| archive | sha256 |
|---|---|
| wolf-0.2.17-aarch64-apple-darwin.tar.gz | `525c91431bf91ed0db5caa5b19819513b16168ca0811ba75e4a28f5bac7ebc53` |
| wolf-0.2.17-x86_64-unknown-linux-gnu.tar.gz | `a95d0f0f8fe384fdb70047bb893c857573cc62dd10b2967ab7788fc9a8ce24ce` |
| wolf-0.2.17-aarch64-unknown-linux-gnu.tar.gz | `d3d2262352fc1d0bd343428c518c3ead69d7cb8bcd2c728d090096c220991420` |
| lupin-0.1.40-aarch64-apple-darwin.tar.gz | `197f19573bb19a8e21f06431451279959784c70a7195d9d98244dcd4b721c034` |
| lupin-0.1.40-x86_64-unknown-linux-gnu.tar.gz | `509929e67b7ae97463973d6bb7c61b9f93dc47a523957055def816c56fb23384` |
| lupin-0.1.40-aarch64-unknown-linux-gnu.tar.gz | `c6a9b30f53cbff0883cf5afb1b09d87ebc9dabd7ec5a531ccb9b18e1064c2996` |

Members by name (the executables; the rest are text):

| member | darwin-arm64 | linux-x64 | linux-arm64 |
|---|---|---|---|
| `wolf` | `8a29fd89…` | `5cdd936e…` | `a1ef6647…` |
| `libwolf_rt.a` | `f5010f76…` | `c5384a5c…` | `d70e070c…` |
| `wolf-cimport-worker` | `f19b6895…` | `7031dd13…` | `21e64ed3…` |
| `_wolf` (zsh completion) | `2d1e4801…` | `2d1e4801…` | `2d1e4801…` |
| `lupin` | `65180b7b…` | `18d64444…` | `f161e5fc…` |

`_wolf` hashes `2d1e48018333…` in all three, as at 0.2.16 — the
cross-check that the member table is of one build, and the reason no
check may read "the first binary it finds". Identity lines, from the
linux-x64 archives: `wolf 0.2.17 (wolfgang, pin 02afce8)` / `paired with
lupin 0.1.40 (reference interpreter), pin 93a5fe5` and `lupin 0.1.40
(wolf-interp, reference interpreter at pin 93a5fe5)`.

### The std pin, re-derived against 0.2.17 first (B151)

Both candidates built on kasumi against the 0.2.17 / 0.1.40 archives,
trunk source unchanged, `--deny-warnings`:

| std rev | what it is | result |
|---|---|---|
| `070884c` | today's pin | 21/21 utilities build (`~/lanes/bu09/probe-std070884c.log`) |
| `14f0ab2` | wolf-std trunk (sc52b), ws42's pin | 21/21 build, `wolf test` 1 passed, `wolf fmt --check` clean (`~/lanes/bu09/probe-std14f0ab2.log`, `probe-fmt.log`) |

`070884c..14f0ab2` is 12 commits and touches exactly one file under
`std/`: `std/map/map.lu` (B117, `map.remove`). boreutils imports
`std.env` and `std.time` and nothing else. **The pin moves to
`14f0ab2`**: it compiles, it is the tree the other downstream (ws42) pins
in this wave, and the one `std/` file that differs is one no utility
reaches.

### Drift, reported

1. **"12 #449 workaround sites" is bu07's count, and it is twelve with
   one of them not a workaround.** bu07's note: "twelve sites in seven of
   the fifteen existing utilities … One of the twelve was a real find and
   is FIXED rather than worked around: `src/seq.lu:208`" (a `read`
   parameter returned, wolf-lang#366's `return copy d`). That one is
   correct code under the rule and **stays**. The workaround commits
   (`0ddd0fa`, `feea11b`, `3068bd2`, `e7ebf30`, `975720f`, `e02b5a8`,
   `812abcd`) change **eleven** call sites.
2. **Trunk carries more #449 shapes than bu07 filed**, because bu07's
   five later utilities and bu08's `sort` were written after the filing
   and took the writer-last shape by convention, each naming #449. Every
   one is listed below as the inventory; deleting `finish_last` alone
   forces six of them.
3. The 0.2.17 CHANGELOG repeats "12 sites in 7 of its 15 utilities" —
   the same count, with the same caveat.
4. lupin 0.1.40's own pin is `93a5fe5` (wolf v0.2.16), not 0.2.17; that
   is the pairing the release declares and is recorded, not a defect.

### The inventory (every #449 shape at `aa37bb9`)

A **site** is a call written in the #449 shape. A signature reordered for
#449 is listed with its calls.

*bu07's eleven:*

| # | file | site | natural shape |
|---|---|---|---|
| 1 | `bore/bore.lu` | `single_quoted`: closing `'` pushed as a byte | `push_str(mut out, "'")` |
| 2 | `bore/bore.lu` | `spliced`: the same | `push_str(mut out, "'")` |
| 3 | `true.lu` | `finish_last` | `bore.finish(mut out, "true", status)` |
| 4 | `false.lu` | `finish_last` | `bore.finish(mut out, "false", status)` |
| 5 | `uniq.lu` | `finish_last` (help/version) | `bore.finish(mut h, "uniq", 0)` |
| 6 | `wc.lu` | `emit`: `put_last("\n", …)` | `bore.put(mut out, "\n")` |
| 7 | `wc.lu` | `main`: `finish_last` | `bore.finish(mut out, "wc", status)` |
| 8 | `echo.lu` | `write_args(args, posix, mut out)` + signature | `write_args(mut out, args, posix)` |
| 9–11 | `tr.lu` | `push_item(…, mut sp)` ×3 + signature | `push_item(mut sp, kind, a, b)` |

*Inherited after the filing:*

| # | file | site | natural shape |
|---|---|---|---|
| 12 | `tac.lu` | `finish_last` | `bore.finish(mut out, …)` |
| 13–14 | `paste.lu` | `finish_last` ×2 | the same |
| 15 | `fold.lu` | `finish_last` | the same |
| 16 | `expand.lu` | `finish_last` | the same |
| 17 | `unexpand.lu` | `finish_last` | the same |
| 18 | `bore/sink.lu` | `sink_push` / `sink_done` take the sink last; 8 calls in `tac` and `paste` | the sink first |
| 19 | `tac.lu` | `one`, `reverse`, `put_range` take the sink last; 6 calls | the sink first |
| 20 | `paste.lu` | `put_delim`, `put_field` take the sink last; 4 calls | the sink first |
| 21 | `sort.lu` | `merge_pass` takes `dst` last; 2 calls | `dst` first |

and the two spellings themselves, `bore.put_last` and `bore.finish_last`,
deleted. The natural shape is fixed by one rule, which is what every
pre-#449 original in `0ddd0fa`…`812abcd` shows: **the `mut` parameter
first, the others in their existing order.** Comments that named #449
go with their sites.

## 3. Prediction, committed before the bump and before any revert

**3a. The pin alone (0.2.17 / 0.1.40 / std `14f0ab2`, source unchanged).**
Measured above only for *building*; nothing was difftested or
memory-measured at the new pin before this commit.
- The difftest answers **2094 passed, 0 failed, 20 skipped**, and the
  per-case verdict list is **identical line for line** to the base's.
  Why: no case runs the compiler (a case runs a binary built ahead of
  time), and nothing in 0.2.17 changes a printed byte of a program
  0.2.16 accepted — #449 and #431 widen what compiles; #438's index
  store copies only where the right-hand side is a non-`Copy` *place*.
- **#438 costs boreutils nothing.** Every single-line index store in
  `src/` (`grep -rnE '^\s*[A-Za-z_.]+\[[^]]+\]\s*=[^=]' src`, 47 hits)
  stores a byte, an int, a bool, an existing `copy`, a call's result or
  a struct literal (a temporary, stored as is). None stores a non-`Copy` place,
  so no deep copy is added anywhere.
- **Falsifier:** any case whose verdict moves; any utility whose peak
  RSS moves outside the band in 3c.

**3b. The revert (21 sites, both spellings deleted).**
- **Every site compiles in its natural shape at 0.2.17** under
  `--deny-warnings`. Falsifier: any E1002 (or any error) at a reverted
  site — which would mean #449's fix does not cover that shape, and the
  site stays worked around and is filed.
- The difftest verdict list is **identical line for line** to 3a's and
  to the base's: 2094 / 0 / 20. Argument order and a one-byte push
  versus a one-byte `push_str` change no output.
- `wolf fmt --check` clean; `wolf test` 1 passed.

**3c. Peak memory.** Argument order allocates nothing, and a `push_str`
of one byte allocates nothing a `push` does not. Predicted: **every
affected utility's peak RSS at head is within max(5 %, 2 MB) of its
base (0.2.16) median, and within the same band of its pin-only
median**, measured on kasumi with `/usr/bin/time -f %M`, three runs
each, generated inputs (64 MiB of text where the utility reads input),
`LC_ALL=C`. Affected: the twelve utilities the inventory touches —
`true false echo uniq wc tr tac paste fold expand unexpand sort`.
**Falsifier:** any one outside the band, at either step.

## 4. Evidence index

Filled as the evidence lands.

## 5. Done-when

- [ ] branch `bu09` on origin; this note's §1–§3 the branch's first commit
- [ ] pin: `wolf-toolchain.toml` at 0.2.17 / 0.1.40 / std `14f0ab2`,
      three digests per half, in its own commit
- [ ] every inventory site reverted, each seen compiling (kasumi log
      cited); `put_last` / `finish_last` gone (`git grep` empty)
- [ ] difftest verdict lists: base = pin-only = head (diff empty, cited)
- [ ] peak RSS table: base / pin-only / head beside §3c
- [ ] PR open, unmerged; CI green on all three legs at the head sha
      (`gh run view`)
- [ ] §2 drift reported; five sections; kasumi build dirs pruned;
      worktree gone; no orphan pids
