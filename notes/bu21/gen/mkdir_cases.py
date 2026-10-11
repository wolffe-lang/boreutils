#!/usr/bin/env python3
# bu21: writes tests/cases/mkdir.toml. A generator only so that a
# hundred cases stay legible; the TOML it writes is what is committed.
import json, sys
out = []
def case(name, args, **kw):
    lines = ["[[case]]", f"name = {json.dumps(name)}", "args = " + json.dumps(args)]
    for k, v in kw.items():
        if k == "comment":
            lines.insert(0, "\n".join("# " + l for l in v.split("\n")))
        elif k == "umask":
            lines.append(f"umask = 0o{v:03o}")
        elif k == "scratch_modes":
            lines.append("scratch_modes = { " + ", ".join(f"{json.dumps(a)} = 0o{b:03o}" for a, b in v.items()) + " }")
        elif isinstance(v, dict):
            lines.append(f"{k} = {{ " + ", ".join(f"{json.dumps(a)} = {json.dumps(b)}" for a, b in v.items()) + " }")
        else:
            lines.append(f"{k} = {json.dumps(v)}")
    out.append("\n".join(lines))

case("no operand", [])
case("one directory", ["a"])
case("two directories", ["a", "b"])
case("a directory that exists", ["a"], scratch_dirs=["a"])
case("a file is in the way", ["f"], scratch={"f": "x\n"})
case("a missing parent", ["x/y/z"])
case("the rest are still made", ["a", "b", "a", "c"], scratch_dirs=["a"])
case("a trailing slash", ["t/"])
case("a trailing slash on a file", ["f/"], scratch={"f": "x\n"})
case("inside an existing directory", ["d/e"], scratch_dirs=["d"])
case("under a file", ["f/x"], scratch={"f": "x\n"})
case("an empty name", [""])
case("the working directory", ["."])
case("a link to a directory is in the way", ["l"], scratch_dirs=["d"], scratch_links={"l": "d"})
case("a dangling link is in the way", ["l"], scratch_links={"l": "nowhere"})
case("through a link to a directory", ["l/x"], scratch_dirs=["d"], scratch_links={"l": "d"})
case("a directory that may not be written", ["ro/x"], scratch_dirs=["ro"], scratch_modes={"ro": 0o555})
case("a directory that may not be searched", ["no/x"], scratch_dirs=["no"], scratch_modes={"no": 0o000})
case("a name with a space", ["sp ace"])
case("names that need quoting, taken", ["q'uote", "a\"b", "tab\tx", "new\nline", "é", "back\\slash"],
     scratch_dirs=["q'uote", "a\"b", "tab\tx", "new\nline", "é", "back\\slash"])
case("-- ends the options", ["--", "-p"])
case("a name that begins with a dash, refused as an option", ["-x"])
case("POSIXLY_CORRECT: the first operand ends the options", ["pc", "-v", "pc2"], env={"POSIXLY_CORRECT": "1"})
case("the cwd is a subdirectory", ["x"], scratch_dirs=["d"], cwd="d")
case("an absolute path", ["{scratch}/abs"])
case("an absolute path that exists", ["{scratch}/d"], scratch_dirs=["d"])

# -v
case("-v", ["-v", "a"])
case("-v, several", ["-v", "a", "b", "c"])
case("--verbose", ["--verbose", "a"])
case("--verb abbreviates", ["--verb", "a"])
case("--v is ambiguous", ["--v", "a"])
case("-v says nothing of a failure", ["-v", "a", "b"], scratch_dirs=["a"])
case("-v with a trailing slash", ["-v", "e/"])
case("-v quotes as a shell would", ["-v", "q'uote", "a\"b", "c'd\"e", "tab\tx", "#h", "e=f", "plain", "é", "a'b c", "sp ace", "new\nline"])
case("-v after the operands", ["a", "-v"])
case("--verbose=1 takes no argument", ["--verbose=1", "a"])

