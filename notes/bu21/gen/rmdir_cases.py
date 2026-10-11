#!/usr/bin/env python3
# bu21: writes tests/cases/rmdir.toml.
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
case("an empty directory", ["e"], scratch_dirs=["e"])
case("two", ["e", "g"], scratch_dirs=["e", "g"])
case("a missing name", ["missing"])
case("a directory that is not empty", ["full"], scratch={"full/x": "x\n"})
case("a directory that holds a directory", ["full"], scratch_dirs=["full/x"])
case("a file", ["f"], scratch={"f": "x\n"})
case("a link to a directory", ["l"], scratch_dirs=["e"], scratch_links={"l": "e"})
case("a link to a directory, with a slash", ["l/"], scratch_dirs=["e"], scratch_links={"l": "e"})
case("a dangling link", ["l"], scratch_links={"l": "nowhere"})
case("a dangling link, with a slash", ["l/"], scratch_links={"l": "nowhere"})
case("a link to a file", ["l"], scratch={"f": "x\n"}, scratch_links={"l": "f"})
case("a link to a file, with a slash", ["l/"], scratch={"f": "x\n"}, scratch_links={"l": "f"})
case("a file, with a slash", ["f/"], scratch={"f": "x\n"})
case("an empty name", [""])
case("the working directory", ["."])
case("a trailing slash", ["a/b/c/"], scratch_dirs=["a/b/c"])
case("a final dot", ["a/."], scratch_dirs=["a"])
case("the rest are still tried", ["g1", "g2", "g3"], scratch_dirs=["g1", "g3"], scratch={"g2/f": "x\n"})
case("names that need quoting, missing", ["q'x", "tab\tx", "sp ace", "new\nline", "é", "a\"b", "back\\slash", ""])
case("names that need quoting, removed", ["q'x", "tab\tx", "sp ace", "new\nline"], scratch_dirs=["q'x", "tab\tx", "sp ace", "new\nline"])
case("in a directory that may not be written", ["ro/in"], scratch_dirs=["ro/in"], scratch_modes={"ro": 0o555})
case("in a directory that may not be searched", ["no/in"], scratch_dirs=["no/in"], scratch_modes={"no": 0o000})
case("a directory with no permissions at all, empty", ["z"], scratch_dirs=["z"], scratch_modes={"z": 0o000})
case("-- ends the options", ["--", "-p"], scratch_dirs=["-p"])
case("a bad option", ["-x"])
case("POSIXLY_CORRECT: the first operand ends the options", ["e", "-v"], scratch_dirs=["e", "-v"], env={"POSIXLY_CORRECT": "1"})
case("an absolute path", ["{scratch}/e"], scratch_dirs=["e", "keep"])
case("the cwd is a subdirectory", ["x"], scratch_dirs=["d/x"], cwd="d")

case("-v", ["-v", "a/b"], scratch_dirs=["a/b"])
case("-v names a failure before it fails", ["-v", "e", "missing", "full"], scratch_dirs=["e"], scratch={"full/x": "x\n"})
case("-v quotes as a shell would", ["-v", "q'u", "sp ace", "new\nline", "a\"b", "c'd\"e", "#h", "é"], scratch_dirs=["q'u", "sp ace", "new\nline", "a\"b", "c'd\"e", "#h", "é"])
case("--verbose", ["--verbose", "e"], scratch_dirs=["e"])
case("--verb abbreviates", ["--verb", "e"], scratch_dirs=["e"])
case("--v is ambiguous", ["--v", "e"], scratch_dirs=["e"])
case("--verbose=1 takes no argument", ["--verbose=1", "e"], scratch_dirs=["e"])

