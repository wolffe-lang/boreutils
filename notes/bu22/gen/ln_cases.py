#!/usr/bin/env python3
# bu22: writes tests/cases/ln.toml. A generator only so that the cases
# stay legible; the TOML it writes is what is committed.
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "bu21", "gen"))
from lib import Cases

c = Cases()
T = {"scratch": {"a": "A\n", "b": "B\n", "d/in": "i\n"}, "scratch_dirs": ["e"],
     "scratch_links": {"ld": "d", "dang": "nowhere", "sa": "a", "sd": "ld"}}

c.note("Usage.")
c.case("no operand", [], **T)
c.case("--help", ["--help"], compare=["exit"])
c.case("--version", ["--version"], compare=["exit"])
c.case("an invalid option", ["-Q", "a", "c"], **T)
c.case("-t with no argument", ["-t"], **T)
c.case("-t and no target", ["-t", "d"], **T)
c.case("-t twice", ["-t", "d", "-t", "e", "a"], **T)
c.case("-t and -T", ["-t", "d", "-T", "a"], **T)
c.case("-T with one operand", ["-T", "a"], **T)
c.case("-T with three operands", ["-T", "a", "b", "c"], **T)
c.case("-r without -s", ["-r", "a", "d/c"], **T)
c.case("-b is not written", ["-b", "a", "b"], skip="-b, --backup and -S are not written: refused by name, status 1", **T)
c.case("--backup=numbered is not written", ["--backup=numbered", "a", "b"], skip="-b, --backup and -S are not written: refused by name, status 1", **T)
c.case("-S is not written", ["-S", ".x", "a", "b"], skip="-b, --backup and -S are not written: refused by name, status 1", **T)

c.note("Hard links.")
for args in [["a", "c"], ["a", "b"], ["-f", "a", "b"], ["-v", "a", "c"], ["-v", "a", "d"], ["a", "d"], ["a", "ld"],
             ["-n", "a", "ld"], ["-nf", "a", "ld"], ["-T", "a", "d"], ["-T", "a", "c"], ["-t", "d", "a", "b"],
             ["-vt", "d", "a", "b"], ["--target-directory=d", "a"], ["-t", "nope", "a"], ["-t", "a", "b"],
             ["a", "b", "d"], ["a", "b", "c"], ["a", "b", "a"], ["a"], ["d/in"], ["nope", "c"], ["d", "c"],
             ["-d", "d", "c"], ["-F", "d", "c"], ["--directory", "d", "c"], ["a", "a"], ["-f", "a", "a"],
             ["a", "./a"], ["-f", "a", "./a"], ["a", ""], ["", "c"], ["a", "c/"], ["a", "nodir/c"],
             ["a", "dang"], ["-f", "a", "dang"], ["-fv", "a", "b"], ["-f", "a", "d"], ["-Tf", "a", "d"],
             ["-Tf", "a", "e"], ["-f", "a", "nodir/c"], ["sa", "c"], ["-P", "sa", "c"], ["-L", "sa", "c"],
             ["-L", "dang", "c"], ["-L", "ld", "c"], ["-P", "ld", "c"], ["ld", "c"], ["-L", "a", "c"], ["-L", "sd", "c"],
             ["--logical", "ld", "c"], ["--physical", "ld", "c"], ["-PL", "sa", "c"], ["-LP", "sa", "c"],
             ["--no-dereference", "a", "ld"], ["--no-target-directory", "a", "d"], ["--verbose", "a", "c"],
             ["--force", "a", "b"], ["a", "e/", "d/"], ["-v", "a", "b", "e"], ["dang", "c"], ["-f", "dang", "c"]]:
    c.case("hard: " + " ".join(repr(a) if a == "" else a for a in args), args, **T)
c.case("hard: into a directory that may not be written", ["a", "ro/c"], scratch={"a": "A\n"}, scratch_dirs=["ro"], scratch_modes={"ro": 0o555})
c.case("hard: -f into a directory that may not be written", ["-f", "a", "ro/c"], scratch={"a": "A\n", "ro/c": "C\n"}, scratch_modes={"ro": 0o555})
c.case("hard: a link already to the same file, -f", ["-f", "a", "h"], scratch={"a": "A\n"}, scratch_hardlinks={"h": "a"})
c.case("hard: a link already to the same file", ["a", "h"], scratch={"a": "A\n"}, scratch_hardlinks={"h": "a"})

