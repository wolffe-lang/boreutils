#!/usr/bin/env python3
"""bu27: carry tests/cases/kill.toml (bu23's generated cases) to wolf 0.2.32.

Every signal the host numbers is ours now (`-N`, `os_signal_text`), so:
  - the `skip_on` that said "GNU names a signal here that wolf has no
    meaning for" goes: those cases run on both hosts;
  - `gnu_keep` goes: the whole tables are compared whole;
  - the `-t` mask that hid GNU's third column now hides only the row for
    signal 0, whose words wolf cannot ask for (`os_signal_text` refuses 0).
usage: kill_cases_0232.py tests/cases/kill.toml   (rewrites it in place)
"""
import re
import sys

path = sys.argv[1]
text = open(path).read()
NOMEANING = 'GNU names a signal here that wolf has no meaning for ([os.signal.set])'
out = []
dropped = {"skip_on": 0, "gnu_keep": 0, "mask": 0}
for line in text.split("\n"):
    if line.startswith("skip_on = ") and NOMEANING in line:
        rest = re.sub(r'(Linux|Darwin) = "' + re.escape(NOMEANING) + r'"(, )?', "", line)
        rest = re.sub(r", \}$", " }", rest)
        dropped["skip_on"] += 1
        if rest.strip() in ("skip_on = {  }", "skip_on = { }", "skip_on = {}"):
            continue
        out.append(rest)
        continue
    if line.startswith("gnu_keep = "):
        dropped["gnu_keep"] += 1
        continue
    if line == 'mask = ["(?m)(?<=[A-Z][A-Z0-9])( +[A-Z][^\\\\n]*)?$"]':
        dropped["mask"] += 1
        out.append('mask = ["(?m)(?<=^ 0 EXIT)( +[^\\\\n]*)?$"]')
        continue
    out.append(line)
open(path, "w").write("\n".join(out))
print(dropped)
