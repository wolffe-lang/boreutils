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
