# bu07 — the pin at 0.2.16, and the rest of B3

Lane note. Written 2026-09-24, before a line of `wolf-toolchain.toml`,
`gnu-oracle.toml` or `src/` moved.

## 2. Inputs, re-derived against origin (2026-09-24)

Every row was re-derived from the thing itself — origin, the GitHub
release API, the release archive, the case files — not copied from the
contract.

| the contract says | origin says | verdict |
|---|---|---|
| boreutils trunk `b8258ab` | `b8258abd9709277df8a5842821ef7f0ae2576d95`, `README: point the licence section at LICENSE-TRAINING-DATA` | holds |
| pins wolf **0.2.14** / lupin **0.1.36** | `wolf-toolchain.toml` `[wolf] version = "0.2.14"`, `[lupin] version = "0.1.36"` | holds |
| fifteen utilities landed | `src/*.lu` minus `bore/` and `bore_test.lu`: basename cat cut dirname echo false head nl seq tail tr true uniq wc yes — fifteen | holds |
| 1,288 differential cases | `grep -c '^\[\[case\]\]' tests/cases/*.toml` sums to **1,288** | holds |
| wolf **0.2.16** = tag `v0.2.16` = `93a5fe50` | annotated tag `014dc68c` dereferences to commit `93a5fe504593ca7642b78ba83b4986e7a03cfe71`; `wolf --version` line 1 from the archive is `wolf 0.2.16 (wolfgang, pin 93a5fe5)` | holds |
| release 395302343, four assets | `gh api repos/wolffe-lang/wolf-lang/releases/tags/v0.2.16` → `id 395302343`, draft false, assets darwin-arm64 / linux-arm64 / linux-x64 / windows-x64 | holds |
| darwin-arm64 `b0431056…`, linux-arm64 `fe1966a4…`, linux-x64 `84e30c05…` | downloaded and hashed: `b04310568d…`, `fe1966a42a…`, `84e30c05e5…` | holds |
| lupin **0.1.38** = `ba357aa`, release 393623352, five assets | annotated tag `a9f07425` → commit `ba357aa6a2e32040d4f089d2cefe05bab86c4f86`; `id 393623352`, draft false, five assets | holds |
| lupin pinned on the released line, `2e4ca769` an ancestor of v0.2.15 | `lupin --version` line 1 from the archive is `lupin 0.1.38 (wolf-interp, reference interpreter at pin 2e4ca76)` | holds |
| boreutils#10 CLOSED | closed | holds |
| B98 open; the `field` leg's `continue-on-error` hides a signal death | `.github/workflows/ci.yml` `field:` carries `continue-on-error: true`; BACKLOG B98 open | holds |
| B73 open; two 9.11 builds disagree on `tail +3` | `tests/cases/tail.toml:298` is the skipped case, `gnu-oracle.toml` `[oracle] version = "9.11"` and nothing else identifies a build | holds |

### Drift found, reported not absorbed

1. **`README.md` says "1,272 differential cases, 0 failing, 16
   skipped".** The tree holds **1,288 cases**; a run on kasumi at
   trunk and the old pin answers `1271 passed, 0 failed, 17 skipped`.
   Two things are wrong in one sentence: the headline calls the
   *passing* count the *case* count, so the sixteen (now seventeen)
   skips are subtracted from the corpus rather than named inside it,
   and the skip count is one release of the corpus stale. Both are
   the shape wave 46's §4 forbids — a figure with no artifact behind
   it. Corrected in this branch from a run, not from arithmetic, and
   the sentence is rewritten to state the corpus and the run
   separately so the next reader cannot repeat it.

2. **The contract's §2 does not mention `[std]`, and the pin has a
   third section.** `wolf-toolchain.toml` pins `wolf-std` by commit
   (`2d1021996da6cde7b14c41ee4ef9d10125182e13`, the same rev lobo
   pinned at ws35). wolf-std's trunk is 69 commits past it at
   `070884c`. **This lane does not move it**, and the reason is the
   contract's own shape: the deliverable is "the pin, BOTH halves",
   the two halves are the two release archives, and a bump that moves
   the compiler two releases and the standard library sixty-nine
   commits in one commit cannot say which half a red belongs to. The
   std rev is re-verified green against 0.2.16 rather than advanced.

