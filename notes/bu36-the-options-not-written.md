# bu36 — the options not written

_Materialised from boreutils#62's body at the merge (`d3d8773f`); the Codex wrapper writes no .md notes._


Five-section bu36 note: wrapper instructions prohibit Markdown report files, so this PR body carries the requested `notes/bu36-the-options-not-written.md` narrative. The tracked receipts are under `notes/bu36/`.

## Prediction
- `346a4a7`: prediction committed before code at trunk `aaa8842fbda7a5e09637c196dc3583f9c70d86aa`: existing surfaces should fit listing/backup/link controls; env and date grammar need the most behavioural work; incomplete black-box derivations remain named refusals.
- Predicted at least 35 Linux skips retired and 150 new rows. Measured: **36 retired**, **307 new registered rows**, corpus **16,495 → 16,802**, still 105 case files / 107 binaries / 103 of 104 utility units. `df` remains blocked on wolf-lang#686; nothing fakes statfs.

## Forbidden
No GNU/gnulib/libc or other implementation source read: GNU 9.11 documentation and oracle outputs only, plus org-owned code. No Mac build, pin/CI/spec/runtime change, package installation, attribution trailer, issue filing/closing, PR label, merge, tag or CI wait. Hasu block B only: CPUs6–11 inside rootless containers, 12GB caps, both canonical B locks. Planning and `~/.claude` untouched.

## Inputs verified
- Wolf0.2.35: tag/pin cf0c13d; Linux archive `4cc4045bbbb605c07835bc4f32685953c784eeef4cd3139a48b457dfc90dad1a`, hashed twice; driver and libwolf_rt.a match archived members.
- Lupin0.1.56: archive `ad703550ac4787e8e4bb26989d591a731410274d7332f2b4e8b9a64c878822cc`, hashed twice, archived driver matched. Bundled std `2386522eb059cca5a84108562c2c0a0e72345d34`: all55 module blobs and key sets match both ways.
- GNU coreutils9.11 tarball `394024eda0a5955217ceda9cd1201e65dc8fa3aa29c2951135a49521d57c3cc3`, hashed twice; complete staged binary manifest checked. `LC_ALL=C`, `_POSIX2_VERSION=200112`, obsolete-syntax probe live. Whole archived stages copied then reverified, never another oracle.
- [Exact input receipt](notes/bu36/input-verification.log). No pin moved.

## Evidence index

### CI40376244635 query-boundary repair at `d3d8773f120104fe7a4121ab2052c1897b0c544a`
The single macOS failure was env --ignore-signal=KILL: GNU9.11 fails reading the old action and says GET, whereas the old code reported SET. Prediction committed before edits in bb627e5. Paired native read-only ctypes probes measure Darwin KILL9/STOP17 GET=-1, errno22, with TERM/PIPE controls succeeding; Linux KILL9/STOP19 and controls all GET=0. The source explicitly names an **attributed platform model standing in for a per-signal action getter wolf0.2.35 does not expose**, not an actual GET call. Only those measured Darwin boundaries return GET failure before a setter; other paths retain the real setter and report SET if it fails. [Repair/proposal note](notes/bu36/signal-query-repair.txt), [Mac probe](notes/bu36/signal-action-query-darwin.jsonl), [Linux probe](notes/bu36/signal-action-query-linux.jsonl).

- Checked Mac `conform-run --json --checked src/env_signal_action_test.lu`: **exit(0), diagnostics/warnings empty**, after the 8GB memory guard; no native Mac build. [Receipt](notes/bu36/signal-action-checked-darwin.json). Same checked row on Linux also exit(0), empty diagnostics/warnings, asserting both exact GET/SET messages and ordinary-signal controls. [Receipt](notes/bu36/signal-action-checked-linux.json).
- Linux env **126 passed/0 failed/8 named skips EACH native tier**, including original KILL and added STOP cases. Units **38 passed**, one explicit native checksum-stream fallback, not all-checked. Formatter/diff checks pass. Corpus16,803; latest repair adds one case to the earlier307. Ignore-signal selected rows now9/9.
- Original detached full gauntlet actually finished **exit0 at da79faf6**, both tiers**16,646/0/156**. [Exact completion](notes/bu36/original-full-completion.txt). This is historical, NOT a fresh full run covering this repair. New-head CI is read once after push; no wait, no labels, PR remains draft.

