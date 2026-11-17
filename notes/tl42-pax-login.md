# tl42: who, users, pinky and uptime on PAX

## Problem
On a PAX boot `who`, `users`, `pinky` and `uptime` stopped at `utmp layout
unsupported on this host`, because the layout check named only Linux on
x86-64. PAX's login writes the same 384-byte x86-64 record (pax#453), so
nothing was wrong with the records, only with the name test.

## Change
- `login_abi` accepts `pax` on x86-64 alongside Linux. An unmeasured machine
  (`pax` on aarch64) is still refused, and a unit row says so.
- With no records, `who` and `users` print nothing and exit 0. A constructed
  USER_PROCESS record is listed.
- On PAX, `uptime` checks `/proc/uptime` and `/proc/loadavg` first and names
  each one that is missing, rather than blaming the utmp layout. Neither file
  exists on a PAX boot today (`ls /proc` shows `1 meminfo net pax-boot
  pax-latency self 6 mounts partitions pax-bootlog pax-random sys`), filed as
  pax#459. Nothing is invented in their place.

## Evidence
`tests/pax-login/boot.py` boots a PAX image under QEMU and runs five rows
(`who-empty`, `users-empty`, `pinky-abi`, `uptime-sources`, `who-record`),
one command at a time over the serial console. It is red at the first commit
(`079b1b8`), green after the fix, and red on `who-empty` and `who-record` with
the one-hunk plant on branch `tl42-plant-abi`.

PAX does not yet run position-independent executables, so the image used for
the local boot carries statically linked builds of the four tools.

## Decision
R-tl42-1: accept PAX by system name plus machine, not by probing the record.
The layout is a fixed ABI, and a probe would also accept a file that merely
has the right size.