3. **`gnu-oracle.toml`'s field table is stale in one cell.** It records
   "ubuntu-latest 9.4" as of 2026-09-18. That is still what the field
   leg reports (run ids in the report), so the cell holds — but the
   file dates it and nothing re-checks the date, which is the same
   drift shape B44 exists to prevent one level up. Item 2 below puts
   a machine-checked identity in its place.

## 3. Prediction, committed before the measurement

Written before the pin moved, before a differential case for the four
new utilities existed, and before `tools/bench` was run on any of them.

### 3a. Which existing cases move at 0.2.16

**Zero. Not one of the 1,288 existing cases changes its verdict, and
the exit-status change is the interesting half of the reason.**

`[conf.exit]` at s169 makes the *compiler* exit 2 for a rejected
program and 4 for a refusal, where it used to exit 1. That moves a
`run(exit=1)` fence in a conformance corpus. It cannot move a
boreutils case, because **no boreutils differential case ever runs the
compiler**: `tools/difftest` execs `target/release/<util>`, a native
binary built ahead of time by `tools/build`, and compares its status
against GNU's. The compiler's own exit status is observed exactly
once in this repository — by `tools/build`, through `set -eu`, where
any non-zero status fails the build identically. So the change is
invisible to the corpus by construction, and 2 rather than 1 from a
failed `tools/build` is the same red.

