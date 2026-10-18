#!/usr/bin/env python3
"""bu27: carry tests/kill/cases.toml to `kill`'s groups (wolf 0.2.31's
os_signal_send_group / os_signal_send_all).

  - every "group:" case that recorded GNU's answer (`expect`) and refused
    BY DESIGN (`ours`) loses its `ours`: both tiers are compared with GNU;
    a `group = true` case whose only id is its own `{pgid}` also becomes
    `runner = true` (its group is the case's, so the macOS runner runs it);
  - the cases of `-1` (every process) are handed to GNU (`gnu = false` and
    `ours` go): they run in a fresh container only, where every process is
    the case's own and the container's process 1 is spared by the host;
  - the cases of `0` stay `ours`, BY DESIGN: the case's script is the
    container's process 1, so `kill` runs in group 1, which wolf never
    names (`[os.signal.send.group]`); GNU's answer is recorded as `expect`
    by --record and pasted in. `kill 0` in a group of its own is the new
    `lead` cases, compared with GNU.
usage: kill_sends_0232.py tests/kill/cases.toml   (rewrites it in place)
"""
import re
import sys

path = sys.argv[1]
text = open(path).read()
head, _, rest = text.partition("[[case]]")
blocks = ["[[case]]" + b for b in rest.split("[[case]]")]
OLD = "a process group cannot be signalled: wolf sends to one process, an id above 0 ([os.signal.send])"
NEW = "this process is in group 1, which wolf never signals ([os.signal.send.group])"
out = []
counts = {"ours dropped": 0, "runner": 0, "minus one handed to GNU": 0, "zero kept by design": 0}
for b in blocks:
    name = re.search(r'^name = "(.*)"$', b, re.M).group(1)
    args = re.search(r'^args = (.*)$', b, re.M).group(1)
    if OLD not in b:
        out.append(b)
        continue
    lines = b.rstrip("\n").split("\n")
    is_zero = re.search(r'"[ +-]?0+"', args) and "-1" not in args and "{pgid}" not in args and "4000" not in args
    is_minus_one = '"-1"' in args or '" -1"' in args
    if is_minus_one:
        lines = [l for l in lines if not l.startswith("ours = ") and l != "gnu = false"]
        counts["minus one handed to GNU"] += 1
    elif is_zero:
        lines = [l.replace(OLD, NEW) if l.startswith("ours = ") else l for l in lines]
        lines = [l for l in lines if l != "gnu = false"]
        counts["zero kept by design"] += 1
    else:
        lines = [l for l in lines if not l.startswith("ours = ")]
        counts["ours dropped"] += 1
        if "group = true" in lines and re.fullmatch(r'\[("[^"0-9]*\{pgid\}"|"-[A-Za-z]+"|"-s"|"[A-Z]+"|"--"|"-\{n:[A-Z]+\}"|, )*\]', args):
            lines.insert(lines.index("group = true") + 1, "runner = true")
            counts["runner"] += 1
    out.append("\n".join(lines) + "\n\n")
text = head + "".join(out)
text = text.rstrip("\n") + "\n"
open(path, "w").write(text)
print(counts)