case("-p: three levels", ["-p", "p/q/r"], scratch_dirs=["p/q/r"])
case("-p: a parent that is not empty stops it", ["-p", "p/q/r"], scratch_dirs=["p/q/r", "p/keep"])
case("-pv: the same, said", ["-pv", "p/q/r"], scratch_dirs=["p/q/r", "p/keep"])
case("-p: a trailing slash", ["-p", "p/q/r/"], scratch_dirs=["p/q/r"])
case("-pv: a trailing slash", ["-pv", "u/v/w/"], scratch_dirs=["u/v/w"])
case("-pv: doubled slashes", ["-pv", "u//v///w//"], scratch_dirs=["u/v/w"])
case("-pv: a leading ./ reaches the working directory", ["-pv", "./u/v/w"], scratch_dirs=["u/v/w"])
case("-pv: a dot in the middle", ["-pv", "u/./v/w"], scratch_dirs=["u/v/w"])
case("-pv: a final dot", ["-pv", "u/v/w/."], scratch_dirs=["u/v/w"])
case("-p: the operand is missing", ["-p", "missing/x"])
case("-p: the operand is not empty", ["-p", "full/x"], scratch={"full/x/f": "x\n"})
case("-p: one component", ["-pv", "a"], scratch_dirs=["a"])
case("-p: two operands share a parent", ["-pv", "a/b", "a/c"], scratch_dirs=["a/b", "a/c"])
case("-p: a parent may not be written", ["-p", "ro/a/b"], scratch_dirs=["ro/a/b"], scratch_modes={"ro": 0o555})
case("-p: through a link", ["-pv", "l/x"], scratch_dirs=["d/x"], scratch_links={"l": "d"})
case("-p: no operand", ["-p"])
case("--parents", ["--parents", "p/q"], scratch_dirs=["p/q"])
case("--p abbreviates", ["--p", "p/q"], scratch_dirs=["p/q"])

case("--ignore-fail-on-non-empty", ["--ignore-fail-on-non-empty", "full"], scratch={"full/x": "x\n"})
case("--ignore-fail-on-non-empty still removes an empty one", ["--ignore-fail-on-non-empty", "e", "full"], scratch_dirs=["e"], scratch={"full/x": "x\n"})
case("--ignore-fail-on-non-empty -p: a parent that is not empty", ["--ignore-fail-on-non-empty", "-p", "full/x"], scratch_dirs=["full/x"], scratch={"full/file": "x\n"})
case("--ignore-fail-on-non-empty -pv", ["--ignore-fail-on-non-empty", "-pv", "full/x"], scratch_dirs=["full/x"], scratch={"full/file": "x\n"})
case("--ignore-fail-on-non-empty forgives nothing else", ["--ignore-fail-on-non-empty", "missing", "f"], scratch={"f": "x\n"})
case("--ignore-fail-on-non-empty -v", ["-v", "--ignore-fail-on-non-empty", "g2"], scratch={"g2/f": "x\n"})
case("--ignore abbreviates", ["--ignore", "full"], scratch={"full/x": "x\n"})
case("--i abbreviates", ["--i", "full"], scratch={"full/x": "x\n"})
case("--ignore-fail-on-non-empty in a directory that may not be written", ["--ignore-fail-on-non-empty", "ro/in"], scratch_dirs=["ro/in"], scratch_modes={"ro": 0o555})
case("--ignore-fail-on-non-empty=1 takes no argument", ["--ignore-fail-on-non-empty=1", "e"], scratch_dirs=["e"])

case("--help", ["--help"], compare=["exit"])
case("--version", ["--version"], compare=["exit"])
case("--help wins over a later bad option", ["--help", "--bogus"], compare=["exit"])
case("a bad option before --help", ["--bogus", "--help"])
case("stdout closed, nothing to write", ["e"], scratch_dirs=["e"], stdout_closed=True)
case("stdout closed under -v", ["-v", "e"], scratch_dirs=["e"], stdout_closed=True)

head = '''# rmdir — GNU coreutils 9.11, black-box, on linux x86-64 and macOS arm64.
# Written by notes/bu21/gen/rmdir_cases.py; this file is the record.
#
# rmdir changes the file system, so every case runs in a scratch
# directory (tools/difftest, bu21) and what each side leaves is compared
# as `files` and `tree`. No case names a path outside it, and none
# gives -p an absolute path: its walk up would not stop at the scratch
# directory's own top.
'''
open(sys.argv[1], "w").write(head + "\n" + "\n\n".join(out) + "\n")
print(len(out), "cases")