The other four movers are read the same way and none of them reaches a
case either: `move` on a `Copy` place recording the move (s177/#444) is
a *fix* for a silent wrong answer, and boreutils has exactly one
`move`-shaped site — it has none; `Scope`/`Proc[T]`, pools and
`handle T` (s170/s173) are surfaces no utility uses; the place model
(s168) is a spec clarification; `[type.list.lit.elem]` saying
`List[i32]` (s175) is about list *literals*, which this repository does
not use at all (lupin 0.1.36 refused them, so every list here is
`List[T]()` and pushes).

**The falsifier is one line.** If the difference between the before and
after `difftest` totals is anything but `0 passed / 0 failed / 0
skipped` at identical corpus content, the prediction is wrong, and the
report names every case that moved.

A second, weaker prediction: **`wolf fmt --check` and `--deny-warnings`
are where a two-release bump actually bites**, not the corpus. If
anything reds at the bump it is a new lint or a formatter change over
`src/`, and it will be visible before a single case runs.

### 3b. Per utility: case count and speed against GNU

Case counts are what this lane intends to write, each falsified by the
committed file.

| utility | predicted cases | predicted vs GNU, and why |
|---|---:|---|
| `tac` | 90–110 | **0.3x–0.6x** on a file. GNU seeks to the end and walks backwards; wolf 0.2.14 has no seek (wolf-lang#426), so `tac` reads the whole stream forward into memory and writes it back. That is the same wall `tail` hit, and `tac` cannot even use a bounded window: it owes the *whole* input reversed, so peak memory is the input, and this is the one utility in the set whose memory is NOT flat. Through a pipe GNU buffers the whole input too, and there I predict **0.6x–0.9x**. |
| `paste` | 80–100 | **0.5x–0.8x** serial (`-s`), **0.3x–0.6x** parallel. The parallel form reads N files a line at a time, which is N open streams and a line-assembly per output record; the per-byte work is a copy. |
| `fold` | 70–90 | **0.5x–0.9x** for `-b` (byte counting, a pure scan) and **0.25x–0.5x** for the default column mode, which has to interpret tab, backspace and carriage return per byte. `-s` (break at a space) adds a backwards scan per line and should be the worst row. |
| `expand` | 60–80 | **0.4x–0.7x**. Per-byte column arithmetic and a run of spaces written out; a tab-heavy input is the best case because one input byte becomes many output bytes and the loop amortizes. |
| `unexpand` | 60–80 | **0.3x–0.6x**, worse than `expand`, because it must buffer a run of blanks before deciding whether the run becomes a tab, and that decision is per blank rather than per tab. |

**Aggregate falsifier:** the four utilities together add **360–460**
cases. Fewer than 360 means the corpus is thinner than the transform
set's standard (`tr` alone has 146); more than 460 is not a failure but
is worth saying.

**Speed falsifier:** a measured ratio outside the band above is a wrong
prediction and is published as one. On the evidence of bu03 and bu04 —
where three of four `tr`/`seq`/`nl` predictions missed, and `seq`
missed in *both* directions — I expect at least one of these five bands
to be wrong. The one I am least sure of is `tac`: if GNU's pipe path
buffers to a temporary file rather than to memory, the pipe row could
go either way by an order of magnitude.

### 3c. B73 and B98, predicted

- **B73.** I expect to find that `gnu-oracle.toml` **can** carry a build
  identity for the *staged* oracle (the tarball is pinned by digest
  already, so a build from it is reproducible up to the toolchain that
  built it) and **cannot** carry one for a *host* oracle, which is
  where the disagreement actually lives: Homebrew's 9.11 and Arch's
  9.11 are two third-party builds of one tarball and neither publishes
  an identity boreutils could pin in advance. The prediction is
  therefore that the honest answer is **half a mechanism and half a
  stated reason**, not one or the other.
- **B98.** I expect a planted signal death on the `field` leg to be
  **invisible today**: `continue-on-error: true` turns the step's
  failure into an annotation and the job's conclusion into `success`,
  whatever the exit code was. The ruling is that a *signal* death is
  loud and a *verdict* difference is not, and the falsifier is that
  after the change the planted signal reds the leg while a planted
  verdict divergence still does not.

## What the lane did, in the order it happened

### 1. The pin, and the thing that stopped it

Both halves were taken from the RELEASE ARCHIVES by digest — never from
a clone, never from `~/.local/bin` — and every MEMBER of every archive
was hashed by name as well. The cross-check that the member hashes are
of one build is `_wolf`, the architecture-independent zsh completion
script, which hashes
`2d1e48018333e3dd70473b34dfc78723f91f71d44a3d95287b68ce85fbbc2221` in
all three wolf archives.

| archive | sha256 |
|---|---|
| `wolf-0.2.16-aarch64-apple-darwin.tar.gz` | `b04310568d0104d7a804917bbd999cf4343c032c6e41aeda61c5b13b194706b5` |
| `wolf-0.2.16-x86_64-unknown-linux-gnu.tar.gz` | `84e30c05e56b89fde2fe6e27eec8f7cec0a6aae6e1464a2993fcfc87a7a1829e` |
| `wolf-0.2.16-aarch64-unknown-linux-gnu.tar.gz` | `fe1966a42a1d95b16f615f57aa4c3dd993b0ccce42ae8288d8f9ae70693e395e` |
| `lupin-0.1.38-aarch64-apple-darwin.tar.gz` | `28760a9923a9f5712dfaf06a827138e5b6ca617135447b267794c7a88434f3d6` |
| `lupin-0.1.38-x86_64-unknown-linux-gnu.tar.gz` | `828b5c5571644107a1b123490b5e188da50020676c6b15b0bc53a899a7cc520b` |
| `lupin-0.1.38-aarch64-unknown-linux-gnu.tar.gz` | `b85ec6471d0572e646a16326f49f6c243626546b1f64a10ec54d72af1941f5d2` |

Members of `wolf-0.2.16-x86_64-unknown-linux-gnu`, by name:

```
c4c5f6707f2832f01fa809d060d220f15b01fc2342e7c3d4f50e8b833b887101  libwolf_rt.a
3972dc9744f6499f0f9b2dbf76696f2ae7ad8af9b23dde66d6af86c9dfb36986  LICENSE
a0eec20d7b98b1cd0e5b4d23c3965667c97b68fb365ec95a9516b0c3cbc4fec4  LICENSE-EXCEPTION
8e14814231d73ef32021d7edb905470b19b854fd3994b1c0ae43e9f3b5e6aff9  README.md
2d1e48018333e3dd70473b34dfc78723f91f71d44a3d95287b68ce85fbbc2221  _wolf
b53b5328f6c020b7e77ee0be6fbdd9bbe41cdf49a185a263cd40218a1a3877c4  wolf
afcf4f7c84f75333cc091326f1e9ef6f5c659d42ceea3f446756a2175d70b608  wolf.1
29eb2d752591ab80fe54aed9e368f51aa9bfd557e48dd7ff2cc95e47fad27d97  wolf.bash
cf2c47a915c321e3ed1f1fa79c498b513212f184d4112c11033d5962b416807a  wolf-cimport-worker
51a1b6a8e12d6e3def4621af12cefee13ec6181ed1687ec9eba7f43f17550c2f  wolf.fish
```

**Then the build failed, and it was not boreutils' fault.** Two separate
things, and this note's own §2 decision about one of them was wrong.

**`wolf-std` HAD to move, and §2 said it would not.** The rev boreutils
pinned — `2d10219`, the same one lobo pins — does not compile under
0.2.16: `std/cmp/cmp.lu`'s `clamp` returns a `read` parameter, which
s168's place model now refuses (E1002, "`v` is the caller's value, and
it is returned here while the caller still holds it"). `std.cmp` is
reached from `use std.env`, so every utility failed to build.
wolf-std#39 (`9ca0139`) is the fix and it is only on trunk, so the pin
advanced to `070884c`. **§2 above says the deliverable was the two
release-archive halves and that moving the standard library in the same
commit would make a red ambiguous. The measurement falsified that in one
step, and §2 stands as written rather than being quietly rewritten.**
This is waiting for every other pin lane in wave 46: lobo pins the same
rev.

**And the compiler has a regression that blocks the shape this
repository's own exit convention prescribes** — filed as
**wolf-lang#449** with a witness, four controls and a cross-machine
verdict. 0.2.16's new E1002 exclusivity leg (CHANGELOG, "a container
element is a place") walks "everything spelled after a `mut` argument",
and the walk is not bounded by the call's argument list: it reaches
statements that PRECEDE the call and reports them as inside its extent.

```wolf
fn push_one(mut out: List[byte], n: int) { (mut out).push(n as byte) }

fn quoted(s: str) -> int {
    var out = List[byte]()
    if s.len > 0 { push_one(mut out, 120) } else { (mut out).push(64 as byte) }
    push_one(mut out, 64)        // 0.2.16 says the line above is "inside" THIS
    out.len
}
```

0.2.14 compiles it and prints `2`; 0.2.16 refuses it on both lanes
(`conform-run --json --checked` answers `"verdict":"fail(E1002)"`,
`"phase_reached":"mem"`); lupin 0.1.38 runs it and prints `2`. The only
argument after `mut out` is the integer literal `64`, so the
diagnostic's stated reason cannot hold. Four controls isolate it, and
`l2` — reorder the callee so the `mut` parameter is LAST — is the
decisive one: with nothing spelled after the `mut` argument the
diagnostic disappears, which is where the bad walk starts.

It landed on **twelve sites in seven of the fifteen existing
utilities**, because every boreutils program ends on
`bore.finish(mut out, prog, status)` and writes something under a
condition before it. Each is worked around under the issue's number and
named where a reader meets it: `bore.put_last` and `bore.finish_last`
are the two new spellings, and they are to be deleted at the release
that closes #449.

**One of the twelve was a real find and is FIXED rather than worked
around**: `src/seq.lu:208` returned a `read` parameter, which 0.2.16
correctly refuses under wolf-lang#366 with the `return copy d` fix-it —
the same shape as wolf-std#39's twenty sites.

### 2. B73 — a version is not the whole pin

The contract said `gnu-oracle.toml` must pin a build identity **or say
why it cannot**. The answer is both halves, and the second half turned
out not to matter.

**It cannot pin one.** Homebrew and Arch compile the same tarball this
file already pins by sha256; neither publishes an identifier a pin file
could name, and `--version` is identical by construction.

**It does not have to.** The disagreement is not a build IDENTITY, it is
a build-time DEFAULT, and the environment overrides it. gnulib's
`posix2_version()` decides whether the obsolete `+N` operand form is
read, and it consults `$_POSIX2_VERSION` FIRST. Measured on kasumi, an
Arch box whose compiled-in default is the older one:

```
$ tail +3 five-lines.txt                           -> lines 3, 4, 5
$ _POSIX2_VERSION=200112 tail +3 five-lines.txt
  tail: cannot open '+3' for reading: No such file or directory
$ uniq +1 two-lines.txt                            -> one line
$ _POSIX2_VERSION=200112 uniq +1 two-lines.txt
  uniq: +1: No such file or directory
```

and the obsolete forms that are NOT decided by it do not move: `head -3`,
`tail -3` and `tail -3l` answer the same either way.

So `gnu-oracle.toml` grew `[oracle.env]` — `LC_ALL=C`, which was
hard-coded in the harness and belongs in the pin for exactly this
reason, and `_POSIX2_VERSION=200112` — and `tools/difftest` builds every
case's environment from it, on BOTH sides. `[oracle.probe]` asserts that
the pin took: `uniq +1 /dev/null` must exit 1. On the `field` leg, where
`BORE_ORACLE_ANY` is already set, the probe is REPORTED rather than
enforced, because a build profile that differs is the finding that leg
exists to make — it is how B73 was found in the first place.

**Seen red, both ways, on kasumi.** With `_POSIX2_VERSION` set to
`199209` in the pin file:

```
difftest: the pinned environment did not take: `uniq +1 /dev/null` exits 0
where gnu-oracle.toml's [oracle.probe] wants 1 … no verdict is possible
against it.                                        (exit 2, the verdict lane)

difftest: ORACLE PROFILE DIFFERS: `uniq +1 /dev/null` exits 0 where
gnu-oracle.toml wants 1            (BORE_ORACLE_ANY=1, and the run continues)
```

**`tail +3` and `uniq +1` stop being skips.** Both were recorded
divergences that could not be cases; both are ordinary cases now and run
on every host. The corpus gained two cases of real coverage, which is
the opposite of bounding one to make it pass.

`tools/fetch-oracle` also takes its configure line from the pin file
now, so the staged oracle is specified by `gnu-oracle.toml` rather than
by a script. Verified end to end on kasumi by forcing the staged path:
the tarball built and `difftest` against `.gnu-bin/` reported
`oracle profile OK`.

**What B73 does NOT close**, stated because the contract asked: B75's
other divergences are the two hosts' C LIBRARY and long-double
arithmetic rather than coreutils at all, and no build identity would
have helped there. Those stay recorded skips — and this lane added one
more of exactly that kind (§5).

### 3. B98 — a difference is data, a death is a defect

**Ruled: the `field` leg is non-blocking about WHAT GNU ANSWERED and
blocking about WHETHER THE LEG RAN.** The line is not "which exit codes
are bad", it is that a leg which cannot say whether it finished has
produced no information at all, so treating its death as information is
a category error.

`continue-on-error` moved off the JOB and onto the one step that earns
it — the differential run, whose exit 1 is a divergence and is data.
`tools/field-verdict` states the ruling as a table (0 quiet, 1 advisory,
2 loud, ≥ 128 loud, anything else loud) and the workflow's next step,
which is NOT `continue-on-error`, runs it.

**Seen red on CI with a planted signal, and green without it, at two
commits one apart:**

| commit | run | the field job | conclusion |
|---|---|---|---|
| `7ffd256`, the plant | **35961824380** | **107511838008** | **failure** |
| `4ce1f42`, the plant pulled | **35962159388** | 107512849313 | success |

The failing step is `what that exit code MEANS (B98)`:

```
Run tools/field-verdict '141'
field-verdict: LOUD — the harness DIED of signal 13
field-verdict: (exit 141). A leg that cannot say whether it
field-verdict: finished has produced no information, so this is a
field-verdict: defect and not an advisory (B98).
##[error]Process completed with exit code 1.
```

The plant is `tools/difftest | head -c 1`, read through
`${PIPESTATUS[0]}`: a real SIGPIPE death of the harness, the same one
run 35673565877 took unnoticed. The PIPELINE's own status is `head`'s
and is 0, which is how it went unnoticed. It landed as its own commit
and was pulled out in the next one, so the history carries both.

`tools/field-verdict-selftest` is the standing gate and runs on every
gauntlet: it checks each exit code against the ruling, then plants a
REAL SIGPIPE death of `tools/difftest` and requires the ruling to be
loud about it.

### 4. The four utilities, and the fifth

| utility | cases | predicted | verdict |
|---|---:|---|---|
| `tac` | 102 | 90–110 | right |
| `paste` | 94 | 80–100 | right |
| `fold` | 102 | 70–90 | **wrong**, above |
| `expand` | 88 | 60–80 | **wrong**, above |
| `unexpand` | 98 | 60–80 | **wrong**, above |
| aggregate | **484** | 360–460 | **wrong**, above |

The corpus is **1,772 cases**, from 1,288; a run on kasumi answers
**1,752 passed, 0 failed, 20 skipped**.

**The speed predictions were worse. One of five bands is right.**

| predicted | measured |
|---|---|
| `tac` 0.3–0.6x on a file | **0.18x** — wrong, below |
| `tac` 0.6–0.9x through a pipe | **0.18x** — wrong, and its reasoning was wrong too: GNU buffers a pipe to `$TMPDIR` and seeks in that, so there is no "fair" comparison to be had |
| `paste` 0.5–0.8x serial, 0.3–0.6x parallel | 0.55–0.57x and 0.35–0.51x — **right** |
| `fold` 0.5–0.9x for `-b`, 0.25–0.5x for columns | **1.37–1.43x** and **1.07–1.90x** — wrong, above, in both bands |
| `fold -s` is the worst row | it is the **best** of its width (2.11x) — wrong |
| `expand` 0.4–0.7x | **2.30–8.47x** — wrong by an order of magnitude |
| `expand`'s tab-heavy input is the best case | it is the **worst** (1.01x) — wrong |
| `unexpand` 0.3–0.6x, and worse than `expand` | **0.99–9.23x**, and comparable to `expand` — wrong |

**Why, in one sentence:** every band assumed the per-byte decision was
the cost, and on these five it is GNU's multibyte decoder that is the
cost — coreutils 9.x runs `expand`, `unexpand` and `fold` through it
even in the C locale, and its slowest path is an invalid byte, which is
why the largest ratios in this repository (8.5x and 9.2x) are on binary
noise.

**And the first draft of all five was a memory defect.** Every one wrote
its output through `bore.put_byte`, which is correct and costs 2.6 to
2.8 times the output in resident memory, because the shared writer
empties its buffer by ALLOCATING A FRESH ONE and the old one is
abandoned in an arena that frees nothing. Measured before and after:

| | before | after | GNU |
|---|---:|---:|---:|
| `expand`, 256 MiB | 715 MB | **3.3 MB** | 2.0 MB |
| `unexpand -a`, 256 MiB | 692 MB | **3.4 MB** | 2.0 MB |
| `fold`, 256 MiB | 721 MB | **4.4 MB** | 2.0 MB |
| `paste`, two × 256 MiB | 1345 MB | **4.3 MB** | 1.7 MB |
| `tac`, 256 MiB | 1171 MB | **515 MB** | 1.8 MB |

The three that read and write a chunk at a time now build each pass's
output inside the per-chunk `region` and hand it to `write_direct`;
`tac` and `paste` cannot, because every call that would build their
output takes a `mut` parameter from outside the region (E1010,
wolf-lang#418), so they use the new `bore.Sink`: one buffer, filled in
place, written whole. Fixing the memory roughly halved the time on
`fold` and `tac` as well.

**`tac`'s 515 MB is twice its input and stays there.** It holds the
whole input because it owes the last record first and wolf has no seek
(wolf-lang#426); the factor of two is `List` having no capacity surface
(wolf-std F-0011), so the buffer doubles and each doubling abandons the
one before. **Sizing it up front from `fs_fstat` does not help, and that
was measured rather than assumed**: filling a list is itself a run of
pushes and doubles the same way.

**A separate 24x memory finding inside `tac -r`.** The first regex
matcher opened with `let a = copy pat.atoms[ai]`, the obvious spelling,
which copies the atom's 256-entry bracket table on every call. The bench
run was KILLED at exit 137: `tac -r -s '[aeiou][aeiou]*'` over 256 MiB
peaked at **29 GB**. Reading the fields through the place instead is
1.2 GB and 14x faster. A `copy` of a struct holding a list is not free,
and in a per-byte loop under an arena it is unbounded.

### 5. What CI found that neither dev host could

**A tenth host divergence, and it is B75's kind rather than B73's.** Run
**35960835138** failed the ubuntu leg on one case: `tac` on a directory
operand. Reading a directory answers EISDIR (`Is a directory`) on Arch
and on macOS, and EINVAL (`Invalid argument`) on the oracle built from
the 9.11 tarball on ubuntu-latest. boreutils has no errno text behind an
fs row at all (wolf-lang#407) and prints the one wording, so no single
answer can match every host. It is recorded as a skip naming both, in
the shape B75's divergences take, and **it is not bounded by a
version** — the version is the same on all three. Neither dev host could
have found it: both say EISDIR.

## 4. Evidence index

| claim | artifact |
|---|---|
| the pin comes from the release archives by digest | the table in §1; `wolf-toolchain.toml`'s `[wolf]` and `[lupin]` digests match it line for line |
| `_wolf` hashes the same at every target | `2d1e4801…` in all three wolf archives, listed in §1 |
| the corpus did not move at the bump | `difftest` before: `1271 passed, 0 failed, 17 skipped`; after: the same, and a `diff` of the two verdict lists over all 1,288 cases is EMPTY |
| `wolf-std` had to move | the E1002 quoted in §1, at `std://cmp/cmp.lu:356`, from `tools/build` at the new pin |
| wolf-lang#449 | https://github.com/wolffe-lang/wolf-lang/issues/449 — witness, four controls, three machines |
| B73's mechanism | the `_POSIX2_VERSION` transcript in §2, kasumi, coreutils 9.11-2 |
| B73's assertion seen red | the two `difftest` transcripts in §2, one refusing and one reporting |
| B73 closed two skips | `tests/cases/tail.toml`, `tests/cases/uniq.toml`; `difftest` went from 17 skips to 15 on kasumi at that commit |
| B98 seen red | run **35961824380**, job **107511838008**, step `what that exit code MEANS (B98)`; the same job one commit later is `success` in run **35962159388**, job 107512849313 |
| B98's standing gate | `tools/field-verdict-selftest`, run by the gauntlet on both hosts |
| the ubuntu divergence | run **35960835138**, `FAIL tac: a directory operand`, `Invalid argument` against `Is a directory` |
| the bench | `tools/bench --scale 0.25 --runs 5` on kasumi; tables in `README.md`; every bench file carries its prediction and was committed before the first run |
| the memory | `/usr/bin/time -v` on the same inputs; the before-and-after table in §4 |
