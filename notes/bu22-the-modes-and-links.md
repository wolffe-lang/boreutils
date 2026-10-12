# bu22 — the modes and links (chmod, touch, ln, mkdir -m, cp -p)

Lane note. **Class:** long (boreutils), **Opus**. **Wave:** 53. Branch
`bu22` off boreutils `abc59f5` (bu21). §1–§3 are committed before any
probe of the new builtins is run and before any line of `src/` or
`tools/` changes; §3 is scored in place later, never rewritten.

One deliverable: boreutils on wolf 0.2.28 with `chmod` (octal and
symbolic modes), `touch` (`-a`, `-m`, `-c`, `-d`/`-t`/`-r` as far as
parsing allows, `-h`), `ln` (`-s`, `-f`, `-n`, `-T`; `-L`/`-r` if a
resolver in wolf is in reach, else refused by name), `mkdir -m` and
`cp -p` (mode, both times; owner refused by name pending wolf-lang#701 and
#633), each differential against GNU coreutils 9.11 as the existing
utilities are; boreutils#28 fixed if it is one condition, else its scope
filed; the PAX-facing note.

## 1. Forbidden

- **GNU coreutils source is never read**, nor busybox's, uutils' or
  toybox's. GNU's behaviour comes from its `--help`, its manual's option
  descriptions, POSIX.1-2024 and black-box runs of the staged 9.11
  oracle. No `extern "c"`.
- **The utilities under test that change files run only in throwaway
  containers** with nothing of the host mounted but scratch under
  `~/lanes/bu22/` (bu21's `tools/roottest` shape): on kasumi, podman,
  `localhost/px12-ubuntu` (Ubuntu 24.04, glibc 2.39; never kasumi's own
  glibc), `--network none`, one bind mount of `~/lanes/bu22/`, as this
  user (`--userns=keep-id`) unless a case is about root. GNU 9.11 is
  built from its tarball by digest inside that image
  (`~/lanes/bu22/gnu-build/out`). On CI the runner is the throwaway
  machine. No changer runs on a host directly, this lane's or GNU's.
- No `rm` outside `~/lanes/bu22/` and this lane's private clones; no
  deletion in any tree this lane did not create; no `git add -A`;
  nothing under `~/.claude`; no edit to another lane's file; no merge,
  no tag, no attribution trailer; no `2>/dev/null` on a checkout.
- The toolchain from the RELEASE ARCHIVES by digest, never a clone,
  Homebrew or `~/.local/bin`. No build on nomad-1 (the commits are made
  there and rsynced; nothing is compiled or run there). kasumi and hasu
  have fish as the login shell (`bash -c`; hasu `env bash`); `setsid`
  with a pid file; kill by recorded pid only. kasumi's `/home` is near
  full (37 GB free at the start): one build tree, pruned as it goes.
  Scratch under `~/lanes/bu22/`, never `/tmp`.
- Strict evidence (wolf-lang#571): counts read from full output, SKIP
  counted; `wolf build` exit 2 is a compile error, never a skip. No
  "seen red" without a run id, sha, path or digest. At most two CI runs
  of this lane at once; no other lane's run cancelled. Waits are inline
  and print at least every five minutes.

## 2. Inputs, verified (2026-10-12, origin and the release archives)

| input | origin says | verdict |
|---|---|---|
| boreutils trunk `abc59f5` (bu21) | `origin/trunk` is `abc59f5`; 36 `src/*.lu` entries; pin wolf 0.2.27 / lupin 0.1.50, std `87ba162`; 4,594 cases | holds |
| wolf 0.2.28 / lupin 0.1.51 release archives | tags `v0.2.28` → `f71ece8e`, `v0.1.51` → `f72e78d7`. Downloaded on kasumi and hashed (`~/lanes/bu22/ev/archives.log`): wolf linux x86-64 `3215f321…`, macOS arm64 `656ab553…`, linux arm64 `f2697a69…`; lupin linux x86-64 `d8f62dd1…` (the CHANGELOG's `PAIRING` digest), macOS arm64 `2b11a7d1…`, linux arm64 `e29d02bf…`. `_wolf` hashes `a368c8ec…` in all three wolf archives (unchanged since 0.2.25). `wolf --version`: `wolf 0.2.28 (wolfgang, pin f71ece8)` / `paired with lupin 0.1.51 …, pin 294d626`; `lupin 0.1.51 (wolf-interp, reference interpreter at pin 294d626)` | holds |
| the 0.2.28 CHANGELOG's downstream step for boreutils | "the toolchain digests (remove the staged `.wolf-bin/std` before unpacking its own std pin, as at 0.2.27). `chmod`, `touch`, `ln`, `mkdir -m` and `cp -p` can be written on the new builtins." `tools/fetch-toolchain` has removed the archive's `std/` since `f18bbe8` (bu20) | holds; nothing to change in the tool |
| the archive's std | `std/STD-REV` in all three wolf archives is `98e1b7bc…` (sc58), which is also wolf-std `trunk`. wolf-std#62 (s230's wrappers) is a DRAFT, unmerged | candidates for `[std]`: `87ba162` (the pin) and `98e1b7b`; the builtins are called directly, the repository's convention, so no wrapper is needed |
| the eight builtins (s230, PR wolf-lang#712, merged `7d85c701`; ruling #67) | `fs_set_mode(path, mode)` follows a link, `0..=0o7777`; `fs_open_perm(path, open, mode)` and `fs_create_dir_mode(path, mode)`, `0..=0o777` less the umask; `fs_symlink(target, path)`, target verbatim, empty `invalid`; `fs_link(existing, path)`, never replaces, never follows a final link; `fs_set_times(path, as, ans, ms, mns, follow)`, `-1` now, `-2` leave; `fs_truncate(fd, len)`; `os_umask(mask)` sets and answers the old one. Capabilities `fs` ×7, `env` ×1: boreutils has no `wolf.pkg` | holds |
| s230's six probes (hasu `~/lanes/s230/probes/`, log `probes-a.log`) | `chmod 755`, `touch -d @…`/`-h`/now, `ln -s`, `ln`, `mkdir -m 775` under 027 and `2750`, `cp -p` — each matched GNU 9.11 on mode, times to the nanosecond, link and bytes, on one host. **Read there, not in its PR:** GNU's hard-link failure is `failed to create hard link 'h2': File exists` — no `=> 'h'` — where the probe printed one | holds; the probes are ~20 lines and parse nothing |
| boreutils#28 | OPEN: `cat < f >> f` appends until the disk is full, GNU says `cat: -: input file is output file`, status 1. Its upstream half is wolf-lang#536 (no device and inode off a handle: `fs_fstat` is `[kind, size, modified_ms]`) | open; see §3 line 9 |
| oracle | GNU coreutils 9.11, `coreutils-9.11.tar.xz` `394024ed…` (matches `gnu-oracle.toml`), built in px12-ubuntu, `touch (GNU coreutils) 9.11` (`ev/gnu-ubuntu.log`) | holds |
| hosts | kasumi: 16 cores, btrfs `/home` 97% used, podman with `localhost/px12-ubuntu` (python 3.12, gcc, make, git, strace; no `xz`). hasu: 20 cores, 281 GB free | holds |

## 3. Prediction (committed before the first probe and the first change)

Each line names what is expected and what would falsify it.

1. **The pin** (its own commit): wolf 0.2.28 / lupin 0.1.51 by the
   digests above; std moves to `98e1b7b` (B151: both `87ba162` and
   `98e1b7b` build all 36 utilities on both tiers with
   `--deny-warnings`). No W0304 from the eight new names (no
   declaration of one in `src/`), no new E1010 (0.2.28's censuses moved
   no boreutils row). The verdict list at the pin is byte-identical to
   trunk's under the same harness, in the same container. Falsified by
   a diagnostic or one line of the list.
2. **`chmod`** ships: octal modes (1–4 digits, and GNU's `=`, `+`, `-`
   numeric prefixes), symbolic modes (`[ugoa]*` then one or more
   `[-+=]` with `rwxXst` or one of `ugo`, comma lists), a mode given as
   an option (`-w`, `-rwx`, `-x,g+w`), `-c`, `-f`, `-v`, `-R`,
   `--reference`, `--preserve-root`/`--no-preserve-root`, and `-H`,
   `-L`, `-P` for the walk. With no `ugoa` a symbolic change honours the
   umask, and a bit the umask kept from being set is GNU's warning and
   status 1. A link met in the walk is neither changed nor reported.
   **Refused by name:** `-h`/`--no-dereference` on a link (no builtin
   changes a link's own mode; linux has none either). About 130 cases,
   0 failed, under 10 skipped. Falsified by a mode bit that differs.
3. **`touch`** ships `-a`, `-m`, `--time=WORD`, `-c`, `-f` (ignored),
   `-h`, `-r`, `-t [[CC]YY]MMDDhhmm[.ss]` and `-d` for: `@SECONDS[.N]`,
   `YYYY-MM-DD`, `YYYY-MM-DD[T ]hh:mm[:ss[.N]]` with an optional `Z`,
   `UTC`, `GMT` or numeric zone, a bare `hh:mm[:ss]`, `now`, `today`,
   `yesterday`, `tomorrow`; local time from the zone's TZif file
   (`bore.clock`). Every other date GNU's grammar takes is **refused by
   name** (status 1, nothing touched). `touch -` (the handle form,
   wolf-lang#714) is refused by name. Both times compared to the
   nanosecond. About 110 cases, 0 failed, under 15 skipped.
4. **`ln`** ships `-s`, `-f`, `-i`, `-n`, `-T`, `-t`, `-v`, `-P`, `-L`
   (the target's links resolved by `bore.paths`), `-r` (relative to the
   link's directory, both ends made canonical by `bore.paths`).
   **Refused by name:** `-d`/`-F` (a hard link to a directory),
   `-b`/`--backup`/`-S` (not written). `-f` removes, then links: not
   GNU's atomic replace, invisible to a test. About 110 cases, 0
   failed, under 8 skipped; macOS parts on an empty symlink target
   (the host takes one, the builtin answers `invalid`): one skip there.
5. **`mkdir -m`** ships, every mode `chmod` reads (symbolic ones from
   `a=rwx`, not from the umask); the result is exactly the mode, the
   umask notwithstanding. bu21's seven `-m` skips become passes, and its
   two umask skips too: a parent made by `-p` gets `u+wx` over the
   mask's mode, the mask read with `os_umask` (set and put back).
   About 30 new cases. Falsified by a mode that differs.
6. **`cp -p`** and `--preserve[=mode,timestamps]` ship: the mode
   exactly (set-id bits included), both times to the nanosecond, a
   directory's times set after its contents. **The owner is refused by
   name** when the source's owner or group is not what the copy was
   made with (#701, #633); `--preserve=ownership` likewise,
   `links`/`xattr`/`context`/`all` and `-a` refused by name. The bu21
   refusal of a file whose mode creation could not give (an executable,
   a private file) is RETIRED: a new file is made with the source's
   mode by `fs_open_perm`, so its bu21 skips become passes. About 45
   new cases, 0 failed.
7. **The harness** gains a sixth field for scratch cases, `times`
   (opt-in, `times = true`): every entry's access and modification
   time to the nanosecond, a link's own, and a time inside the case's
   own window compared as `now` rather than as a number. A plant in
   `tests/selftest/` must fail on it. And a container runner for the
   changers (`tools/boxtest`): build and difftest inside a throwaway
   container, nothing of the host mounted but the tree and a scratch
   root.
8. **The counts:** 36 utilities become **39** (`chmod`, `touch`,
   `ln`). The corpus grows by about 420 cases; no verdict of the 36
   moves except the bu21 skips named in lines 5 and 6, which become
   passes. Falsified by any other line of the list moving.
9. **boreutils#28.** GNU's refusal is ONE condition: the input and the
   output are the same regular file (device and inode) and the output's
   offset is before the input's end — so `cat f >> f`, `cat < f >> f`
   and `cat f 1<> f` are all refused, and `cat f > f` (truncated,
   empty) is not. wolf can ask it: `fs_stat("/dev/stdout")` names fd 1's
   file on linux (`/dev/fd/1` on macOS), and `fs_tell(1)` its offset.
   So it is FIXED here, in `cat`, with cases. Falsified by GNU copying
   `cat f 1<> f`, which would make the append flag part of the
   condition — and no builtin answers it, which is filed scope instead.
10. **Planted breaks**, one per utility, each red in CI on its named
    case and green after the revert: `chmod` taking `fs_stat` for
    `fs_lstat` in the walk (follows a link out); `touch -a` setting
    both times; `ln -f` not removing the old name; `mkdir -m` leaving
    the umask applied; `cp -p` dropping the nanoseconds.
11. **CI green** on ubuntu and macOS at the head. macOS parts from
    linux in the host's words (`os_error_text`, measured per case, not
    predicted) and nowhere in a mode or a time.
12. **For PAX**: the static binaries make `fchmodat` (`chmod`,
    `mkdir -m`, `cp -p`), `utimensat` (`touch`, `cp -p`), `symlinkat`
    and `linkat` (`ln`), `umask` (`mkdir -p -m`), `mkdirat` with a mode,
    `openat` with a mode. px27's in-memory tree has no modes, no times
    and no links yet: none of the five runs there as written, each said
    by syscall.
13. One thing here is wrong in a way this list does not name.
