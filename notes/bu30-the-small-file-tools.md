# bu30 — boreutils at wolf 0.2.35, timeout's core, and the small file tools

*Written by the orchestrator at the merge from the PR body (boreutils#46), because the lane's Codex wrapper does not write Markdown. Merged by fast-forward at `3ddb68b`; `tier full` 39992795298 green on linux (difftest 7,027 / 0 / 123) and macOS (6,831 / 0 / 319). Issues filed from this lane: wolf-lang#906 (sync(2)/syncfs(2)), #907 (raw utsname fields), #908 (a writable open that never creates), #909 (a non-blocking writable open), #910 (fs_link cannot follow a source symlink); `truncate -o` added to #684. boreutils#44 closed.*

## Summary

Footprint: cross-cutting

Final portability head: `3ddb68b0e6b0d8532c33ad8dd1561810d8bb5799`. The orchestrator’s full-matrix label is retained.

Pin wolf 0.2.35 / lupin 0.1.56 with bundled std `2386522e`, suppress timeout's own core, and add eight utilities. `uname`, bare `sync` and filesystem-wide `sync` remain listed surface gaps, not substitutes.

**Forbidden:** no GNU implementation source consulted; no Mac builds, tests or git configuration; no merge, tag, release, issue creation or issue closure. Code and commits are on the Mac; runtime work is on hasu A in Ubuntu 24.04 containers with 12 GiB caps, inner CPU affinity and the shared flock.

## Changes

- `ceac9d7`: verified toolchain pin; six archive digests read from the release API twice and checked against r40's table.
- `d6ced61`: call `os_core_off()` before timeout re-raises; remove its three own-core design overrides. boreutils#44 is ready for closure after merge.
- `4c836e5`, `f65f6df`, `cfe8163`: mkfifo, link, directory-safe unlink.
- `6bc120e`, `823f32e`: truncate's size grammar/reference/no-create options, operand sync and `-d`.
- `bb56567`, `0f9cf19`, `d4eb6e8`: mktemp, realpath, tty.
- `e73caea`, `cf90877`, `fcbd6b6`: shared canonical-path recovery and trailing-link-slash fixes, with readlink twins.
- `88591fe`, `f300c11`, `0f4b198`: explicit empty options and full signed reduction range.
- `886ace7`: validate a tty's reported name against the actual pty slave before masking it. Random-name checks independently validate shape, alphabet, object kind and private mode.
- `cc17cef`, `e25cbcf`: explicit FIFO/write-only refusals instead of blocking or creating files as a fallback.
- `a16af68`: README counts, readiness and census.

## Evidence

**Inputs, verified:** base `12de639`; wolf tag `cf0c13d3`, lupin tag `28547b4`, bundled std `2386522e`; GNU coreutils 9.11 built by the digest-checked oracle tool. The thirteen new prelude names produce no bore shadow or deny-warnings diagnostic.

**Prediction score:** `8e6e0ec` preceded implementation. The pin alone preserved 6,668 / 0 / 120 on both tiers. Timeout's three own-core rows now compare directly with GNU. The prediction's “-s 33 stays skipped” wording was wrong: that row remains `design`, not a counted SKIP; Linux CI's one timeout SKIP is Darwin's EMT row. Extra open-surface gaps and shared path-walk bugs were found and recorded, not hidden.

**Evidence index:** `notes/bu30/ev/`, the reproducible probes in `notes/bu30/probes/`, and portability full run **39992795298**, first read **in_progress** at `3ddb68b0e6b0d8532c33ad8dd1561810d8bb5799`. The orchestrator watches; there is no CI wait by the lane.

| utility | cases | passed / skipped, both tiers |
|---|---:|---:|
| mkfifo | 34 | 32 / 2 |
| link | 17 | 17 / 0 on Linux; 15 / 2 on Darwin |
| unlink | 16 | 16 / 0 |
| truncate | 96 | 92 / 4 |
| sync | 19 | 15 / 4 |
| mktemp | 49 | 49 / 0 |
| realpath | 116 | 116 / 0 |
| tty | 12 | 12 / 0 |

Full differential: **7,020 passed / 0 failed / 130 named skips**, release and dev (before: **6,668 / 0 / 120**, both). Readlink is now 100 / 0. All 55 utilities build on both tiers with deny-warnings; fmt, 9 wolf tests with `--nocapture`, the shape/refusal gate and harness selftests pass. Killprobe agrees on all 240,578 numbers in all four comparisons. Container suites: kill 365 / 0 / 0; timeout 150 / 0 / 13; identities 1,098 / 0 / 28; inout 104 / 0 / 0; root 178 / 0. Kill and timeout use inner CPUs 0–3. Every SKIP is loud. Mac and Linux arm64 are not tested locally; no new benchmark claim is made.

**Own-core planted break:** branch `bu30-plant`, `49cab55`, CI run **39968180129**, job `timeout, repeated (bu27)`: all three whole runs were **159 / 3 / 1**. Exactly SEGV, ABRT with `-p`, and QUIT sent to timeout failed: an extra wrapper core, where GNU has none. The retained log is `notes/bu30/ev/ci-core-plant.txt`.

## Findings

**macOS portability follow-up:** full run **39987951234**, job **120532019884**, had eight failures (6,822 / 8 / 317). The retained red is `notes/bu30/ev/ci-macos-red.log`.
- `6202c37`: report the actual host unlink error for directories (Linux EISDIR, macOS EPERM), preserving the file-only removal invariant.
- `345ae3b`: the shared canonical walk validates every component before accepting libc realpath, which on macOS strips a regular file’s trailing slash. Existing `f/`, `-L`, `-P`, and link-target-slash rows cover the failures; explicit `-E f/` and a directory-positive row were added.
- `e2018a7`: **new gap to file:** fs_link cannot follow a symlink, so macOS link(1) cannot be matched atomically. The pinned [os.fs.link] and runtime fs_change.rs both require no-follow. Source symlinks now refuse by name on macOS, with two Darwin-scoped cases and a Darwin-only refusal test. The real GNU dangling-source result is ENOENT; it is never fabricated. Resolving then linking is not the missing atomic operation. **R-bu30-4:** the named refusal is accepted over silently hard-linking the symlink; implemented reversibly.

The planner has no jobs input or macOS-gauntlet partial target; no substitute full dispatch was made. The labeled push starts the full matrix. Linux recheck at the exact pushed head `3ddb68b` is green: 55 builds per tier, fmt, 9 strict wolf tests, six Python tests per tier (one loud Darwin-only skip), harness selftests, killprobe, and **7,020 / 0 / 130** on release and dev. Raw logs remain at `/home/mfwolffe/lanes/bu30/ev/gauntlet-portability.log` and `difftest-final-{release,dev}.log`. No Mac build/test is run locally.

Independent static review found no serious issue in mktemp, unlink, link, mkfifo, sync's other paths, tty's lookup or timeout's call placement; follow-up confirmed negative accumulation's bounds. Its numbered findings were handled as follows (GNU-first measurements at uid 1000 are retained):

1. No writable open without create exists. Keep `truncate -c`'s precheck and list its unlink/open race; do not claim atomic no-create.
2. Empty truncate reference: fixed with an option-presence flag; both cases leave the operand unchanged.
3. FIFO: GNU immediately reports ENXIO without a reader; bore now refuses by name before opening, rather than hanging or fabricating GNU's errno. Three bounded differential witnesses and bounded refusal tests remain.
4. Link target `f/` for regular `f`: fixed for realpath `-e`/`-E` and readlink `-e`.
5. Cyclic prefix then `..`: reset the abandoned walk's link budget; both realpath/readlink now follow the later link.
6. Empty relative-to/base: presence flags now force the empty path to fail.
7. Tty masking: compare the actual slave name first. The formerly false-green made-up-name case now fails as required by the harness selftest.

A final GNU-first mktemp check found dry-run lstat failures being mistaken for unused names: denied/io now fail (quiet still returns 1 silently); both denied-parent rows were red before the fix.

Signed-boundary cases were measured first: INT_MIN and `-9007199254740992K` reduce to zero; one below each rejects without change; MAX/MAX+1 use `-c` on an absent operand; `é`, `+é`, `-é` diagnose without a trap or mutation.

**Gaps to file in wolf-lang:**

- Global `sync(2)` / `syncfs(2)` for bare sync / `-f`. Witness: `src/sync.lu` and `notes/bu30/ev/witness.log`; both invocations refuse by name, exit 1. File-scoped sync calls cannot implement either operation.
- Raw uname fields. Witness: `notes/bu30/probes/surface.lu`: `os_name=linux` versus GNU's `Linux`; node, release and version have no call. No uname utility is shipped.
- A writable open without O_CREAT: `truncate -c` and write-only sync are two consumers. `notes/bu30/probes/open-gap.lu` prints `recreated=true` after stat/unlink/mode 2; mode 5 is not writable and mode 6 is invalid. GNU sync succeeds on owner mode 0200; bore refuses it by name, rather than adding a create race.
- A non-blocking writable open for truncate's FIFO operands. The stat-based refusal avoids the common-path hang; replacement by a FIFO after stat remains a listed race. Witness: the open probe, GNU-only review probe and bounded FIFO cases.

**wolf-lang#684, a second consumer, not a new issue:** truncate `-o` needs st_blksize, absent from all 20 stat words. `surface.lu` prints that layout; GNU `stat -c %o` prints 4096 on this filesystem. The refusal is by name, not a guessed block size.

Unlink needs no further surface: the file-only remove call preserves a directory and supplies its host diagnostic (Linux EISDIR, macOS EPERM). The lstat directory guard remains; no remove-directory call is used.

**R-bu30-1:** refuse `-o` rather than guess st_blksize; recommendation accepted, implemented reversibly. **R-bu30-2:** tty-local write-error status 3 rather than shared finish's 1; accepted, buffering and error text preserved. **R-bu30-3:** named write-only sync/FIFO refusals rather than append/create or a blocking open; accepted, with GNU's measured answers recorded beside each divergence.

## Checklist

**Done-when:** final source and the complete local strict gauntlet are green; the final head is declared final; PR tier is read once, then the lane audit is handed back. The orchestrator alone adds the full-matrix label and watches that tier.

- [x] Release API read twice; pin-control prediction checked
- [x] Both tiers, all utilities, fmt and strict unit capture
- [x] Full differential counts and every utility's cases
- [x] Harness plants, actual pty identity, random shape/private mode checks
- [x] Fresh isolated container suites and inner CPU constraints
- [x] Independent review findings fixed or explicitly listed with witnesses
- [x] README read and refreshed; uname remains blocked
- [x] No attribution trailers; the lane adds no label, and the orchestrator’s full-matrix label is retained
- [ ] Green tier pr at the final head
- [x] Initial audit at `4e3b225`: `AUDIT FAIL (footprint: cross-cutting)` solely pending CI/tier and then-missing label. For this portability handoff the label is retained; the new full run is pending. No new audit verdict is claimed.


