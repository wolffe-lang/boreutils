# bu24 — the ids (boreutils on wolf 0.2.30: `id`, `whoami`, `groups`, `logname`, `chown`, `chgrp`)

Lane note. **Class:** long (boreutils), **Opus**. **Crawl:** 54, batch 2.
Branch `bu24` off boreutils `9819e44` (bu23). Contract:
`sprints/boreutils/18-the-ids/bu24-the-ids.md` (planning `ae2dd72`).
§1–§3 are committed before any of GNU's six identity tools has been run
by this lane and before any line of `src/`, `tools/`, `tests/` or the
pins changes; §3 is scored in place later, never rewritten.

One deliverable: boreutils pinned to wolf 0.2.30 / lupin 0.1.53 (its own
commit), and `id`, `whoami`, `groups`, `logname`, `chown`, `chgrp`
written on 0.2.30's `os_uid` … `os_groups`, `fs_set_owner` and a pure
`/etc/passwd` / `/etc/group` reader, measured against GNU coreutils
9.11's own binaries in throwaway `--network none` containers, as root
and as a user that container defines, both tiers, ubuntu and macOS (macOS
by CI); static binaries and their system calls for PAX (P5 U6); plants.

## 1. Forbidden

- **No implementation's source is read**: not GNU coreutils', not glibc's
  (`getlogin`, `getgrouplist`, `initgroups`), util-linux's, shadow's,
  busybox's, uutils', toybox's. GNU's behaviour comes from its `--help`,
  its info manual (`id invocation`, `chown invocation`, …), POSIX.1-2024,
  the `passwd(5)`, `group(5)`, `utmp(5)` and `getlogin(3)` manual pages,
  and black-box runs (and `strace`) of the GNU coreutils 9.11 BINARIES
  built from the oracle tarball by digest. **Which binary answered is
  recorded**, and which package owns the one each image ships.
- **No id or owner changes on any host.** Every case that runs as a user
  other than the caller, or that can change an owner, runs in a fresh
  `--network none` container the test made, with nothing of the host
  mounted, as container root and as a user that container's own
  `/etc/passwd` defines. No account is made on a host; no `sudo`.
  `tools/difftest` (which runs on hosts) refuses any `chown`/`chgrp`
  case that names a file. CI's macOS leg, which has no engine, runs only
  on the throwaway runner, as the runner, on files the case itself made,
  and the tool refuses that mode anywhere but GitHub Actions.
- No `rm` outside `~/lanes/bu24/` (nomad-1 and kasumi); no deletion in a
  tree this lane did not make; no `git add -A`; nothing under
  `~/.claude`; no edit to another lane's file; no merge, no tag, no issue
  filed or closed; no attribution trailer; no `2>/dev/null` on a
  checkout; the branch asserted before every commit.
- The toolchain from the RELEASE ARCHIVES by digest, each read twice; the
  archive's `std/` removed before the pin's own is staged. No build on
  nomad-1. kasumi's login shell is fish (`bash -c`); `setsid` with a pid
  file; a job is killed by its recorded pid only. `/home` is near full:
  prune as I go, remove this lane's images at the end. Scratch under
  `~/lanes/bu24/`, never `/tmp`.
