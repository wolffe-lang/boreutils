#!/usr/bin/env python3
# bu22: writes tests/cases/chmod.toml. A generator only so that a few
# hundred cases stay legible; the TOML it writes is what is committed.
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "bu21", "gen"))
from lib import Cases

c = Cases()
F = {"f": "x\n"}

c.note("Usage: what is missing, what is not an option.")
c.case("no operand", [])
c.case("a mode and no file", ["755"])
c.case("a symbolic mode and no file", ["u+x"])
c.case("an option mode and no file", ["-x"])
c.case("-R alone", ["-R"])
c.case("only --", ["--"])
c.case("an invalid option", ["-Q", "7", "f"], scratch=F)
c.case("an unrecognized long option", ["--bogus", "7", "f"], scratch=F)
c.case("--mode is not an option of chmod", ["--mode=644", "f"], scratch=F)
c.case("--help", ["--help"], compare=["exit"])
c.case("--version", ["--version"], compare=["exit"])
c.case("--reference with a mode", ["--reference=f", "-w", "f"], scratch=F)
c.case("--reference and no file", ["--reference=f"], scratch=F)
c.case("--reference to nothing", ["-v", "--reference=nope", "f"], scratch=F)
c.case("--reference copies", ["--reference=d", "f"], scratch=F, scratch_dirs=["d"], scratch_modes={"d": 0o751})
c.case("--reference as two words", ["--reference", "d", "f"], scratch=F, scratch_dirs=["d"], scratch_modes={"d": 0o700})
c.case("--ref abbreviates", ["--ref=d", "f"], scratch=F, scratch_dirs=["d"], scratch_modes={"d": 0o711})
c.case("--reference: the next word is a file", ["--reference=f", "700", "d"], scratch=F, scratch_dirs=["d"])
c.case("--reference with set-id bits", ["--reference=s", "f"], scratch={"f": "x\n", "s": "y\n"}, scratch_modes={"s": 0o6750})

c.note("Octal modes, on a file and on a directory.")
for m in ["755", "644", "0", "7", "70", "700", "4755", "2755", "1777", "7777", "0755", "00755",
          "000000000644", "6000", "0000"]:
    c.case(f"octal {m} on a file", [m, "f"], scratch=F)
for m in ["755", "0755", "00755", "000755", "1755", "4755", "700", "2700", "07755", "=755", "+755",
          "-2000", "-6000", "=0", "-0", "+1000"]:
    c.case(f"octal {m} on a set-group-ID directory", [m, "d"], scratch_dirs=["d"], scratch_modes={"d": 0o2755})
for m in ["17777", "8", "999", "08", "-8", "=8", "+17777", "u+0", "755,u+x", "u+x,755", "0x1ff"]:
    c.case(f"invalid octal {m}", [m, "f"], scratch=F)
c.case("an empty mode", ["", "f"], scratch=F)
c.case("operator numbers in a list", ["+755,-5", "f"], scratch=F)
c.case("a number after =, under a mask", ["=751", "f"], scratch=F, umask=0o077)
c.case("a number after +, under a mask", ["+111", "f"], scratch=F, umask=0o077)

c.note("Symbolic modes, from three starting modes, on files and directories.")
syms = ["u+x", "+x", "a+x", "-x", "=r", "a=rwx,o-w", "u=g", "go=u", "g+u,o-g", "u+s,g+s", "+s", "=s",
        "o+t", "+t", "u+t", "a+X", "u+x,a+X", "a+X,u+x", "a+xX", "ug+rw-x", "u+", "+u", "-u", "o=rw+x",
        "ugoa+r", "-r,+w", "u=,g=o", "o=u-w", "o=u+w", "=", "u=rwx,go=rx", "a=rx", "u=rx", "g=rx", "o=rx",
        "=rx", "u=s", "g-s", "-s", "-t", "a-w", "u+w,g-r,o=x", "o=g,g=u,u=o", "+X", "a=", "g+wX,o-rwx"]
for start in [0o644, 0o750, 0o6755]:
    for m in syms:
        c.case(f"{m} on a file of {start:o}", [m, "f"], scratch=F, scratch_modes={"f": start})
for start in [0o755, 0o3755]:
    for m in syms:
        c.case(f"{m} on a directory of {start:o}", [m, "d"], scratch_dirs=["d"], scratch_modes={"d": start})
for m in ["u", "a", ",", "u+r,", "u+rw,,g+r", "z+r", "u+q", "o=ug", "o+ugo", "o+ur", "u+r g+w", "U+x", "+R", "=w,"]:
    c.case(f"invalid symbolic {m}", [m, "f"], scratch=F)

c.note("With no `who`, the umask decides what +, - and = reach; s and t ignore it.\n"
       "A `-` the mask kept from clearing a bit is GNU's warning and status 1.")