c.note("Symbolic links.")
for args in [["-s", "a", "c"], ["-s", "a", "b"], ["-sf", "a", "b"], ["-sv", "a", "c"], ["-sfv", "a", "b"], ["-sfv", "a", "d"],
             ["-sf", "a", "ld"], ["-snf", "a", "ld"], ["-sn", "a", "ld"], ["-sn", "a", "d"], ["-sT", "d", "e"], ["-sTf", "d", "e"],
             ["-s", "nope", "c"], ["-s", "x/y", "c"], ["-s", "a", ""], ["-s", "a", "c/"], ["-s", "a", "nodir/c"],
             ["-s", "a"], ["-s", "d/in"], ["-s", "a", "d/"], ["-s", "d/", "lnk"], ["-sf", "a", "a"], ["-s", "a", "a"],
             ["-s", "x", "dang"], ["-sf", "x", "dang"], ["-s", "{scratch}/a", "c"], ["-st", "d", "a", "b", "nope"],
             ["--symbolic", "--force", "a", "b"], ["-s", "a b", "c d"], ["-sv", "q'x", "n\nl"], ["-s", "-a", "c"],
             ["-s", "--", "-a", "c"], ["-sv", "a", "b", "e"], ["-sf", "a", "e"], ["-sfT", "a", "e"], ["-sL", "sa", "c"]]:
    c.case("symbolic: " + " ".join(repr(a) if a == "" else a for a in args), args, **T)
c.case("symbolic: an empty target", ["-s", "", "c"], skip_on={"Darwin": "macOS's symlink(2) takes an empty target and GNU makes the link; wolf refuses one as invalid before asking the host ([os.fs.symlink], ruling #67 R3), and says what linux says"}, **T)
c.case("symbolic: into a directory that may not be written", ["-s", "a", "ro/c"], scratch_dirs=["ro"], scratch_modes={"ro": 0o555})

c.note("-r: relative to the link's own directory, both ends canonical.")
for args in [["-sr", "a", "d/c"], ["-sr", "a", "c"], ["-sr", "ld/in", "e/y"], ["-sr", "{scratch}/a", "c"],
             ["-sr", "{scratch}/d/in", "e/z"], ["-srv", "a", "d/c"], ["-sr", "nope", "e/q"], ["-sr", "nope/deeper", "e/q"],
             ["-sr", "a", "e"], ["-sr", "d", "e/back"], ["-sr", "e", "e/self"], ["-sr", ".", "e/dot"], ["-sr", "a", "sd/c"],
             ["--relative", "-s", "a", "d/x"], ["-srf", "b", "sa"], ["-srt", "e", "a", "d/in"], ["-sr", "dang", "e/w"],
             ["-sr", "d/in", "{scratch}/e/abs"], ["-sr", "a", "./c"], ["-sr", "./a", "./e/./c"]]:
    c.case("relative: " + " ".join(args), args, **T)

c.note("-i asks on standard error; a line beginning y or Y is yes.")
c.case("-i, yes", ["-i", "a", "b"], stdin="y\n", **T)
c.case("-i, Yes", ["-i", "a", "b"], stdin="Yes\n", **T)
c.case("-i, no", ["-i", "a", "b"], stdin="n\n", **T)
c.case("-i, end of input", ["-i", "a", "b"], **T)
c.case("-i, nothing there", ["-i", "a", "c"], stdin="n\n", **T)
c.case("-si, yes", ["-si", "a", "b"], stdin="y\n", **T)
c.case("-i then -f", ["-i", "-f", "a", "b"], **T)
c.case("-f then -i", ["-f", "-i", "a", "b"], stdin="n\n", **T)
c.case("--interactive", ["--interactive", "a", "b"], **T)
c.case("-i twice", ["-i", "-t", "e", "a", "b"], stdin="y\nn\n", scratch={"a": "A\n", "b": "B\n", "e/a": "x\n", "e/b": "y\n"})

c.write(os.path.join(os.path.dirname(__file__), "..", "..", "..", "tests", "cases", "ln.toml"),
        "# ln — GNU coreutils 9.11, black-box, on linux x86-64 and macOS arm64.\n"
        "# Written by notes/bu22/gen/ln_cases.py; this file is the record.\n"
        "#\n"
        "# ln changes the file system, so every case runs in a scratch\n"
        "# directory (tools/difftest); `files` compares each link's text and\n"
        "# `tree` its kind and link count.\n")