Upstream recommendation for the coordinator to file (lane files nothing): add `os_signal_action_one(meaning: int) -> int ! {invalid, unsupported, QueryFailed(int)}`, a read-only query accepting every sending-shape meaning, including fault/KILL/STOP and host -N forms. Return0=SIG_DFL,1=SIG_IGN,2=another installed handler, never a pointer. `invalid` names malformed/out-of-range meanings; `unsupported` names hosts lacking the operation; `QueryFailed(errno)` preserves the native GET error for a valid signal, notably Darwin KILL/STOP EINVAL, without conflating it with a shape error or losing its words. Change neither dispositions nor masks. A later pin replaces this model with the real query and distinguishes actual GET and SET failures.

- `d06d74a`: ls author column, display units, +FORMAT and C quoting. `7d0a903`: touch shares date's independently written token grammar, including separate reference atime/mtime clocks; [grammar](docs/touch-date-grammar.txt).
- `85241cf`, `e14f5f8`, `3f08441`, `9ee318e`: ln backups, rm device guard, mv update/backups/debug, cp links and the five remaining controls. `1733b5f`, `68f717b`, `127d214`, `381570a`, `7e408ad`, `58d6667`: precedence, same-entry/alias safety, unbounded backup versions and protected-parent metadata cases, each chunk committed separately.
- `a758465`: env splitting/debug/ignore actions; explicit mask limits below, not a pretend implementation.
- `a439a02`: measured Darwin od NaN rule with both platform selectors exercised in pure tests; twelve exact Darwin skips retired. **Native Darwin CI is pending**, not claimed locally.
- `6d39230`: independent shuf/tsort attempts and exact thirty-row Darwin review. `5cd937b`: full-state container witnesses and local red plant. `17f5df0`: README read/refreshed, status/readiness/counts/build/install paragraphs checked; existing speed numbers remain dated, not rerun.
- [Complete receipt index](notes/bu36/evidence-index.txt), [per-option row counts](notes/bu36/options-table.json).

### Measured gates (GNU9.11, hasu B)
- [x] Seven-family differential **2,006 passed / 0 failed / 41 named skips EACH native tier**. Before: **1,663 / 0 / 77** on unchanged trunk dev. [dev](notes/bu36/family-dev.log), [release](notes/bu36/family-release.log), [before](notes/bu36/baseline-diff.log).
- [x] Unit suite **37 passed**, including both Darwin/Linux NaN models: **36 checked, one native fallback** (`checksum_stream_test`, checked step budget), not all-checked. [Receipt](notes/bu36/unit.log).
- [x] [Complete-state integration](notes/bu36/options-integration.log) **59/0/0**, with real tmpfs boundaries, positive controls, independent live-relative date bounds and inherited blocked-PIPE refusals.
- [x] [Root refusal gauntlet](notes/bu36/roottest.log) **178 passed / 0 failed**. [idtest](notes/bu36/idtest.log) **1,098 passed / 0 failed / 28 loud CI-runner-only skips**. Each case in its own disposable pinned container; static binaries built inside Ubuntu, not linked against hasu's host libc.
- [x] Local planted missing author column produces **five named FAILs, exit1**, before restored green; [receipt](notes/bu36/plant-run.log), full red retained on hasu. Missing mask primitives produce **E0301 / compiler exit2**, never counted as skips.
- [x] Formatter and diff checks pass; no new native-warning allowance.
- [ ] **Full-repository final-head gauntlet is detached/pending**, not a new full green. Durable launcher `/home/mfwolffe/lanes/bu36/run-full.sh`; PID `/home/mfwolffe/lanes/bu36/full.pid`, log `/home/mfwolffe/lanes/bu36/ev/full.log`, exit marker `/home/mfwolffe/lanes/bu36/full.exit`; [recipe](notes/bu36/run-full.sh). The lane hands back instead of waiting on a >20min job.
- [ ] CI run id and final-head audit are handed back immediately; no lane CI wait or label. Darwin validation is explicitly required for the od selector and the shared listing changes.

