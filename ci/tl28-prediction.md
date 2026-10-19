# tl28 — the prediction, before the first change (ruling #92)

Written before any tl28 change to this repository is committed, against
trunk `43ee185`.

**Before** (the ten completed push/pull_request runs of `ci` up to
39165773466): three jobs a run, the gauntlet on linux (18 to 20 minutes)
and macOS (15 to 21) and the field leg (5); **38.4 job-minutes** a run
(median 38.6) and **18.6 minutes of wall** (median; max 22.1). The
terminal read, measured (`ttyprobe`, macOS, a 50-minute ceiling) ran on
request alone.

**After, predicted:**

1. A pull-request push is `tier pr`: the plan (under 1 job-minute, the
   planner's test inside it), `gauntlet (ubuntu-latest, )` (18 to 20), the
   field (5) and the verdict (under 1): **24 to 27 job-minutes, about 20
   minutes of wall** (the linux leg was already the pole), the macOS leg
   skipped: about a third fewer job-minutes and no macOS slot.
2. A notes-only pull request (bu28's shape) is `tier noop`.
3. The `full-matrix` label at the head is `tier full`: both legs and the
   field, **about 38 job-minutes and 19 of wall**, as before.
4. A dispatch with `-f tier=pr` of a branch that adds a path no rule names
   comes out `tier full`; a dispatch with `only` naming a job is
   `tier partial`, that job alone, as before.
5. The nightly is `tier nightly`: the full tier and the terminal read,
   measured, on macOS (about 38 plus up to 50 job-minutes).
6. The planted break (an unmapped path classified pr in `ci/tiers.py`) reds
   the plan job at "the planner can say no", skips every job, and the
   verdict job, `tier unplanned`, is red: **1 to 2 job-minutes**.
