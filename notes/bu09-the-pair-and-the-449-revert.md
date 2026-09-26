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

All measurement on kasumi (CachyOS, x86_64, 16 cores, load under 0.1 at
the start), logs under `~/lanes/bu09/`. Three trees, each a clone of
origin: **base** = trunk `aa37bb9` at 0.2.16 / 0.1.38 / std `070884c`;
**pin** = `fd8950c` (the pin commit, source unchanged) at 0.2.17 /
0.1.40 / std `14f0ab2`; **head** = `96a939f` (every revert, plus the
README and sink comment restated at 0.2.17). The head difftest also ran
at `8f5fd33`, the last source-changing commit, with the same answer.

### 3a and 3b scored: the difftest

| tree | answer | sorted verdict list (2,114 lines) sha256 | log |
|---|---|---|---|
| base `aa37bb9` | `difftest: 2094 passed, 0 failed, 20 skipped` | `b97c0e91b8d20373…` | `base-difftest.log` |
| pin `fd8950c` | `difftest: 2094 passed, 0 failed, 20 skipped` | `b97c0e91b8d20373…` | `pin-difftest.log` |
| head `8f5fd33` | `difftest: 2094 passed, 0 failed, 20 skipped` | `b97c0e91b8d20373…` | `head-8f5fd33-difftest.log` |
| head `96a939f` | `difftest: 2094 passed, 0 failed, 20 skipped` | `b97c0e91b8d20373…` | `head-difftest.log` |

The verdict list is every `ok` / `FAIL` / `SKIP` line, sorted
(`*-verdicts.txt`); `diff base-verdicts.txt pin-verdicts.txt` and
`diff pin-verdicts.txt head-verdicts.txt` both print nothing, and the
full digest is `b97c0e91b8d203737eb42c10234517f2ffbcdb7e6d0ba1b70e185b8a3dfc5817`
for all four. **The comparison was seen to fire**: the base list with
its first line dropped diffs against head as `0a1 > ok   basename: a
backslash operand in the diagnostic`. Each run asserted the oracle
(`GNU coreutils 9.11`, `LC_ALL=C _POSIX2_VERSION=200112`, the `uniq +1
/dev/null` probe OK). **3a held; 3b's difftest half held.**

### 3b scored: every site seen compiling, and seen refused at 0.2.16

**At 0.2.17, every commit builds all 21 utilities** under
`--deny-warnings` — built one commit at a time from a clean `target/`,
`~/lanes/bu09/percommit.txt`, one line per commit (`sha ok built errors`):

| commit | built | errors | site(s) |
|---|---|---|---|
| `fdf0191` | 21 | 0 | 3, 4 |
| `d379096` | 21 | 0 | 5 |
| `51c2a27` | 21 | 0 | 6, 7 |
| `295114b` | 21 | 0 | 8 |
| `4e3a360` | 21 | 0 | 9–11 |
| `f0a62db` | 21 | 0 | 12 |
| `56b4a01` | 21 | 0 | 13–14 |
| `85c91db` | 21 | 0 | 15 |
| `725e56e` | 21 | 0 | 16 |
| `1decc4e` | 21 | 0 | 17 |
| `eb1dc25` | 21 | 0 | 18 |
| `a402a5e` | 21 | 0 | 19 |
| `69849bc` | 21 | 0 | 20 |
| `b2e9087` | 21 | 0 | 21 |
| `bb62ff3` | 21 | 0 | 1, 2 |
| `8f5fd33` | 21 | 0 | `put_last` / `finish_last` deleted |

and head `96a939f`: 21 built, `wolf test: 1 passed`, `wolf fmt --check`
clean, `BUILD_EXIT=0` (`head-build.log`).

**The control: head's source under the 0.2.16 archive** (the same
`wolf` binary and std tree as base, `WOLF_STD` set, `--release
--deny-warnings`, `~/lanes/bu09/red216/`). All 21 utilities are refused,
exit 2, **every error E1002 and nothing else**
(`red216-summary.txt`). The distinct locations, which are where 0.2.16
put the claim it misread:

| location | inventory site |
|---|---|
| `bore/bore.lu` :536, :538, :557, :562, :564, :568, :572, :575 (in all 21) | 1, 2 |
| `true.lu:24`, `false.lu:24` | 3, 4 |
| `uniq.lu:478` | 5 |
| `wc.lu:597`, `wc.lu:943` | 6, 7 |
| `echo.lu` :35, :36, :39, :40 | 8 |
| `tr.lu:437`, `tr.lu:443` | 9–11 |
| `tac.lu:327`, `tac.lu:330` (`` `sink` goes `mut` … while `sink` is lent ``) | 19 |
| `paste.lu` :399, :404, :415 | 13, 18, 20 |

