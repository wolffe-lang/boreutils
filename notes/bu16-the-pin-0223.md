# bu16 — the pin at wolf 0.2.23 / lupin 0.1.46

Lane note and contract. **Class:** medium (boreutils), **Opus**. **Wave:**
53. Contract: planning `wolffe-lang/wolf`
`sprints/boreutils/10-the-pin-0223/bu16-the-pin-0223.md` at planning
trunk `bd1dfa2`. Branch `bu16` off boreutils `075219a`. §1–§3 were
committed as `85bb455` before any archive was fetched; this file
restates them with the evidence.

## 1. Forbidden

No `rm` outside `~/lanes/bu16/` and this lane's worktree; no
`git add -A`; nothing under `~/.claude`; no build on nomad-1 (every
build and difftest ran on kasumi); no merge, tag or attribution
trailer; no "seen red" without a run id, sha, path or digest; the pin
from the release archives by digest only; GNU coreutils source never
read (GNU's behaviour is the 9.11 oracle, staged by `tools/fetch-oracle`
because kasumi ships 9.12). Strict evidence (wolf-lang#571): every count
below is read from the full output, stderr included; this repository
has no cargo gate, and `tools/difftest` prints its SKIP lines to stdout.

## 2. Inputs, verified (2026-10-04)

| the contract says | origin says | verdict |
|---|---|---|
| boreutils trunk `075219a` (bu15), 0.2.22 / 0.1.45, std `6a0df5e` | the same | holds |
| wolf 0.2.23 = `8edac3ee`, release 403069562, `6f505eb5…` / `f3b31984…` / `92c918f2…` / windows `eb8497cb…` | tag object `b05c0ef3` → `8edac3ee`; the release API's four digests are those | holds |
| lupin 0.1.46 = `f9269e33`, release 403040421, `d13a0379…` / `b84018ba…` / `320bf428…` / zip `495ad265…` / `lupin.exe` `8798adba…` | tag object `281fe8c7` → `f9269e33`; all five match | holds |
| 2642 / 0 / 32 at bu15 plus its 107 cases | 2749 / 0 / 32 (trunk CI push run 37173509510, ubuntu; macOS 2709 / 0 / 72); verdict list `3a4bc841…` | holds (the same number) |
| ruling #34 changes three fns' shape only | in 0.2.23; `bore.put`, `bore.put_byte`, `sink_push` end in `if … { …? }` | holds |
| sc54's std if it merged first | wolf-std has no sc54 PR; trunk is `6a0df5e` | the pin stays on `6a0df5e` |

kasumi had been rebooted minutes before (up 6 min at the base run), so
both sides were rebuilt on a fresh host, and the base reproduced bu15's
verdict list exactly (`3a4bc841…`).

## 3. Prediction, scored

| predicted (`85bb455`) | measured | verdict |
|---|---|---|
| all 27 build at 0.2.23 under `--deny-warnings`, nothing refused or warned | **one refusal**: W0304, `bore.offset_of` shadows the prelude's new `offset_of` (kw08), promoted by `--deny-warnings`; 0 built (`build-pin-try.log` `54bf0a43…`) | **wrong**, fixed here |
| ruling #34 fires nothing (each raise leaves through `?`) | after the rename: `errors=0 warnings=0 ice=0 built=27` | right |
| the new refusals (E0705, E0819, E0820, E0821, E1301, E1307) reach no site | none did | right |
| verdict list byte-identical to `3a4bc841…`, same 32 SKIP | at the pin `709809b`: `3a4bc841…`, 2749 / 0 / 32; the whole difftest log is byte-identical to the base's (`1aa2832e…` both) | right |
| selftest, `wolf test`, `wolf fmt --check` green; fmt moves nothing | green, nothing reformatted | right |
| `libwolf_rt.a` differs, so every binary differs | 27 of 27 differ; `crates/wolf_rt` is unchanged between the tags, but the crate hash moved with the version (`wolf_rt-6a72b950…` → `wolf_rt-e3125a76…`), renaming every symbol | right, reason refined |
| `_wolf` keeps `2d1e4801…` | in all three wolf archives | right |
| lupin is identity only | `tools/lib-toolchain.sh` reads its version line; no case runs it | right |
| no commit under `src/` needed | one rename (`ef82fcf`), then a restatement of still-open gaps (`a1e9f20`) | wrong (the rename) |

**The move table.** No verdict moved. Every change to the verdict list
is a SKIP reason's version text:

| step | verdict list | what moved |
|---|---|---|
| base `075219a`, 0.2.22 | `3a4bc841…` 2749 / 0 / 32 | — |
| the rename `ef82fcf`, 0.2.22 | `3a4bc841…` | nothing |
| the pin `709809b`, 0.2.23 | `3a4bc841…` | nothing (difftest log identical) |
| head `a1e9f20`, 0.2.23 | `443e432e…` 2749 / 0 / 32 | 8 SKIP reasons say `wolf 0.2.23` (printenv 4, pwd 1, tee 3); the base list with `wolf 0.2.22` → `wolf 0.2.23` substituted hashes `443e432e…` too |

The one binary that moves between the pin and head is `tee`: its `-i`
refusal now names 0.2.23. Two trees built the pin to the same 27
binaries (`bins-pin-709809b.sha256` = `bins-pin-ef82fcf-try.sha256`
= `850224f8…`).

**Why the rename and not a waiver.** W0304 is the compiler right: a
module fn named like a prelude fn silently wins over it everywhere in
the module. `bore.offset_of` (bu15's "where the next read starts")
became `bore.position_of` at its five call sites, before the pin, and
the rename alone builds and verdicts identically at 0.2.22. The
CHANGELOG's "Read this before you bump the pin" names the new refusals
but not that the three new prelude names can collide with a
downstream's own fn; reported to the orchestrator, not filed.

## 4. Evidence index

Every path is under kasumi `~/lanes/bu16/ev/`.

- The archives: `archives.log` `2ec99cb6…` (the six unix archives at
  0.2.23 / 0.1.46 and the 0.2.22 linux one, each and every member
  hashed by name). Members:

  | member | darwin-arm64 | linux-x64 | linux-arm64 |
  |---|---|---|---|
  | `wolf` | `fd75411e…` | `97b5404b…` | `8441a014…` |
  | `libwolf_rt.a` | `1897b731…` | `5af08d0e…` | `9fefa2b0…` |
  | `wolf-cimport-worker` | `e32af6a8…` | `23599021…` | `bd2ecb0d…` |
  | `_wolf` | `2d1e4801…` | `2d1e4801…` | `2d1e4801…` |
  | `lupin` | `66abb384…` | `fa4e6c35…` | `06711048…` |

  Identity: `wolf 0.2.23 (wolfgang, pin 8edac3e)` / `paired with lupin
  0.1.46 (reference interpreter), pin 8e36bc1`; `lupin 0.1.46
  (wolf-interp, reference interpreter at pin 8e36bc1)`. lupin's pin is
  wolf v0.2.22's commit, its spec pin (the 0.2.23 CHANGELOG says so).
- The prediction: `85bb455`.
- The refusal: `gauntlet-pin-try.log` `49b6c5cb…`, `build-pin-try.log`
  `54bf0a43…` (W0304 at `src/bore/bore.lu:747:8`).
- Base: `gauntlet-base-075219a.log` `df6584f4…`.
- The rename at 0.2.22: `gauntlet-rename-ef82fcf-0.2.22.log` `0ccae6cb…`.
- The pin: `gauntlet-pin-709809b.log` `8076fc22…` (and the same tree
  before the toml's last comment edit, `gauntlet-pin-ef82fcf-try.log`
  `c758ceb8…`).
- Head: `gauntlet-head-a1e9f20.log` `289b6f81…`.
- `gauntlet-mislabelled-075219a-0.2.22.log` is a run this lane's script
  launched as the pin while the pin tree's checkout had failed; it is a
  second 0.2.22 base run at `075219a` (its own header says so),
  renamed, and it reproduced the base's binaries (`46d74892…` both).
- CI at `1826f45`: run 37229323186. Attempt 1: ubuntu green; **macOS
  red at `build (release)`** (job 111515456616, log `d49a9c59…`):
  `wolf build: ICE: backend: read …/wolf-llvm-5650-1791142997632476000/wolf.o:
  No such file or directory`, building `expand`. Attempt 2 was green on
  the same commit (macOS job 111515949737, 2709 / 0 / 72; ubuntu job
  111515951101, 2749 / 0 / 32; field job 111515950290, 2692 / 15 / 74;
  SKIP lines counted in each full log: 72, 32, 74). These match bu15's
  trunk run 37173509510 leg for leg. Filed as **wolf-lang#583**. Read
  from v0.2.23's source and not reproduced: the release backend names
  its scratch directory by pid and wall-clock nanoseconds, but macOS's
  clock has microsecond granularity (the name ends `000`). Units are
  finished in parallel in one process, so two units can share the
  directory, and one deletes the other's object. It is not a boreutils
  defect and nothing here works around it. A macOS CI red at
  `build (release)` with this ICE is a re-run. CI at head: in the PR.

## 5. Done-when

Branch `bu16`; PR open, unmerged; CI green at head; worktree and
kasumi trees removed. Close nothing; nothing to close.
