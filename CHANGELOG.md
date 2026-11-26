# Changelog

## 0.1.0 — 2026-11-20

- First 0.1.0 release of the implemented core utilities. Existing per-utility compatibility boundaries and named refusals remain; this is not a claim of complete GNU coreutils parity.
- Align the package manifest with the existing shared 0.1.0 CLI version. Every version-capable archived utility is checked for that version. POSIX `test` keeps its operand grammar, and `false` exits 1 after printing its version as GNU's does; the release check names both explicitly.
- Require the full matrix with every suite at the exact tag before staging macOS arm64 and Linux x86-64 archives with SHA-256 sidecars as a draft. The release workflow uses the shared release infrastructure at `183a4e18`, whose smoke job can read the draft it staged.
- The archives carry `LICENSE` (GPL-3.0-or-later). The wolf Training Data Permission in `LICENSE-TRAINING-DATA` covers this repository's text and is not in the archives.
- `users`, `who`, `pinky` and `uptime` read the x86-64 utmp layout on PAX as well as on Linux. On PAX, `uptime` names a missing `/proc/uptime` or `/proc/loadavg` and exits 1 instead of reporting invented values.
- `sort`: a plain byte-order sort of 4,096 lines or more compares cached eight-byte key prefixes first. On a million-line input it used about 17 % less CPU than before, with peak memory inside its bound. It stays single-threaded.
- Pin wolf 0.2.40 and lupin 0.1.62; the archives are built with them. The CI runners are pinned to ubuntu-24.04.
- `bore`: the utilities in one program, chosen by the name it is run under, or `bore NAME ARG...`; `dd`, `shred`, `sleep`, `sync`, `tail` and `timeout` stay separate programs and `bore NAME` runs the one beside it. Experimental: built and tested in CI, not in the release archives or the packages.
- The utilities' code moves into modules under `src/cmd/`, each `src/NAME.lu` a short entry; no utility's behaviour changes.
- `tools/multicalltest` holds `bore` to the separate programs (census, refusals, signal dispositions, size in loadable bytes, the PAX page bound, start-up, no signal hub or thread path, the six beside it); the gauntlet runs it and the corpus through `bore` by link and by name, and a `links` job runs the kill, identity, root and in-out tests through its links.
- `tools/fetch-toolchain` tries a refused download three more times, five seconds apart; the pinned digests still decide what is accepted.