# -p
case("-p: three levels", ["-p", "x/y/z"])
case("-p: all of it exists", ["-p", "x/y/z"], scratch_dirs=["x/y/z"])
case("-p: part of it exists", ["-p", "x/y/z"], scratch_dirs=["x"])
case("-p: an existing directory is no error", ["-p", "a"], scratch_dirs=["a"])
case("-p: a file is in the way", ["-p", "f"], scratch={"f": "x\n"})
case("-p: a file is in the way, with a slash", ["-p", "f/"], scratch={"f": "x\n"})
case("-p: under a file", ["-p", "f/x"], scratch={"f": "x\n"})
case("-p: deep under a file", ["-p", "f/x/y"], scratch={"f": "x\n"})
case("-p: a file in the middle", ["-p", "d/f/x"], scratch={"d/f": "x\n"})
case("-p: the rest are still made", ["-p", "a/n1", "f/n2", "a/n3"], scratch={"f": "x\n"})
case("-p: an empty name", ["-p", ""])
case("-p: the working directory", ["-p", "."])
case("-p: ./", ["-p", "./"])
case("-p: dot components", ["-p", "./t/./u"])
case("-p: a final dot", ["-p", "d/new/."], scratch_dirs=["d"])
case("-p: doubled slashes", ["-p", "t//u///"])
case("-p: a link to a directory", ["-p", "l"], scratch_dirs=["d"], scratch_links={"l": "d"})
case("-p: through a link to a directory", ["-p", "l/x/y"], scratch_dirs=["d"], scratch_links={"l": "d"})
case("-p: a dangling link", ["-p", "l"], scratch_links={"l": "nowhere"})
case("-p: through a dangling link", ["-p", "l/x"], scratch_links={"l": "nowhere"})
case("-p: a link to a file", ["-p", "l"], scratch={"f": "x\n"}, scratch_links={"l": "f"})
case("-p: through a link to a file", ["-p", "l/x"], scratch={"f": "x\n"}, scratch_links={"l": "f"})
case("-p: a directory that may not be written", ["-p", "ro/x/y"], scratch_dirs=["ro"], scratch_modes={"ro": 0o555})
case("-p: a directory that may not be searched", ["-p", "no/sub/x"], scratch_dirs=["no/sub"], scratch_modes={"no": 0o000})
case("-p: a new name in a directory that may not be searched", ["-p", "no/new"], scratch_dirs=["no"], scratch_modes={"no": 0o000})
case("-p: the directory that may not be searched, itself", ["-p", "no"], scratch_dirs=["no"], scratch_modes={"no": 0o000})
case("-p: deep in a directory that may not be searched", ["-p", "ok/no/a/b"], scratch_dirs=["ok/no"], scratch_modes={"ok/no": 0o000})
case("-p: an absolute path", ["-p", "{scratch}/x/y"])
case("-p: no operand", ["-p"])
case("--parents", ["--parents", "x/y"])
case("--p abbreviates", ["--p", "x/y"])
case("--parents=1 takes no argument", ["--parents=1", "x"])

# -pv
case("-pv: each one made is named", ["-pv", "p/q/r"])
case("-pv: only the ones made", ["-pv", "p/q/r", "p/q/s"], scratch_dirs=["p"])
case("-pv: nothing made, nothing said", ["-pv", "p/q"], scratch_dirs=["p/q"])
case("-pv: the last is the operand as typed", ["-pv", "t//u///"])
case("-pv: a trailing slash", ["-pv", "a/b/", "a//c", "a/./d/"])
case("-pv: dot components are not named", ["-pv", "./t/./u"])
case("-pv: a final dot", ["-pv", "d/new/."], scratch_dirs=["d"])
case("-pv: through a link", ["-pv", "l/in"], scratch_dirs=["d"], scratch_links={"l": "d"})
case("-pv: a failure between two successes", ["-pv", "a/b", "ro/x", "c/d"], scratch_dirs=["ro"], scratch_modes={"ro": 0o555})
case("-pv: under a file, then another", ["-pv", "f/x/y", "g"], scratch={"f": "x\n"})
case("-pv: names that need quoting", ["-pv", "a b/c'd", "new\nline/x"])
case("-v -p given apart and twice", ["-v", "-p", "deep/er", "-v"])
case("-p quotes a failure as an error does", ["-p", "a b/c'd/x"], scratch={"a b/c'd": "x\n"})

