# bu19 — the byte surface (boreutils at wolf 0.2.26 / lupin 0.1.49)

Lane note and contract. **Class:** medium (boreutils), **Opus**. **Wave:**
53. Contract: planning `wolffe-lang/wolf`
`sprints/boreutils/13-the-byte-surface/bu19-the-byte-surface.md` at
planning trunk (fetched 2026-10-09). Branch `bu19` off boreutils
`50d8907`. §1–§3 are committed before any 0.2.26 or 0.1.49 archive is
fetched or unpacked; §3 is scored in place later, never rewritten.

## 1. Forbidden

No `rm` outside kasumi `~/lanes/bu19/` and this lane's worktree
(`boreutils-bu19`); no deletion in any tree this lane did not create; no
`git add -A`; nothing under `~/.claude`; no edit to another lane's file;
no merge, no tag, no attribution trailer; no `2>/dev/null` on a checkout.
The pin from the RELEASE ARCHIVES by digest, never a clone, Homebrew or
`~/.local/bin`. No build on nomad-1: every build, difftest and bench runs
on kasumi with `CARGO_INCREMENTAL=0`, one tree per state, pruned as it
goes. No "seen red" without a run id, sha, path or digest. Strict
evidence (wolf-lang#571): counts are read from the full output, stderr
included (`tools/difftest` prints SKIP to stdout). **GNU coreutils source
is never read**: GNU's behaviour comes from its documentation and the
staged 9.11 oracle (`tools/fetch-oracle`), black-box, including through a
pseudo-terminal.

## 2. Inputs, verified (2026-10-09, release API and origin)

| the contract says | origin says | verdict |
|---|---|---|
| wolf 0.2.26 = `89dc1394`, linux x86-64 `05acdc5e…`, aarch64 `8b019b64…`, macOS `8ea7ef3b…`, windows `9cb6958d…` | release 408143286 (published 17:48Z); tag object `fdc73f26` → `89dc1394`; the four asset digests are those | holds |
| lupin 0.1.49 = `f516a5f`, linux x86-64 `84911a35…`, aarch64 `e1f53d15…`, macOS `ad188d58…`, zip `ebff44ab…`, `lupin.exe` `64212006…` | release 408028965; tag object `5d14986a` → `f516a5f4`; all five match | holds |
| boreutils trunk `50d8907` (bu18), pinned 0.2.25 / 0.1.48 | the same; std `0f74ec5`; trunk CI run 37739571055 green: ubuntu 2986 / 0 / 62, macOS 2945 / 0 / 103, field 2921 / 15 / 112 | holds |
| what 0.2.26 changes: s217 capabilities, #618, `copy region`, `-> never`, `!` on integers, the nine builtins, 10 new prelude names (W0304) | the CHANGELOG's "Read this before you bump the pin" says so; a grep of `src/` for a declaration of any of the ten finds none; boreutils has no `wolf.pkg`, so s217 cannot refuse a build here; s216 measured boreutils byte-identical under #618 | holds |
| s200's probes: `wc -l` 0.38x GNU, `cat f > g` 5.7 ms vs GNU 17.5 | wolf-lang#627's body: `wc -l` 81.4 ms vs GNU 31.1 on 256 MiB; `cat f > /dev/null` 6.6 vs 7.2; `cat f > g` (btrfs) 5.7 vs 17.5; the probes were throwaway copies, never pushed, and kasumi `~/lanes/s200/probes/` is empty | holds; the code is this lane's to write |
| bu18's `ls` PENDING list (`os_isatty`) | one case, `-C on a terminal is the default`, skipped on the primitive; `src/ls.lu`'s header names it | holds, and **GNU's terminal default is wider than "columns and `-q`"**: see below |
| wolf-lang#624 (`unexpand` slower) | open | re-measured at this pin |
| wolf-std | trunk still `0f74ec5`; sc57 (std at 0.2.26) is open, not merged | the std pin is re-derived at the bump (B151) and again if sc57 merges first |

**Drift, GNU's terminal default (measured before any code, kasumi
`~/lanes/bu19/probe/ptyrun.py`, GNU 9.11, `LC_ALL=C`, standard output a
pseudo-terminal):** on a terminal GNU's `ls` does not only switch to
columns and `?`. Its default QUOTING STYLE becomes shell-escape: `with
space` prints `'with space'`, a newline `'new'$'\n''line'`, `é`
`''$'\303\251'`, and in `-C`/`-x` every unquoted name in a listing that
holds a quoted one gains one leading space, so the columns align on the
quote. `?` for a control byte shows only under the literal style (`-N`,
`QUOTING_STYLE=literal`). Directory headers are quoted the same way.
The width is `-w`, then the TERMINAL'S OWN WIDTH (`TIOCGWINSZ`), then
`COLUMNS`, then 80: a terminal 80 wide with `COLUMNS=30` lays out at 80,
a terminal reporting 0 columns takes `COLUMNS`. wolf 0.2.26 has no way to
ask a terminal its width, so this `ls` can match GNU on a terminal only
where the terminal's width is 80 or unreported; that is filed upstream
with the witness.