for mask in [0o022, 0o077, 0o027, 0o002, 0o000, 0o777]:
    for m in ["+x", "+rw", "+w", "-w", "-r", "=rwx", "=rx", "u=rwx,=rx", "a=rwx,-w", "-r,+w", "+s", "+t", "=s", "-x", "+X", "a-r"]:
        c.case(f"{m} under the mask {mask:03o}", [m, "f"], scratch=F, scratch_modes={"f": 0o755}, umask=mask)
c.case("the warning under -v", ["-v", "-r", "f"], scratch=F, umask=0o027)
c.case("the warning under -c", ["-c", "-r", "f"], scratch=F, umask=0o027)
c.case("the warning under -f", ["-f", "-r", "f"], scratch=F, umask=0o027)
c.case("the warning, a directory and a file", ["-r", "d", "f"], scratch=F, scratch_dirs=["d"], umask=0o027)
c.case("the warning, a name with a space", ["-r", "a b"], scratch={"a b": ""}, umask=0o027)
c.case("the warning, a name with a quote", ["-r", "q'x"], scratch={"q'x": ""}, umask=0o027)
c.case("the warning, a name with a tab", ["--", "-r", "t\tb"], scratch={"t\tb": ""}, umask=0o027)
c.case("no warning when the mask is not in the way", ["-r", "f"], scratch=F, umask=0o022)
c.note("Measured: the warning is given for a MODE given as an option, never for\nthe same MODE as an operand.")
for m in ["-r", "-r,u+x", "u+x,-r", "-r,-w", "a=rwx,-w", "=rw,-w", "-w,a=rwx"]:
    c.case(f"no warning for {m} as an operand", ["--", m, "f"], scratch=F, scratch_modes={"f": 0o755}, umask=0o027)
for args in [["-r", "f"], ["-r,u+x", "f"], ["-r,-w", "f"], ["-r", "--", "f"], ["f", "-r"], ["-r", "-w", "f"], ["-w,a=rwx", "f"]]:
    c.case("the warning for an option mode: " + " ".join(args), args, scratch=F, scratch_modes={"f": 0o755}, umask=0o027)

c.note("A mode given as an option, joined with commas.")
for args in [["-w", "f"], ["-rwx", "f"], ["-x,g+w", "f"], ["-w", "-x", "f"], ["-v", "-w,u+x", "f"],
             ["-x", "f", "-w"], ["f", "-w"], ["-w", "f", "-v"], ["u+x", "-v", "f"], ["-R", "-w", "f"],
             ["-c", "-w", "-v", "f"], ["-0", "f"], ["-7", "f"], ["-u", "f"], ["-a", "f"], ["-+x", "f"],
             ["-=x", "f"], ["-,", "f"], ["-X", "f"], ["-s", "f"], ["-t", "f"], ["-g+x", "f"], ["-w+x", "f"],
             ["-rw", "-v", "-x", "f"], ["-w", "--", "-x", "f"], ["-wxr", "f"], ["-vw", "f"], ["-cw", "f"],
             ["-w", "u+x", "f"], ["-c", "--", "-w", "f"], ["--", "-w", "f"], ["-w", "--", "f"], ["755", "--", "f"],
             ["-Rv", "f"], ["-Qw", "f"], ["-x", "-"], ["-c", "u+x"], ["-R", "-w"]]:
    c.case("as options: " + " ".join(args), args, scratch=F)
c.case("as options under POSIXLY_CORRECT", ["u+x", "f", "-w"], scratch=F, env={"POSIXLY_CORRECT": "1"})

c.note("What is said: -v, -c, -f.")
c.case("-v changed", ["-v", "755", "f"], scratch=F)
c.case("-v retained", ["-v", "644", "f"], scratch=F)
c.case("-c retained says nothing", ["-c", "644", "f"], scratch=F)
c.case("-c changed", ["-c", "755", "f"], scratch=F)
c.case("--changes", ["--changes", "700", "f"], scratch=F)
c.case("--verbose", ["--verbose", "700", "f"], scratch=F)
c.case("-v, set-user-ID without execute", ["-v", "u+s", "f"], scratch=F)
c.case("-v, a sticky directory", ["-v", "1777", "d"], scratch_dirs=["d"])
c.case("-v, a sticky file without other execute", ["-v", "1644", "f"], scratch=F)
c.case("-v twice on one file", ["-v", "755", "f", "f"], scratch=F)
c.case("-v on a directory", ["-v", "-x", "d"], scratch_dirs=["d"])
c.case("-v of a missing file", ["-v", "755", "nope"], scratch=F)
c.case("a missing file", ["755", "nope"], scratch=F)
c.case("a missing file among others", ["755", "f", "nope", "g"], scratch={"f": "", "g": ""})
c.case("-f of a missing file", ["-f", "755", "nope"], scratch=F)
c.case("--quiet", ["--quiet", "700", "nope"], scratch=F)
c.case("--silent", ["--silent", "700", "nope"], scratch=F)
c.case("an empty name", ["-v", "7", "", "f"], scratch=F)
c.case("a name with a space, -v", ["-v", "755", "sp ace"], scratch={"sp ace": ""})
c.case("a name with a newline, -v", ["-v", "755", "n\nl"], scratch={"n\nl": ""})
c.case("under a file", ["755", "f/x"], scratch=F)
c.case("a trailing slash on a file", ["755", "f/"], scratch=F)
c.case("a trailing slash on a directory", ["-v", "700", "d/"], scratch_dirs=["d"])
c.case("an unsearchable parent", ["-v", "700", "p/f"], scratch={"p/f": ""}, scratch_modes={"p": 0o600})

