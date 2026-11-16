# Changelog

## 0.1.0 — 2026-11-15

- First 0.1.0 release of the implemented core utilities. Existing per-utility compatibility boundaries and named refusals remain; this is not a claim of complete GNU coreutils parity.
- Align the package manifest with the existing shared 0.1.0 CLI version. Every version-capable archived utility is checked for that version. POSIX `test` keeps its operand grammar; its unavailable version option is named explicitly.
- Require the full matrix with every suite at the exact tag before staging macOS arm64 and Linux x86-64 archives with SHA-256 sidecars as a draft.
