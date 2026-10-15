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