Sites 12 and 14 (`tac`'s `finish`, `paste`'s second `finish`) are not
separately visible: 0.2.16 names the claim it misread, and in those two
functions the claims it names are the sink's.

So the natural shape is refused at 0.2.16 and accepted at 0.2.17 for
bu07's eleven and for the sink family: **the revert and the fix are
seen red and green on the same source.** And one thing the control
shows that §2 did not predict: **`fold`, `expand`, `unexpand` (sites
15–17) and `sort`'s `merge_pass` (site 21) draw no E1002 of their own
at 0.2.16** — those four followed the writer-last convention, not a
refusal. They are reverted all the same, because the convention was
#449's and its comments said so.

`git grep '#449' aa37bb9 -- src` finds 24 lines in 14 files; the same
pattern over head's `src` finds none, and `git grep -n
'put_last\|finish_last' -- src` is empty.

### 3c scored: peak RSS

`~/lanes/bu09/rss.sh`, raw lines `rss-raw.txt` (`state util KB rc`, 108
lines, none empty — the first attempt's `2>/dev/null` swallowed
`/usr/bin/time`'s own report and printed nothing, so it now writes
through `-o` and refuses an empty value before any comparison). Three
rounds, the three states interleaved in each round, 64 MiB of generated
text (`in.txt`, 67,108,907 bytes, seed 9, deleted after).

| utility | workload | base KB | pin KB | head KB | head vs base (median) |
|---|---|---|---|---|---|
| true | `--version` | 2336 2524 2456 | 2448 2404 2368 | 2520 2492 2532 | +2.6 % |
| false | `--version` | 2360 2436 2528 | 2332 2528 2540 | 2488 2456 2516 | +2.1 % |
| echo | 1,000 operands | 2620 2668 2544 | 2500 2612 2644 | 2484 2488 2620 | −5.0 % (132 KB) |
| uniq | file | 6256 6328 6316 | 6320 6336 6264 | 6224 6316 6212 | −1.5 % |
| wc | file | 4416 4448 4384 | 4408 4392 4400 | 4336 4296 4416 | −1.8 % |
| tr | `a-z A-Z` < file | 7004 6976 6856 | 6844 6836 6856 | 6952 6928 6828 | −0.7 % |
| tac | file | 201152 201048 201188 | 201064 199428 200572 | 199608 201184 199680 | −0.7 % |
| paste | file file | 4536 4532 4488 | 4536 4536 4536 | 4484 4500 4524 | −0.7 % |
| fold | `-w 40` file | 4536 4540 4488 | 4484 4400 4536 | 4500 4508 4404 | −0.8 % |
| expand | file | 3732 3772 3804 | 3756 3756 3772 | 3500 3772 3788 | 0.0 % |
| unexpand | `-a` file | 3364 3336 3264 | 3256 3332 3272 | 3312 3320 3372 | −0.5 % |
| sort | `-S 10M -T` file | 43868 46752 44204 | 42988 44204 44236 | 46696 43624 42404 | −1.3 % |

**Every utility is inside max(5 %, 2 MB) between every pair of
states. 3c held.** The largest relative move, `echo`'s −5.0 %, is
132 KB on a 2.5 MB process, inside its own spread across rounds.

### Predictions, scored

| prediction | result |
|---|---|
| 3a: pin alone, verdict list identical, 2094/0/20 | **held** |
| 3a: #438 adds no copy (no non-`Copy` place is index-stored) | **held** by the RSS table (pin within band of base everywhere); not separately instrumented |
| 3b: every site compiles in its natural shape at 0.2.17 | **held** (16 commits × 21 utilities) |
| 3b: verdict list identical after the revert | **held** |
| 3c: peak RSS within band at every step | **held** (12 of 12) |
| (not predicted) which inventory sites 0.2.16 actually refused | a finding: four of the inherited sites (15, 16, 17, 21) never were; §2 called them convention, and the control confirms it |

### CI

A note cannot cite the run of the commit that carries it, so the CI
evidence at the head sha — run id, all three legs — is in PR #14's
body, read with `gh run view`. The code head `96a939f` ran as
36276407921.

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