c.note("Links handed in: followed, unless -h.")
L = {"scratch": {"f": "x\n"}, "scratch_links": {"lf": "f", "dang": "nowhere"}}
c.case("a link to a file", ["-v", "700", "lf"], **L)
c.case("a dangling link", ["-v", "700", "dang"], **L)
c.case("a dangling link, -f", ["-f", "700", "dang"], **L)
c.case("a dangling link, -R", ["-vR", "700", "dang"], **L)
c.case("-h on a link", ["-vh", "700", "lf"], skip_on={"Darwin": "GNU changes a link's own mode there (lchmod); wolf has no call that does (fs_set_mode follows a final link), so this one leaves it, as GNU does on linux"}, **L)
c.case("--no-dereference on a link", ["-v", "--no-dereference", "700", "lf"], skip_on={"Darwin": "GNU changes a link's own mode there (lchmod); wolf has no call that does"}, **L)
c.case("-h on a file", ["-h", "755", "f"], **L)
c.case("--dereference", ["--dereference", "755", "lf"], **L)
c.case("-h then --dereference", ["-h", "--dereference", "755", "lf"], **L)

c.note("-R: the directory, then what it holds; links inside are left alone unless -L.")
T = {"scratch": {"d/f": "x\n", "e/x": "y\n"}, "scratch_dirs": ["d/s", "e/sub"],
     "scratch_links": {"d/l": "../e", "ld": "e", "lf": "d/f", "d/dang": "nowhere"}}
for args in [["-vR", "700", "d"], ["-R", "700", "d", "lf"], ["-vR", "700", "lf"], ["-R", "-L", "700", "d"],
             ["-R", "-H", "700", "d"], ["-vR", "-L", "u-x", "d"], ["-cR", "755", "d"], ["-vRh", "700", "d"],
             ["-vR", "700", "ld"], ["-vR", "-H", "700", "ld"], ["-vR", "-P", "700", "ld"], ["-vR", "-L", "700", "ld"],
             ["-v", "700", "ld/"], ["-vR", "700", "ld/"], ["-vRh", "700", "ld"], ["-vR", "a-x", "d"],
             ["-vR", "000", "d"], ["-vR", "a-r", "d"], ["-R", "--preserve-root", "700", "d"],
             ["--no-preserve-root", "-R", "700", "d"], ["-R", "go-rwx", "."], ["-vR", "u+x", "d", "e"],
             ["-fR", "a-x", "d"], ["-RP", "-vL", "700", "d"], ["-RL", "-P", "700", "ld"], ["--recursive", "700", "e"],
             ["--rec", "700", "e"], ["-R", "a+X", "d"], ["-vR", "=", "e"]]:
    c.case("walk: " + " ".join(args), args, **T)
c.case("walk: the mask's warning on every entry", ["-R", "-r", "e"], umask=0o027, **T)
c.case("walk: a link back up, -L", ["-R", "-L", "700", "c"], scratch_dirs=["c/sub"], scratch_links={"c/sub/up": ".."})
c.case("walk: an empty directory", ["-vR", "700", "z"], scratch_dirs=["z"])
c.case("walk: a file", ["-vR", "700", "f"], scratch=F)

c.write(os.path.join(os.path.dirname(__file__), "..", "..", "..", "tests", "cases", "chmod.toml"),
        "# chmod — GNU coreutils 9.11, black-box, on linux x86-64 and macOS arm64.\n"
        "# Written by notes/bu22/gen/chmod_cases.py; this file is the record.\n"
        "#\n"
        "# chmod changes the file system, so every case runs in a scratch\n"
        "# directory (tools/difftest), and what each side leaves is compared:\n"
        "# `files` (names, kinds, bytes) and `tree` (modes, link counts).\n")
