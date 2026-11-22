# Changelog

## Unreleased

- `bore`: the utilities in one program, chosen by the name it is run under, or `bore NAME ARG...`; `dd`, `shred`, `sleep`, `sync`, `tail` and `timeout` stay separate programs and `bore NAME` runs the one beside it. Experimental: built and tested in CI, not in the release archives or the packages.
- The utilities' code moves into modules under `src/cmd/`, each `src/NAME.lu` a short entry; no utility's behaviour changes.
- `tools/multicalltest` holds `bore` to the separate programs (census, refusals, signal dispositions, size in loadable bytes, the PAX page bound, start-up, no signal hub or thread path, the six beside it); the gauntlet runs it and the corpus through `bore` by link and by name, and a `links` job runs the kill, identity, root and in-out tests through its links.

## 0.1.0 — 2026-11-20

- First 0.1.0 release of the implemented core utilities. Existing per-utility compatibility boundaries and named refusals remain; this is not a claim of complete GNU coreutils parity.
- Align the package manifest with the existing shared 0.1.0 CLI version. Every version-capable archived utility is checked for that version. POSIX `test` keeps its operand grammar; its unavailable version option is named explicitly.
- Require the full matrix with every suite at the exact tag before staging macOS arm64 and Linux x86-64 archives with SHA-256 sidecars as a draft.
- `users`, `who`, `pinky` and `uptime` read the x86-64 utmp layout on PAX as well as on Linux. On PAX, `uptime` names a missing `/proc/uptime` or `/proc/loadavg` and exits 1 instead of reporting invented values.
- Pin wolf 0.2.40 and lupin 0.1.62. The CI runners are pinned to ubuntu-24.04.