- Strict evidence (wolf-lang#571): `wolf build` exit 2 is a compile
  error; SKIP lines counted over the full output; no "seen red" without
  a run id, sha, path or digest. No other lane's run cancelled. Waits
  inline, printing at least every five minutes. A harness refusal stops
  the lane and is reported.

## 2. Inputs, verified (2026-10-15, origin and the release archives)

| input | origin says | verdict |
|---|---|---|
| boreutils trunk `9819e44` | `origin/trunk` is `9819e449…` (bu23); 40 `src/*.lu` entries (not `_test`); 6,514 `[[case]]` tables in `tests/cases/`; 0 open PRs; pin wolf 0.2.29 / lupin 0.1.52, std `9e5bd6b` | holds. **Drift:** trunk's own push run 38355253341 at `9819e44` is RED on macOS, one case, `ls: a terminal with -m: quoted, no alignment space` — boreutils#27 (the macOS pty flake), not a regression; ubuntu and the field leg green |
| wolf 0.2.30 is `v0.2.30` at `1b37f368`; lupin 0.1.53 is `v0.1.53` at `7896edd` | `git rev-parse v0.2.30^{}` = `1b37f368228d…`, `v0.1.53^{}` = `7896eddc17fd…`, each read twice | holds |
| the release archives | fetched on kasumi, each hashed twice (`~/lanes/bu24/ev/archives.log`), equal to the release API's digests: wolf linux x86-64 `4e55b39e…` (79,910,152 B), linux arm64 `34237d4a…`, macOS arm64 `f3257e74…`; lupin linux x86-64 `5db55332…`, linux arm64 `7874ec27…`, macOS arm64 `997b71a5…`. `_wolf` `a368c8ec…` in all three. `wolf 0.2.30 (wolfgang, pin 1b37f36)` / `paired with lupin 0.1.53 …, pin 294d626`; `lupin 0.1.53 (wolf-interp, reference interpreter at pin 294d626)` | holds |
| the bundled std is wolf-std `fd6bcdc` | `std/STD-REV` in the linux x86-64 archive is `fd6bcdcb1dfe…`; wolf-std `trunk` is `fd6bcdc` | `[std]` expected to move `9e5bd6b` → `fd6bcdc` (B151 first) |
| `std.os.users` in the pinned std | **absent**: `fd6bcdc` has `std/os/os.lu` only; the reader and the id wrappers are wolf-std#65 (OPEN, draft, "waits for the release") | **boreutils' own reader** (`src/bore/ids.lu`, grown); the builtins called directly, as the CHANGELOG says |
| the 0.2.30 CHANGELOG | eleven new prelude names (`fs_set_owner`, `fs_set_owner_fd`, `os_uid`, `os_euid`, `os_gid`, `os_egid`, `os_groups`, `os_set_ids`, `os_term_size`, `os_term_chars`, `os_signal_wait_fd`); a grep of boreutils `9819e449` found no declaration, one use in a census probe (not built); capabilities: the reads `env`, the owner calls `fs` | holds |
| spec `[os.proc.ids]`, `[os.fs.owner]`, `[os.proc.ids.note]` at `v0.2.30` | the five reads `-> int ! {unsupported}` / `List[int] ! {io, unsupported}`; `os_groups` is `getgroups` as the host answers (linux lists the egid only if set so); `fs_set_owner(path, uid, gid, follow) -> () ! {denied, invalid, io, not_found, unsupported}`, `-1` leaves an id, `follow` false is `AT_SYMLINK_NOFOLLOW`; `invalid` also the host's `EINVAL` for an unmapped id. **lupin serves the two owner calls and refuses the five reads and `os_set_ids` by name** | holds |
| boreutils#32 | OPEN: "missing: id, whoami, groups, logname, chown, chgrp" | closes at merge (by hand) |
| boreutils#28 | OPEN (`cat f >> f`); needs wolf-lang#722 and #536, both OPEN | expected not to move |
| bu23's harness | PR #30 read; `tools/killtest` (one fresh container a case, a base image plus the programs copied in, GNU beside, `setpriv` for the user), the GNU oracle built in `localhost/px12-ubuntu` from the tarball | the template for `tools/idtest` |
| s236 (wave-53) | wolf-lang `e6bb122b` merged; witnessed in throwaway containers; rulings R1–R10 made (#78) | holds |
| pax `notes/px38-the-users.md` | Ubuntu 24.04's coreutils 9.4 traced: `id` = `geteuid, getuid, getegid, getgid, getgroups(0), getgroups(n)` and `/etc/passwd`, `/etc/group` (plus nsswitch, `/proc/filesystems`, nscd socket); `whoami`/`id -u` `geteuid`; `chown`/`chgrp` `fchownat(AT_FDCWD, f, uid, -1|gid, 0)`, `-R` `getdents64` | holds |
| hosts | kasumi: 16 cores, `/home` 27 G free (98 %), load 42 at 08:52Z (other lanes), podman 6.1.3, `localhost/px12-ubuntu` (Ubuntu 24.04.5, coreutils 9.4-3ubuntu6.3 owns `/usr/bin/{id,whoami,groups,logname,chown,chgrp}` by `dpkg -S`; has gcc, strace, useradd, setpriv, python3). My kasumi session: `SigBlk 0`, `SigIgn 0`, loginuid 4294967295 | holds |

## 3. Prediction (committed before GNU's six are run and before the first change)

What GNU does is predicted from its manual, POSIX and memory, and is the
part most likely to be wrong.

1. **The pin** (own commit): wolf 0.2.30 / lupin 0.1.53 by the digests
   above; `[std]` to `fd6bcdc` (B151: `9e5bd6b` and `fd6bcdc` both build
   all 40 on both tiers under `--deny-warnings`). No W0304, no new E1010
   (no utility spawns a proc). The verdict list of the 40 at the pin is
   byte-identical to trunk's under the same harness in the same box.
   Every binary's bytes move (`RT_SYMBOLS` 214). Falsified by one
   diagnostic or one line.
2. **`id`**: `uid=U(name) gid=G(name) groups=…`, `euid=`/`egid=` only
   when they differ; `-u -g -G`, `-n`, `-r`, `-z`, `-a` (ignored), a USER
   operand (by name, then by number), several USERs one line each; a
   USER's groups are its primary group then every `/etc/group` line
   naming it, in file order; an id with no name prints bare, and `-un` of
   one says `cannot find name for user ID N` with status 1. `-Z` refused
   as GNU built `--without-selinux` refuses it. Falsified by GNU listing
   a USER's groups in any other order, or the process's groups in an
   order other than egid then `getgroups` with repeats dropped.
3. **`whoami`** is `id -un` with its own messages; **`groups`** is `id
   -Gn` (`USER : g1 g2` with operands).
4. **`logname`**: on linux GNU's answer comes from `/proc/self/loginuid`
   (a name for that uid), else the utmp record of standard input's
   terminal, else `logname: no login name`, status 1. In a container
   with no login it says `no login name`. Ours reads the same files with
   no builtin. **On macOS** `getlogin` is a kernel call wolf cannot make:
   refused by name, skipped there by name; a wolf issue is owed.
5. **`chown` / `chgrp`**: `OWNER[:[GROUP]]`, `:GROUP`, `OWNER:` (the
   login group), `OWNER.GROUP` (obsolete), numbers for names, `+N` as a
   number; `--from=`, `--reference=`, `-c`, `-v`, `-f`, `-h`,
   `--dereference`, `-R` with `-H`/`-L`/`-P` (`-P` the default), `--
   preserve-root`. GNU skips the call when nothing would change only for
   `--from` mismatches, and otherwise always calls `fchownat`, so `-v`
   says `retained as` and `-c` says nothing. Messages `changed ownership
   of 'f' from a:b to c:d` / `changed group of 'f' from a to b`;
   `changing ownership of 'f': Operation not permitted`; `invalid user:
   'x'`, `invalid group: 'x'`. A user may `chgrp` a file it owns to a
   group it is in and nothing else.
6. **The counts:** 40 utilities become **46**. About 250 `difftest`
   cases for the six that change nothing on a host (read-only `id`,
   `whoami`, `groups`, `logname`; `chown`/`chgrp` usage and refusals),
   and about 250 container cases (`tools/idtest`) as root and as a user,
   0 failed, every skip named; macOS skips every name-printing case
   (its accounts are in the directory service: `accounts = true`). No
   verdict of the 40 moves. Release and dev answer alike.
7. **The harness:** a new `tools/idtest` in `tools/killtest`'s shape:
   one fresh `--network none` container a case, accounts (users,
   groups, an id with no name, a user in several groups) defined in the
   image the tool builds, a tree laid out as root with owners, the
   program run as root or as a user by `setpriv`, the tree's owners and
   modes read back and compared with GNU's side. A plant must fail by
   name.
8. **The four machines:** native and release run every case. A witness
   unit file: the checked machine (`wolf conform-run --json --checked`)
   answers the reads and the owner call as native does; **lupin serves
   `fs_set_owner` and refuses `os_uid` … `os_groups` by name**; the pure
   reader answers on all four.
9. **boreutils#28 does not move.**
10. **For PAX:** static `id` makes `getuid`, `geteuid`, `getgid`,
    `getegid`, `getgroups` (twice) and reads `/etc/passwd` and
    `/etc/group` with `openat`/`read`; no nsswitch, no socket, no
    `/proc/filesystems`. `chown`/`chgrp` make `fchownat` (one a file)
    after `statx`/`newfstatat`; `-R` adds `getdents64`. `logname` opens
    `/proc/self/loginuid`. Beside the start-up set and `statx` on
    descriptor 1, nothing else. Falsified by any other name.
11. **Planted breaks**, red in CI on their own branches, each on its
    named case: `chown -h` following the link; `id -G` dropping the
    effective group.
12. **CI green** on ubuntu and macOS at the head.
13. One thing here is wrong in a way this list does not name.

## 3a. The prediction, scored

§3 above is as it was committed (`0d231b2`, before any of GNU's six had
been run by this lane and before the first change). Scored in place, by
line. "A container" is a fresh `--network none` container on kasumi
(podman 6.1.3) with nothing of the host mounted unless named; the
accounts in every one are the image's own (`tools/idtest`'s `ACCOUNTS`:
alice 1001 in pack, crew and zeta; bob 1002 with login group pack; carol
1003 named by `crew2` and `pack2`; `twin` repeating 1001; `dot.ty`;
ghost 3000; ids 4242 and 4243 that nothing names). **GNU in every line
is `~/lanes/bu24/gnu-build/out/bin/`**, GNU coreutils 9.11 built in
`localhost/px12-ubuntu` from the oracle tarball (`394024ed…`, read
twice) with the pin file's configure line (`ev/gnu-ubuntu.log`). In that
image `dpkg -S` gives `/usr/bin/{id,whoami,groups,logname,chown,chgrp}`
to Ubuntu's coreutils 9.4-3ubuntu6.3: never the oracle.

| # | predicted | measured | verdict |
|---|---|---|---|
| 1 | the pin by digest; std to `fd6bcdc` after B151; no diagnostic; the 40's list unmoved; every binary moves | digests as §2 (`ev/archives.log`); one list, `4cca7ca46318f541…` 6252 / 0 / 262 on both tiers, at trunk on 0.2.29 (`ev/gauntlet-trunk-9819e44.log`), at the pin with std `9e5bd6b` (`gauntlet-pin-ecdf2f2.log`) and with `fd6bcdc` (`gauntlet-pin-ecdf2f2-fd6bcdc.log`); 0 diagnostics in 80 builds each; 80 of 80 binaries differ from 0.2.29's, 40 of 80 between the two stds. At the head the 40's lines are still `4cca7ca46318f541…` (`gauntlet-w2.log`, the six's lines taken out) | right |
| 2 | `id`'s formats; a USER's groups in file order; the process's list as egid then `getgroups`; `-Z` refused | the default format, `euid=`/`egid=`, missing names, `-n`/`-r`/`-z` refusals and `-Z` as predicted (`ev/probe-p1.log`). **Wrong:** `-G` for the process is the REAL group first, then the effective one, then the list (the default line has no real group: `groups=` starts at the effective one). **Not predicted:** a USER's groups are found by the LINE's name (`id twin` prints `uid=1001(alice)` and only `groups=1001(alice)`); `id 1001` and `id +1001` find a user by number where `groups 1002` says `no such user`; `-Gz` with more than one USER ends each list with one more NUL (`ev/probe-p4.log`); the order of the refusals (`-Z` first); on macOS GNU appends `: Invalid argument` to `'nosuch-bu24': no such user` (CI run 38749117948) | right on the shapes, wrong on `-G`'s order, five rules not predicted |
| 3 | `whoami` is `id -un`, `groups` is `id -Gn` | as predicted, but for `groups`'s name-only lookup (line 2) | right |
| 4 | `logname`: loginuid, then utmp for standard input's terminal, else `no login name`; macOS refused by name | the order as predicted, under `strace` (`ev/probe-p2.log`). **Not predicted:** the record's user is printed AS WRITTEN (`zed`, whom `/etc/passwd` does not know); a `LOGIN_PROCESS` record counts; a record whose user is empty prints an empty line, status 0; standard input not a terminal is `no login name` whatever utmp holds. A RECORDED loginuid was on no host this lane had, so that branch is not measured | right, with four rules not predicted |
| 5 | the spec grammar, the always-made call, `-v`'s words, a user's `chgrp` | the call is made for an unchanged owner and for `:` and `''` (the set-ID bits go, `ev/probe-p3.log`), and skipped only on a `--from` mismatch: right. **Wrong in nine ways** (`ev/probe-p3.log`, `probe-p4.log`, `idtest-t1.log`): NEW keeps a NAME only for a part written as one (`1001:pack` says `:pack`, `1001:2000` says `1001:2000`); `chown :2000` is worded as `chgrp` words it; `nosuch:` and `1002:` are `invalid spec`; `-v` and `-c` are ONE setting, the last wins; a spec with neither part that fails says `failed to change ownership of 'F'`; `--from`'s spec warns about a `.` too; `-R` changes a directory AFTER its entries, with OLD as the walk first read it; under `-RH` an inner link is followed for the change and not walked; under `-RL` OLD is the walk's record (the target, or the link where there is none) even when `-h` changes the link; a directory that cannot be listed is not changed at all. **And GNU 9.11 prints an uninitialized owner** for a link to nothing it follows (`from 2445336480 to alice`, a different number each run) | right on the calls, wrong on the words |
| 6 | 46 utilities; ~250 host cases and ~250 container cases, 0 failed, every skip named; the 40 unmoved; release = dev | **46**; **131** host cases (`tests/cases/`, ubuntu 131 / 0 / 0, macOS see §4) and **1,126** container cases (1,098 run on linux: 615 as root, 483 as users, 0 failed; 28 for CI's macOS runner); release and dev answer alike on every case (`gauntlet-w2.log`, `idtest-w2.log`) | right on the rule, low on the counts by 4x in the container |
| 7 | `tools/idtest` in killtest's shape; a plant fails by name | `tools/idtest` and `tools/idtest-selftest` (four plants: an owner, an account, the actor, the terminal; a control). **Not predicted:** three sides in ONE container a case (as killtest's note says, not three containers), each on a fresh `/work`; `logname`'s terminal is one `script` session that reads its own line, writes the utmp records as root and runs the actor; `gnu_sub` for GNU's uninitialized owner | right |
| 8 | checked = native = release; lupin serves `fs_set_owner`, refuses the reads by name; the pure reader on all four | `ev/machines-w2.log`: `ids_test.lu` and `owner_rows_test.lu` `exit(0)` on all four; `ids_rows_test.lu` `exit(0)` on checked, native and release and `unsupported` on lupin by name (`os_uid` … `R10`). **Not predicted:** before `var n: int`, lupin trapped `overflow` in `bore.id_number` where the other three answered (wolf-interp#173; `ev/lupin-i32-witness.log`) | right, after one trap |
| 9 | boreutils#28 does not move | it does not (wolf-lang#722 and #536 open) | right |
| 10 | static: the id calls and the two files; `fchownat`; `getdents64` under `-R`; nothing else | `ev/static.log`: as predicted, and no nsswitch, no socket, no `/proc/filesystems`. **Not predicted:** `id` makes all five reads whatever is asked (`id -u` too); every account file and loginuid is `openat` + `statx` + `read`; `logname` is `ioctl(TCGETS)` on 0, `readlink(/proc/self/fd/0)`, `openat(/var/run/utmp)`. **Caught by the trace:** the first build passed `AT_SYMLINK_NOFOLLOW` for a plain file (equivalent, but GNU passes 0); fixed before the head | right but for the details |
| 11 | two plants red in CI on their own branches, each on its named case | `bu24-plant-G` (`ca7efb9`, `id` leaves the effective group out): run 38749187354 red on ubuntu at the differential step, 6388 / 2 / 255, the two failures `id: (none)` and `id: -a` (macOS cannot see it: its runner's own groups skip, and the run met the 9.12 drift of §4). `bu24-plant-h` (`1587a84`, `chown -h` follows the link): run 38751408576 red on both hosts at the identity step — ubuntu `idtest` 997 / 101 / 28 (`-h`, `-R`, `-P`), the macOS runner's `self` cases 23 / 5. Never merged; the branches are left for the audit | right |
| 12 | CI green on both hosts at the head | green at `efb51c3`, run 38751387617 (attempt 2; §4 says why attempt 1's macOS leg was re-run). The first head run, 38749117948 at `c8fd11e`, was red on two things, both fixed: `idtest-selftest` used `echo "$out"`, and ubuntu's `/bin/sh` (dash) reads its backslashes (`155a08f`); and macOS's errno line (line 2, `efb51c3`) | right at the second head |
| 13 | one thing wrong this list does not name | four. (d) CI's macOS runners do not all ship one Homebrew coreutils: run 38749187354's had **9.12**, so `tools/fetch-oracle` built 9.11 for everything and boreutils#31's `printf '\u0000'` case went red there (B44's cost (a), met). And three (a) dash's `echo` (line 12). (b) The sides of a case share one container, so a case that changes `/` itself — `chown -v --preserve-root alice /`, no `-R` — changed it for the sides after GNU's (`idtest-t1.log`): removed; every other case changes only `/work`, laid out again for each side. (c) lupin's `i32` (line 8) | — |

## 4. Evidence index

Shas are this branch's (`bu24`). kasumi paths are under `~/lanes/bu24/`;
a digest's first twelve characters follow a log. CI logs are on nomad-1
under `~/lanes/bu24/ci/`.

- **The prediction:** `0d231b2`. **The pin:** `ecdf2f2`, `bff477c`,
  `d25a586`; `ev/archives.log` `d81bd0ea47f4`,
  `ev/gauntlet-trunk-9819e44.log` `c2c3dc74263f`,
  `ev/gauntlet-pin-ecdf2f2.log` `16fc8936408f`,
  `ev/gauntlet-pin-ecdf2f2-fd6bcdc.log` `bf70b693c804`.
- **The oracle:** `ev/gnu-ubuntu.log` `9d1482568402` (the tarball read
  twice, the build, `--version` of the six, `dpkg -S` of the image's
  six = coreutils 9.4); the six's digests: `id` `112be4de7e9e`,
  `whoami` `b4e538e7bb42`, `groups` `8bc676e2a08e`, `logname`
  `55d1a390d1d5`, `chown` `e0a54a4314c0`, `chgrp` `5dc79f4da4be`.
- **GNU measured** (each probe one fresh `--network none` container of
  `localhost/bu24-probe`, accounts its own; scripts `probes/p1.sh` …
  `p6.sh`): `ev/probe-p1.log` `1585343c3339` (the readers, nine actors,
  70 operand forms), `probe-p2.log` `d9b6ad1ddbc5` (`logname` under
  `strace`, utmp records), `probe-p3.log` `368a0fff02c7` (`chown` and
  `chgrp`, 130 forms, every tree read back), `probe-p4.log`
  `0fb9376d9b76` (NEW's words for names and numbers; `-z` with several
  users), `probe-p6.log` (`kill -l N`, §4's macOS flake).
- **The code:** `56839f4` (the reader), `217d5cf` (`id`, `whoami`,
  `groups`, `logname`), `baea1a8` (`chown`, `chgrp`); **the harness:**
  `97f8e30` (`tools/difftest` refuses a `chown`/`chgrp` case naming a
  file; three plants under `tests/refuse/owner-*`), `e47bdbc`
  (`tools/idtest`, `tools/idtest-selftest`), `b4bc492` (the cases and
  their generators, `notes/bu24/gen/`), `52da579` (CI), `155a08f`,
  `efb51c3` (the two fixes from run 38749117948).
- **The gauntlet at the code's head** (`c8fd11e`; `155a08f` and
  `efb51c3` change a selftest's `echo` and add one macOS skip, and CI
  ran them): `ev/gauntlet-w2.log` `71bce28e4d4a` — 46 built on both
  tiers with no diagnostic, fmt, `wolf test` 7 of 7, the suite **6,383
  passed, 0 failed, 262 skipped on release and on dev**, one list
  `4644afb15f38b6d3…`; with the six's lines taken out it is trunk's
  `4cca7ca46318f541…` (the 40 unmoved); the selftest (the three
  `owner-*` plants refused), the evidence gate, the field-verdict
  selftest. `difftest-release-w2.log` `b7c6daba0fac`,
  `difftest-dev-w2.log` `8073d2f31212`.
- **`tools/idtest`** (podman, `docker.io/library/ubuntu:24.04`, the six
  static on both tiers built in px12-ubuntu, GNU beside them):
  `ev/idtest-w2.log` `c06d617f54ec` — `idtest-selftest` saw its four
  plants and passed its control; **1,098 passed, 0 failed, 28 skipped**
  (the 28 are the macOS runner's). By actor:

  | utility | as root | as a user | CI's macOS runner (`self`) |
  |---|---|---|---|
  | `id` | 149 / 0 | 279 / 0 | — |
  | `whoami` | 9 / 0 | 10 / 0 | — |
  | `groups` | 29 / 0 | 33 / 0 | — |
  | `logname` | 20 / 0 | 26 / 0 | — |
  | `chown` | 288 / 0 | 85 / 0 | 14 / 0 |
  | `chgrp` | 120 / 0 | 50 / 0 | 14 / 0 |
  | **all** | **615 / 0** | **483 / 0** | **28 / 0** |

  Users here are alice, bob, carol, dot.ty, a user with no name (4242),
  real and effective ids split two ways, a user with no supplementary
  groups, a group with no name, and `twin` (1001 by number).
  Earlier runs kept: `idtest-t1.log` `e40dd1d7b55f` (75 differences that
  taught §3a line 5), `idtest-t2.log` `d2ce24531f86` (8).
- **Case counts against GNU, per host and tier** (passed / failed /
  skipped; release and dev alike on every row):

  | where | the six on a host (`tools/difftest`) | the six in containers (`tools/idtest`) | the whole suite |
  |---|---|---|---|
  | kasumi, px12-ubuntu box | 131 / 0 / 0 | 1,098 / 0 / 28 | 6,383 / 0 / 262 |
  | CI ubuntu, run 38751387617 | 131 / 0 / 0 | 1,098 / 0 / 28 (docker) | 6,390 / 0 / 255 |
  | CI macOS, run 38751387617 (attempt 2) | 95 / 0 / 36 | 28 / 0 / 1,098 (`--engine none`) | 6,327 / 0 / 318 |

  The 36 macOS skips: 30 cases that print a name the directory service
  holds (`accounts`: `id` 22, `groups` 5, `whoami` 3), `logname`'s 4,
  `id -u > /dev/full` (no `/dev/full` there), and the errno line (§3a
  line 2).
- **The four machines:** `ev/machines-w2.log` `961e5150ec06` (§3a line
  8): `src/ids_test.lu` (the reader and the spec, pure) `exit(0)` on
  `wolf conform-run --json --checked`, `--native`, `--release` and
  `lupin conform-run --json`; `src/ids_rows_test.lu` (the five reads)
  `exit(0)` on checked, native, release, `unsupported` by name on lupin;
  `src/owner_rows_test.lu` (`fs_set_owner`'s rows) `exit(0)` on all
  four. `ev/lupin-i32-witness.log` `eff6b62c78ee` (wolf-interp#173).
- **The static binaries for PAX** (`ev/static.log` `e9850a3749f8`):
  kasumi `~/lanes/bu24/static-pax/release/`, built in px12-ubuntu (gcc
  13.3.0, glibc 2.39) through a `cc` that adds `-static`, never against
  kasumi's glibc; each `statically linked`, no INTERP, about 13.9 MB:
  `id` `bbc99826fc0b2ba3bf9f2fdb97d0aaa78f3bd7a9280f0e0366c1d32275b18a82`,
  `whoami` `c764dc0d4e22939c8070e430aaf04ea5ae1b3ec1078fbb3b9b6787b0fa623be6`,
  `groups` `c6ce8b91d118c5dd560fc62dc72cf981aabadc2f4b404680b8b64c4470dc5a8d`,
  `logname` `998049af3bac258e0416edec73895eec129d8fbc09625d85b7f885f0257bcd5c`,
  `chown` `71ee01029ed28371adfe06daccf3e848009884e88c1f16f3d7a3d01bc03d9ba1`,
  `chgrp` `f7cafb34c03ab29dafa2071569e36731cb58b48b7d65b816f5c3cba35c665343`.
  Nineteen runs under `strace -f` in a fresh container of the probe
  image (as root, and as alice by `setpriv` with the trace started
  inside it):
  - every run: `execve`, `brk` ×5, `arch_prctl`, `set_tid_address`,
    `set_robust_list`, `rseq`, `prlimit64`, `readlinkat`
    (`/proc/self/exe`), `getrandom`, `mprotect`, `statx` (descriptor 1,
    `AT_EMPTY_PATH`), `exit_group`; `write` when it prints;
  - the account files: `openat` + `statx` (the descriptor) + `read` of
    `/etc/passwd` and `/etc/group`, every tool but `logname` (no
    nsswitch, no socket, no `/proc/filesystems`);
  - `id`, `groups` (no operand): `getuid`, `geteuid`, `getgid`,
    `getegid` (all of them, whatever is asked), `getgroups(0)` then
    `getgroups(n)`; `whoami`: `geteuid`; `id USER`, `groups USER`: no
    id call;
  - `logname`: `openat` + `read` of `/proc/self/loginuid`,
    `ioctl(0, TCGETS)`; on a terminal also `readlink("/proc/self/fd/0")`
    and `openat` + `read` of `/var/run/utmp`;
  - `chown`, `chgrp`: `statx(AT_SYMLINK_NOFOLLOW)` of the operand, then
    `fchownat(AT_FDCWD, F, uid | -1, gid | -1, 0)`, or
    `AT_SYMLINK_NOFOLLOW` under `-h`; `-R` adds `openat(O_DIRECTORY)`
    and `getdents64` per directory, and the directory's `fchownat`
    comes after its entries'; `--reference` one more `statx`; refused
    as alice: `fchownat` = `-EPERM`, then `write`.
  - nothing else: no thread, signal, `futex`, `poll` or socket.
  **For PAX (U6):** the six need `getuid`/`geteuid`/`getgid`/`getegid`/
  `getgroups`, `fchownat` with flags 0 and `AT_SYMLINK_NOFOLLOW`
  (`-EPERM` and `-EINVAL` as its refusals), `getdents64`, `statx`,
  `readlink` of `/proc/self/fd/0`, `ioctl(TCGETS)`, and the files
  `/etc/passwd`, `/etc/group`, `/proc/self/loginuid`, `/var/run/utmp`.
  Not run on PAX by this lane.
- **The plants** (§3a line 11): `ca7efb9` red in run 38749187354;
  `1587a84` red in run 38751408576 (its first cut `56263d0`, on the
  head before `155a08f`, was cancelled by this lane before it ran, run
  38749181789, because its ubuntu leg would have gone red at the
  selftest for the wrong reason).
- **CI:** green at `efb51c3`, run 38751387617, attempt 2. **Attempt 1's
  macOS leg was red** on one case of bu23's `tools/killtest`, `placing:
  {pid0} -l` on the dev tier (`PIPE` where GNU said `invalid signal`),
  and its ubuntu leg was green; the whole failed job was re-run once.
  The case's answer depends on the process id the runner hands out:
  `kill PID -l` reads PID as an exit status, and on linux `kill -l N`
  agrees with GNU for every N from 0 to 140,000 beyond bu23's designed
  refusals (`ev/probe-p6.log`), so the difference is macOS's, for some
  N past 255. Nothing of this lane touches `kill`. Also seen: run
  38749187354's macOS runner shipped Homebrew coreutils **9.12** and
  went red on boreutils#31's `printf` case; the head's runner shipped
  9.11. Earlier: 38749117948 at `c8fd11e` (§3a line 12).

### What the six cannot do yet, and the wolf issue each needs

No issue was filed by this lane. Searched 2026-10-15 (wolf-lang, wolf-std,
wolf-interp): none exists for 1 or 2; 3 and 4 are open.

1. **The login name on macOS** — *new wolf-lang issue*. There
   `getlogin(2)` asks the KERNEL for the session's login name (no file
   holds it), and wolf has no call for it. `logname` refuses by name on
   macOS (`logname: wolf cannot ask this host for the login name`,
   status 1); its host cases skip there by name. Asked for:
   `os_login_name() -> str ! {not_found, unsupported}` — linux reading
   what `getlogin` reads (loginuid, then utmp) or left to the program,
   macOS the kernel's answer.
2. **Accounts outside `/etc/passwd` and `/etc/group`** — *new wolf-std
   issue, or wolf-std#65's `std.os.users` grown*. macOS keeps every
   ordinary user in its directory service, LDAP/NIS/systemd's dynamic
   users likewise: there `id USER` says `no such user`, `whoami` says
   `cannot find name for user ID N` and `chown NAME` says `invalid
   user`, where GNU (through the C library's name service) answers. A
   pure reader cannot see them; a lookup through the host is a builtin
   (`getpwnam`/`getgrouplist`) or a ruling that boreutils stays with the
   two files. Every case that prints a name is `accounts = true` and
   skips on macOS.
3. **`std.os.users` and the ids wrappers are not in the pinned std**
   (wolf-std#65, OPEN, a draft): the six call the builtins directly and
   carry their own reader (`bore.read_accounts`). Owed at the next std
   pin: adopt `std.os.users` if it answers as this reader does on the
   cases here.
4. **lupin keeps `var n = 0` an `i32`** after a later use types it
   `int` — wolf-interp#173 (OPEN), met again: `bore.id_number` trapped
   `overflow` on lupin at a ten-digit id where checked, native and
   release answered (`ev/lupin-i32-witness.log`). Worked around with
   `var n: int`, named in CLAUDE.md.
5. **A non-UTF-8 argument** aborts the runtime in `env_args` —
   wolf-lang#406 (open); a non-UTF-8 name met under `-R` is reported and
   skipped (#687); the walk is by path (#707).
6. **SELinux contexts**: `id -Z` is refused as the oracle of record
   (built `--without-selinux`) refuses it; a context-aware `id` needs
   an extended-attribute read (#685).

For the orchestrator, **one boreutils issue, not filed**: `kill -l N`
(and so `kill PID -l`) on macOS names a signal for some N past 255 where
GNU 9.11 says `invalid signal` — a pid-dependent flake in `killtest`'s
`placing: {pid0} -l` (run 38751387617, attempt 1).

### Ruling #83 and two drifts on CI's macOS runners (2026-10-15)

- **Homebrew coreutils 9.12.** Runs 38749187354 and 38761140234 (both
  attempts) drew macOS runners whose Homebrew ships 9.12, so
  `tools/fetch-oracle` built 9.11 from source for every utility, and
  that build prints `\u0000` for `printf '\u0000'` where GNU 9.11 on
  linux and Homebrew's 9.11 print a NUL (boreutils#31). **Ruling #83**
  (the maintainer, under B44): hold the real NUL. `5cc32ca`:
  `tools/difftest` gains `oracle_build_differs = { HOST = "why" }`, a
  named SKIP on that host ONLY when GNU's program is the staged source
  build (`.gnu-bin/`), and the one `printf` case carries it with the
  ruling and #31; boreutils' `printf` is unchanged; on linux and against
  Homebrew's 9.11 the case still runs (kasumi box: `ok printf: \u for a
  NUL and DEL`, 270 / 0 / 0). Seen as the named skip in run 38777228646
  (macOS 6,326 / 0 / 319). B44 stands. boreutils#31 closes at merge.
- **hyperfine 2.0.0.** The same run's macOS runner poured hyperfine
  2.0.0 (the green run 38751387617 had 1.20.0), and `tools/bench`
  crashed (`KeyError: 'boreutils'`): 2.0.0 runs a command without a
  shell unless asked, and its JSON (schema 2) keeps the `-n` name in
  `name` and the times under `summary.time_wall_clock`. `7b09f02`
  fix: `--shell default` for 2.x, and both
  schemas read by name. Measured on kasumi with each version on `cat`,
  `wc` and `ls`: 36 table rows each (`ev/bench-hyperfine.log`; 2.0.0 is
  the release's musl binary, sha256 `38e59087bd65…`, read from the
  release API).

## 5. Done-when

- [x] Branch `bu24`, PR wolffe-lang/boreutils#33, unmerged; five sections.
- [x] The pin, its own commits (`ecdf2f2`, `bff477c`, `d25a586`); the archive's `std/` removed before the pin's own is staged (`tools/fetch-toolchain`, unchanged).
- [x] `id`, `whoami`, `groups`, `logname` on `os_uid` … `os_groups` and boreutils' own reader (`bore.read_accounts`; the pinned std has no `std.os.users`).
- [x] `chown`, `chgrp` on `fs_set_owner`: `-R`, `-h`, `--reference`, `--from`, `-v`/`-c`, `--dereference`/`-H`/`-L`/`-P` as GNU has them.
- [x] Cases against GNU coreutils 9.11's own binaries as root and as users, in throwaway `--network none` containers; no id or owner changed on a host; both tiers; ubuntu and macOS (macOS by CI).
- [x] No regression in the 40 (the list unmoved, §4).
- [x] Static binaries for PAX and their system calls (§4).
- [x] Plants red in CI (38749187354, 38751408576), on their own branches, never merged.
- [x] boreutils#28: unmoved, open. boreutils#32: closes at merge, by hand.
- [x] CI green at `efb51c3` (38751387617); after ruling #83 and the hyperfine fix, the head's own run and the audit's exit status are in the PR.
- [x] Ruling #83 (boreutils#31): the real NUL held; a named skip only against macOS's source-built oracle.
- Utility count: **46** of GNU's 103.
- No issue filed or closed (#32 and #31 close at merge, by hand). For the orchestrator: two wolf issues to file (a login-name call; accounts beyond the two files), one boreutils issue (macOS `kill -l N`), and one more sighting of wolf-interp#173.