# the mask
case("a mask of 077", ["a"], umask=0o077)
case("a mask of 027 under -p", ["-p", "a/b/c"], umask=0o027)
case("a mask of 077 under -p", ["-p", "a/b/c"], umask=0o077)
case("a mask of 000", ["-p", "a/b"], umask=0o000)
case("a mask that takes the owner's write: one directory", ["a"], umask=0o277)
case("a mask that takes the owner's write: -p", ["-p", "a/b/c"], umask=0o277,
     skip="GNU gives a missing parent u+wx whatever the mask says; wolf cannot read or set the mask (wolf-lang#704), so the parent gets the mask's mode and the host refuses the next component",
     comment="What this mkdir cannot match, named: see the header of src/mkdir.lu.")
case("a mask that takes the owner's search: -p", ["-p", "a/b"], umask=0o177,
     skip="GNU gives a missing parent u+wx whatever the mask says; wolf cannot read or set the mask (wolf-lang#704)")
case("a mask that takes the owner's write: -p of one new component", ["-p", "a"], umask=0o277)

# -Z, --context
case("-Z is accepted", ["-Z", "z"])
case("-Zv", ["-Zv", "z"])
case("-pZ on a directory that exists", ["-pZ", "z"], scratch_dirs=["z"])
case("--context alone is accepted", ["--context", "z"])
case("--context=CTX warns and carries on", ["--context=foo", "z"])
case("--contex=CTX abbreviates", ["--contex=x", "z"])
case("-Z with no operand", ["-Z"])

# -m: refused by name
REF = "a directory's mode cannot be set in wolf 0.2.27 (wolf-lang#346): -m is refused by name, status 1, and nothing is made"
case("-m 700", ["-m", "700", "m"], skip=REF, comment="-m: refused by name (wolf-lang#346).")
case("-m attached", ["-m755", "m"], skip=REF)
case("--mode=u+x,g-w", ["--mode=u+x,g-w", "m"], skip=REF)
case("-m 0", ["-m", "0", "m"], skip=REF)
case("-m a=rwxt", ["-m", "a=rwxt", "m"], skip=REF)
case("-pm 700: the parents take the mask, the last the mode", ["-pm", "700", "pm/a/b"], skip=REF)
case("-m with an invalid mode", ["-m", "999", "m"], skip=REF + " (GNU says: invalid mode '999')")
case("-m with no argument", ["-m"])
case("--mode with no argument", ["--mode"])

# help, version, bad options
case("--help", ["--help"], compare=["exit"])
case("--version", ["--version"], compare=["exit"])
case("--help wins over a later bad option", ["--help", "--bogus"], compare=["exit"])
case("a bad option before --help", ["--bogus", "--help"])
case("an unknown long option", ["--bogus", "a"])
case("stdout closed, nothing to write", ["a"], stdout_closed=True)
case("stdout closed under -v", ["-v", "a"], stdout_closed=True)

head = '''# mkdir — GNU coreutils 9.11, black-box, on linux x86-64 and macOS arm64.
# Written by notes/bu21/gen/mkdir_cases.py; this file is the record.
#
# mkdir changes the file system, so every case runs in a scratch
# directory whether it names one or not (tools/difftest, bu21), and what
# each side leaves is compared twice: `files` (names, kinds, bytes) and
# `tree` (modes, link counts). No case names a path outside it.
#
# What this mkdir cannot match is named, never imitated:
#   wolf-lang#346  no mode at creation and no chmod: -m is refused (skips)
#   wolf-lang#704  no umask: under -p a missing parent gets the mask's
#                  mode, not GNU's u+wx (two skips, under masks that take
#                  the owner's write or search)
'''
open(sys.argv[1], "w").write(head + "\n" + "\n\n".join(out) + "\n")
print(len(out), "cases")
