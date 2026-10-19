#!/usr/bin/env python3
"""bu28: carry tests/cases/kill.toml to wolf 0.2.33 (boreutils#41 (4)).

`os_signal_text(0)` answers `strsignal(0)`'s words since 0.2.33 (s246,
wolf-lang#787): glibc's `Unknown signal 0`, macOS's `Unknown signal: 0`.
So the `-t` mask bu27 left on the row for signal 0 (`EXIT`) goes: every
`-t`/`-L`/`--table` case compares its whole output, the EXIT row's third
column included. The header's sentence about that row is rewritten.
usage: kill_cases_0233.py tests/cases/kill.toml   (rewrites it in place)
"""
import sys

path = sys.argv[1]
text = open(path).read()
MASK = 'mask = ["(?m)(?<=^ 0 EXIT)( +[^\\\\n]*)?$"]'
OLD_HEAD = """# signal (`strsignal`, which wolf asks through `os_signal_text`). The one
# row with no words here is signal 0's (`EXIT`): `os_signal_text` refuses
# 0, so the `mask` hides GNU's third column on that row only. The whole
# tables (`-l`, `-t` with no operand) are compared whole."""
NEW_HEAD = """# signal (`strsignal`, which wolf asks through `os_signal_text`), signal
# 0's (`EXIT`) included since wolf 0.2.33 (`Unknown signal 0`; bu28 took
# out the mask bu27 put on that row). The whole tables (`-l`, `-t` with
# no operand) are compared whole."""
assert text.count(OLD_HEAD) == 1, "the header sentence moved"
text = text.replace(OLD_HEAD, NEW_HEAD)
out = []
dropped = 0
for line in text.split("\n"):
    if line == MASK:
        dropped += 1
        continue
    out.append(line)
text = "\n".join(out)
OLD_GEN = """# notes/bu27/gen/kill_cases_0232.py; the help and version TEXT is"""
NEW_GEN = """# notes/bu27/gen/kill_cases_0232.py and to 0.2.33 by
# notes/bu28/gen/kill_cases_0233.py; the help and version TEXT is"""
assert text.count(OLD_GEN) == 1, "the generator line moved"
text = text.replace(OLD_GEN, NEW_GEN)
open(path, "w").write(text)
print({"mask": dropped})