## 3. Prediction (committed before the archives are fetched)

Each line names what moves, by how much, and the number that falsifies
it. "±5%" is against the same row's previous state, both measured in ONE
hyperfine call with GNU beside them (bu17's A/B shape), at load near 1.

**The pin (its own commit; no `src/` change).**
1. The archives' digests are the release API's above; `_wolf` keeps
   bu17's `a368c8ec…` (no subcommand added in 0.2.26's CHANGELOG).
2. All 28 utilities build on both tiers under `--deny-warnings` at std
   `0f74ec5`: no W0304 (no local shadows), no E1504 (no manifest), no
   E1010 (#618: s216 measured boreutils byte-identical). Falsified by any
   diagnostic.
3. All 28 binaries differ from 0.2.25's raw AND after `objcopy
   --strip-debug --remove-section .note.gnu.build-id`, because
   `libwolf_rt.a` changed (s200, s213, s215 and the crate hash);
   `--emit=wir` is byte-identical in all 28, because no 0.2.26 change
   reaches boreutils' lowering (s200 measured 180/180 codegen units
   identical; s216 byte-identical; s213/s215/s217 add surfaces `src/`
   does not use). Falsified by one WIR that differs.
4. Verdicts identical to trunk (2986 / 0 / 62 on kasumi's oracle); the
   verdict text moves only where a SKIP reason names "wolf 0.2.25" and
   is restated (pwd 2, printenv 4, tee 3).
5. Every bench row benched below sits within ±5% of 0.2.25's at the pin,
   **including #624**: `unexpand` on ordinary lines stays ~1.5x slower
   than 0.2.23 (the partition follows boreutils' own fns, which do not
   change). Falsified by any row past ±5% that a repeat confirms.

**Adoption A — descriptors 0, 1 and 2 directly (`bore`).** `stdout()`
writes descriptor 1 (closed is `fs_fstat(1)` answering `io`, not a
failed reopen), `-` reads descriptor 0; the `/dev/stdout` and
`/dev/stdin` reopens, the `print_raw` fallback for a socket and the
offset dance (`settle`) go.
6. Every verdict identical, including bu15's 216 offset cases and every
   `stdout_closed` case on both hosts. Falsified by one FAIL.
7. `strace -f` of `cat f`, `wc -l < f` and `head -n 1 -`: no `open` of
   `/dev/stdout`, `/dev/stdin` or `/proc/self/fd`, where trunk has one
   each. No bench row moves past ±5% (the reopen is one syscall).

**Adoption B — `os_error_text(os_error())` for the host's words.**
8. Three SKIPs become passes on ubuntu (wc's ENOTDIR and ELOOP, ls's
   EACCES through an unreadable directory); macOS the same where the case
   runs. The 24 `/dev/full` cases (23 utilities) widen from `compare =
   ["exit"]` to the full comparison and pass on linux: every utility says
   `PROG: write error: No space left on device` (cat too, through
   `write_direct`). Falsified by one of the 27 failing.

**Adoption C — `cat` through `fs_copy_chunk` to descriptor 1** (the
plain path; `-n` and friends keep the rendering loop).
9. `cat` a 1 GiB file to /dev/null: 120 ms → **≤ 15 ms** (GNU 6.0);
   to a file on btrfs: 706 ms → **≤ 60 ms** (GNU 34.8); 64 operands to
   /dev/null: 590 ms → **≤ 40 ms** (GNU 18). `-n` within ±5%. Verdicts
   identical, `/dev/full` included (an `io` from the copy falls back to
   read-then-write to say WHICH side failed).

**Adoption D — `wc -l` through `bytes_count`.**
10. `-l` on 1 GiB, C and UTF-8: 434 ms → **150–280 ms** (GNU 74; the
    rest is `fs_read_chunk` allocating a fresh list per chunk, which no
    0.2.26 call avoids); `-l` on very short lines: 126 ms → **≤ 30 ms**
    (GNU 5.8). Every other `wc` row within ±5%.

**Adoption E — line splitters through `bytes_find`/`bytes_count`**,
adopted per utility only where it pays (no row slower past 5%, one
faster past 5%).
11. `tail -n 10` through a pipe: 422 → **≤ 250 ms**; of short lines
    through a pipe 132 → **≤ 80 ms**; `head` and `tail` rows that read
    back from a file unchanged (no backward scan: `bytes_find` is
    forward only).
12. `nl`, `uniq`, `cut` on ordinary lines: **0 to −15%** each; on very
    short lines (4 bytes average) a call per line costs about what the
    loop did, so **±5%** there. Where a utility gains nothing it is NOT
    adopted and the measurement says so.

**Adoption F — `ls` on a terminal (`os_isatty`), through a
pseudo-terminal in `tools/difftest`.**
13. On a terminal: `-C` by default, shell-escape quoting with the
    alignment space, quoted headers, `?` under `-N` (the literal style,
    added because it is the only place GNU's `-q` default shows). New
    pty cases pass on linux and macOS, the bu18 PENDING case among them;
    the cases where GNU reads a terminal width other than 80 SKIP naming
    the new upstream issue. Every pipe verdict identical; `ls`'s bench
    rows (pipes) within ±5%.

**CI.** Green on ubuntu, macOS and the field leg at the head: trunk's
counts plus the new cases, minus the cleared skips, 0 failed.

## 3a. The prediction, scored (added after the measurements; §3 above is as committed in `7a2f552`)

| # | predicted | measured | verdict |
|---|---|---|---|
| 1 | digests as the API; `_wolf` keeps `a368c8ec…` | all six archives match (`archives.log` `10fd5da8…`); `_wolf` `a368c8ec…` in all three wolf archives; new members `wolf.1`, `wolf.bash`, `LICENSE-EXCEPTION` | right |
| 2 | 28 build on both tiers, no diagnostic | `errors=0 warnings=0 ice=0 built=28` release and dev at the pin (`gauntlet-pin-d39e57c.log` `7df1f40e…`) | right |
| 3 | 28 differ raw and stripped; WIR identical in 28 | 28/28 raw, 28/28 stripped on each tier; `--emit=wir` identical in 28/28 (`wir-*.sha256` `532121dc…` both); own-function instruction and load counts identical on both tiers; `libwolf_rt.a` `6ac563e7…` → `679d77e1…` | right |
| 4 | verdicts identical, only restated reasons move | `b7154d32…` at base and pin, release and dev (2986 / 0 / 62); the nine "wolf 0.2.25" reasons restated in `4a5b801` | right |
| 5 | every benched row within ±5% at the pin, #624 still ~1.5x | most rows within ±5%; **`wc` default counts +11.7%** at the pin, confirmed at 30 runs (2069 → 2310 ms), identical user instructions (13.805 G) and +12.4% cycles, hot loop at a different address: code placement, and the next build (`ab`) is back at 2076 ms; `cat` rows −12% at the pin in the noisiest window (load 7–11), not repeated; **#624 is GONE**: `unexpand` ordinary lines 2820 / 2929 ms at 0.2.25 / 0.2.26 against GNU 6547, `one` 689 instructions as at 0.2.23 | **wrong twice**: a placement move on `wc`, and #624 vanished because `bore` grew (bu18), not because anything fixed it; commented on wolf-lang#624 |
| 6 | A: every verdict identical | 2986 / 0 / 62 after A (`try-fdA.log`) | right |
| 7 | A: no reopen in strace; no row past ±5% | no `/dev/stdout`, `/dev/stdin` or `/proc/self/fd` open in `cat`, `wc -l <`, `head -`; rows: **`cut` on very short lines +42% / +45%** (383 → 546, 543 → 788 ms), **`uniq` −11% / −14%**; the stdin rows' first +7–10% did not survive 30 runs | **wrong for `cut`/`uniq`**: same instructions, the system time is glibc trimming the heap per chunk (10 → 1,537 `brk`), and a malloc tunable makes both builds equal: filed **wolf-lang#644** |
| 8 | B: three skips pass; 24 `/dev/full` cases compare stderr | wc ENOTDIR, wc ELOOP, ls EACCES pass; every `/dev/full` case passes with stderr; added `sort` ×2, `head`, `tail` full-device cases | right, after threading the host's number past `close_input` in eight utilities (a successful close clears it) |
| 9 | C: `cat` ≤ 15 / ≤ 60 / ≤ 40 ms, `-n` ±5% | 9.9 ms (GNU 8.3), **60.1 ms** (GNU 54.5, min 53.0), 25.3 ms (GNU 18.4), `-n` +2.5% | right but for the file row, 0.1 ms over its bound by the mean; and a **silent wrong answer found on the way**: the first cut exited 0 on `cat f > /dev/full` (the copy's read/write rung had taken the bytes off the input), caught by the difftest case, fixed, filed **wolf-lang#642** |
| 10 | D: `wc -l` 150–280 ms, short ≤ 30 ms | 173 / 172 ms (GNU 88 / 91), 15.6 ms (GNU 7.0); default counts +2% | right |
| 11 | E: `tail -n 10` pipe ≤ 250, short ≤ 80; read-back rows unchanged | 166.5 ms (GNU 302: **1.82x GNU**), 11.2 ms (GNU 79.6: **7.11x**); `-n 10` of a file 0.4 → 0.5 ms, `-n +1` +4.5% | right |
| 12 | E: `nl`/`uniq`/`cut` 0 to −15% on ordinary lines, ±5% on very short | `nl` −8.5%; `uniq` −12.6%; **`cut -b` −28%, `cut -f1` −23%, binary noise −53%**; very short: `nl` −2%, **`uniq` −12%**, `cut` −2% / −7%; `head -n -1` through a pipe −18% | **wrong in the good direction for `cut` and short-line `uniq`**: `cut`'s line scan was a larger share than its per-line work; every one adopted |
| 13 | F: pty cases pass on both hosts; PENDING clears; two skip on width; pipes unchanged | 24 run + 2 skip on linux (kasumi, CI) and macOS (CI); `-C on a terminal` passes; 21 of them fail against the pin's `ls` (`lsF-against-pin.diff` `3fc864e4…`); `ls` pipe rows within ±3% | right; GNU's default QUOTING style on a terminal was the drift §2 recorded before writing code |
| CI | green on all three legs | run 37984988431 at `9d9cb2b` green: ubuntu 3017 / 0 / 60, macOS 2972 / 0 / 105 (as run 37982011386 at `880af7f`); field 2951 / 16 / 110 there, the 16th the `wc` `/dev/full` reason 9.4 does not print, bounded by `gnu_min` in `9d9cb2b` | right, and the field leg found a tenth 9.11-only `wc` case |

## The move table

**Verdicts**, kasumi, release and dev identical at each state:

| state | passed / failed / skipped | list |
|---|---|---|
| base `50d8907` (0.2.25) | 2986 / 0 / 62 | `b7154d32…` |
| pin `d39e57c` | 2986 / 0 / 62 | `b7154d32…` |
| head `9d9cb2b` (the code at the PR head) | **3017 / 0 / 60** | `591bf0fc…` |

pin → head: +29 cases (24 run on a pseudo-terminal and 2 skipped on its
width, `sort` ×2, `head` ×1, `tail` ×1 into a full device); three skips
now pass (`wc` ENOTDIR and ELOOP, `ls` EACCES); the `ls` PENDING case
passes; nine restated reasons. Nothing that passed stopped passing.

**Binaries**: pin → head, all 28 differ stripped on both tiers (every
utility compiles `bore`, whose output path changed).

**Bench rows before and after**, kasumi, one hyperfine call per row
(10 runs, `ab.py`, kasumi `~/lanes/bu19/ev/ab-*/`), ms mean:

| adoption | row | 0.2.25 | pin | after A+B | after the adoption | GNU 9.11 |
|---|---|---:|---:|---:|---:|---:|
| C `cat` | 1 GiB to /dev/null | 285.1 | 250.3 | 251.7 | **9.9** | 8.3 |
| C `cat` | 1 GiB to a file | 699.7 | 613.8 | 548.3 | **60.1** | 54.5 |
| C `cat` | -n, short lines | 874.4 | 898.8 | 887.5 | 910.0 | 248.8 |
| C `cat` | 64 operands | 804.2 | 841.9 | 818.1 | **25.3** | 18.4 |
| D `wc` | -l, C | 504.4 | 482.5 | 480.8 | **173.1** | 87.6 |
| D `wc` | -l, UTF-8 | 512.4 | 486.1 | 494.8 | **171.6** | 90.7 |
| D `wc` | -l, very short lines | 140.3 | 139.0 | 141.4 | **15.6** | 7.0 |
| D `wc` | default counts (30 runs) | 2069.0 | 2310.1 | 2075.6 | 2128.6 | 2023.8 |
| E `tail` | -n 10 through a pipe | 454.4 | 453.5 | 459.7 | **166.5** | 302.3 |
| E `tail` | -n 10, short lines, pipe | 137.6 | 135.9 | 138.4 | **11.2** | 79.6 |
| E `tail` | -n +1, the whole file | 139.7 | 139.8 | 143.4 | 149.8 | 131.7 |
| E `head` | -n -1 through a pipe | 1352.0 | 1326.3 | 1294.1 | 1057.6 | 361.7 |
| E `head` | -n 100000 of short lines | 1.9 | 1.8 | 1.9 | 1.8 | 1.5 |
| E `nl` | very short lines | 1022.3 | 1029.9 | 1040.5 | 1017.2 | 953.4 |
| E `nl` | ordinary lines | 2623.9 | 2636.8 | 2631.8 | 2409.0 | 2167.4 |
| E `nl` | no numbers at all | 3010.8 | 2881.4 | 2799.5 | 2755.5 | 1322.9 |
| E `uniq` | very short lines | 423.6 | 427.8 | 422.2 | 371.4 | 381.4 |
| E `uniq` | ordinary lines | 3069.3 | 3028.7 | 2679.1 | 2342.2 | 1250.0 |
| E `uniq` | a field skipped | 3588.4 | 3632.9 | 3129.6 | 2648.9 | 1606.6 |
| E `cut` | -b1-10, C | 949.2 | 940.5 | 970.9 | 698.2 | 495.1 |
| E `cut` | -f1 -d' ', C | 1316.9 | 1299.3 | 1240.7 | 951.4 | 619.4 |
| E `cut` | -b1-10, very short lines | 373.3 | 383.3 | 546.2 | 532.6 | 220.7 |
| E `cut` | -f1, very short lines | 563.9 | 543.3 | 788.3 | 735.5 | 316.9 |
| E `cut` | -b1-10 on binary noise | 154.9 | 148.6 | 160.2 | 75.2 | 50.9 |
| F `ls` | flat/, one per line | 4.0 | 4.1 | — | 4.0 | 6.4 |
| F `ls` | flat/ -C | 4.2 | 4.3 | — | 4.2 | 7.6 |
| F `ls` | -R of deep/ | 10.0 | 9.7 | — | 9.7 | 3.7 |
| #624 | `unexpand`, ordinary lines | 2820.1 | 2928.9 | — | — | 6546.8 |

A (descriptors) has no row of its own to win: its stdin rows (`head -c
-1024` / `-n -1` of stdin that is a file, `tail` of stdin, `wc -c <`)
are within noise at 30 runs (`ab-confirm-head`), and its two real moves
are `cut` and `uniq` above (wolf-lang#644).

## 4. Evidence index

Everything below is under kasumi `~/lanes/bu19/ev/` (kept; the build
trees are pruned) unless named otherwise.

- **Archives**: `archives.log` `10fd5da8…`, the six unix archives and
  every member hashed by name; identity `wolf 0.2.26 (wolfgang, pin
  89dc139)` / `paired with lupin 0.1.49 (reference interpreter), pin
  294d626`; `lupin 0.1.49 (wolf-interp, reference interpreter at pin
  294d626)`.
- **The prediction**: `7a2f552`, pushed before `archives.sh` ran.
- **Gauntlets** (fetch, both tiers, WIR, own counts, stripped hashes,
  `wolf test`, fmt, selftest, difftest on both tiers): base
  `gauntlet-base-50d8907.log` `468adc37…`, pin
  `gauntlet-pin-d39e57c.log` `7df1f40e…`, head
  `gauntlet-head-9d9cb2b.log` `8ce0b50f…`; verdict lists
  `verdicts-{release,dev}-*.txt`; WIR `wir-{base,pin}-*/` with
  `wir-*.sha256` `532121dc…`; own counts `own-*-*.txt`.
- **Bench**: `ab-cat`, `ab-fds`, `ab-wc`, `ab-split`, `ab-624`, `ab-ls`,
  `ab-confirm-wc`, `ab-confirm-head` (each a `rows.json`, a `table.md`
  and the hyperfine JSON per row; `rows.json` `8a7bd026…`, `de27c852…`,
  `593085d9…`, `498ca8ce…`, `2fcd0ee6…`, `840f1546…`, `4141486c…`,
  `39cb1f08…`); the binaries of every state in `~/lanes/bu19/bins/`.
- **Witnesses filed upstream**: wolf-lang#642 (`~/lanes/bu19/wit/copy-lost/`,
  `copy_lost.lu` `dbef39f4…`), wolf-lang#643 (`~/lanes/bu19/probe/ptyrun.py`
  `578924ef…`, `ls` `71db0e52…`), wolf-lang#644 (`bins/pin/cut`
  `f043c929…`, `bins/ab/cut` `d3a0bfcf…`, input `bench-in/lines`
  `29933fd1…`); the #624 re-measure is a comment on that issue.
- **Gates seen red**: the pty capture planted to read nothing makes
  `difftest-selftest` refuse (`selftest-plant-tty.log` `e79ed0d8…`); the
  24 terminal cases against the pin's `ls`: 21 FAIL
  (`lsF-against-pin.diff` `3fc864e4…`); **in CI**, the plant `9ecce3e`
  (`ls` asks descriptor 2) red in run **37985034764**, ubuntu job
  114004784611 (`difftest: 2996 passed, 21 failed, 60 skipped`),
  reverted in `d02941f`.
- **CI green**: run 37982011386 at `880af7f` (ubuntu 3017 / 0 / 60,
  macOS 2972 / 0 / 105, field 2951 / 16 / 110); run 37984988431 at
  `9d9cb2b`; the head's run is in the PR.

## 5. Done-when

Branch `bu19`, PR wolffe-lang/boreutils#24 open and unmerged; CI green
at the head; the worktree and kasumi's build trees removed, `ev/`,
`bins/`, `probe/` and `wit/` kept as the evidence above. Close nothing.
Filed wolf-lang#642, #643, #644; commented on #624.