### Options (rows pass / selected, both native tiers unless stated)
| utility | option | rows | verdict |
|---|---|---:|---|
| ls | --author | 6/6 | pass |
| ls | --block-size | 21/21 | pass |
| ls | --time-style=+FORMAT | 7/7 | pass |
| ls | -Q | 8/8 | pass |
| env | -S | 17/17 | pass |
| env | -v | 8/8 | pass |
| env | --ignore-signal | 8/8 | pass |
| env | --default-signal | 4/4 | unblocked Linux masks only; blocked/unknown refused |
| env | --list-signal-handling | 3/3 | Linux /proc; Darwin refused |
| env | --block-signal | 1/2 | empty no-op passes; nonempty remains named refusal |
| ln | -b / --backup; -S | 42/42; 10/10 | pass |
| rm | --preserve-root=all | 6/6 | pass; real cross-device witness also live |
| mv | -u; -b / --backup; -S; --debug | 19/19; 32/32; 8/8; 5/5 | pass |
| cp | -s; -l | 22/22; 23/23 | pass |
| cp | -u; -b / --backup | 12/12; 61/61 | pass |
| cp | --parents; --attributes-only; -x | 15/15; 18/18; 2/2 | pass; real mount boundary also live |
| touch | -d free-form / -r -d | 25/25 | fixed reference states plus independent live-clock bounds |

### Six issues and recommendations (implemented, not decided)
- **R-bu36-1 / #49: retain refusal.** 152 known-byte oracle rows; four modulo/rejection/Fisher–Yates hypotheses all fail (best34/125 successful permutations). This attempt failed; it does not prove black-box derivation impossible.
- **R-bu36-2 / #50: retain refusal.** 576 oracle graphs,457 cyclic; no one of72 DFS orientation/order/root/rotation hypotheses predicts even every first diagnostic cycle (best264/457). Full outputs retained. Existing DAG/simple-cycle coverage and refusal ledger unchanged.
- **R-bu36-3 / #51: defer optional bounded storage.** Not cheap in this pass; no implementation or RSS improvement claimed.
- **R-bu36-4 / #58,#59,#60:** every original measured row reviewed against attribution40165219687, both code heads and all three GNU9.11 providers. #58 retains11 exact account-name qualifications; #59 retains7 exact numeric-boundary qualifications. #60 implements the measured NaN rule and removes12 skips; recommend closure only after native Darwin CI validates it. **No masks, altered oracle answers, new GNU-bug claim or issues closed.** [Row review](notes/bu36/darwin-row-review.json).
- **R-bu36-5:** request upstream portable signal-mask query/set/unblock. Nonempty block actions, blocked/unknown default masks and Darwin listings refuse125 explicitly, never run a command with silently wrong state. Empty signal lists are no-ops. Missing-surface compile witnesses tracked.
- `cp -a`, `-d`, `--preserve=links` still refuse hard-link identity preservation among sources; xattr/context/all and ACL marks retain #685. `df` remains #686-blocked.

One earlier release run differed on the partial tree of existing `-p: -pr d d/sub/e`. It remains **live and unwaived**. The final family runs are green; rebuilding unchanged trunk and repeating that isolated case30 times on each of trunk-release, candidate-release and candidate-dev gave90 greens, so attribution remains unresolved. [Exact retained red](notes/bu36/cp-selfcopy-once-red.txt), [attempt](notes/bu36/cp-selfcopy-attribution.log). Report for further inode/order fixture investigation; do not erase this evidence.

## Done-when
- [x] Requested options each have code and GNU9.11 rows, per-utility commits; actual missing primitive remains named.
- [x] Own touch grammar documented; complete reference and live-clock witnesses.
- [x] Six issue dispositions, measured attempts, retained boundaries and exact Darwin attribution.
- [x] README/status/readiness re-pasted; measured scoped skips **77 → 41**, corpus **+307**; no df imitation.
- [x] Local plant seen red: `notes/bu36/plant-run.log`, five FAILs/exit1 from the author mutation; complete-state/root/id tests run, receipts retained; no labels or CI waits.
- [ ] Detached full gauntlet exits0 at the exact final head.
- [ ] Final-head CI, especially native Darwin, green; orchestrator watches.
- [x] Required audit run once at final head: `AUDIT FAIL (footprint: module)`. It surfaced matching-head CI **40376244635**, in progress. Its missing-artifact complaint was the Done-when plant line (now explicitly cites `notes/bu36/plant-run.log`); the owned Mac worktree is pruned at handback. No audit rerun and no CI wait. The detached full gauntlet is PID **3943061**; `full.exit` is pending. Audit receipt: `/Users/mfwolffe/lanes/bu36/audit.log`.

Prune only after the recorded job is finished and review/merge permits: owned hasu `boreutils/target`, `.wolf-bin`, `.gnu-bin`, `toolchain-input`, `oracle-input`, `tmp`, and bundle under `/home/mfwolffe/lanes/bu36`; retain `ev/`, scripts and markers. Mac worktree is exactly `/Users/mfwolffe/lanes/bu36/boreutils`; never prune repo-wide worktrees.

