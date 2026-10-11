#!/usr/bin/env python3
# bu21: writes tests/cases/rm.toml.
import sys
from lib import Cases
C = Cases(); case = C.case
F = {"f": "hi\n"}
T = {"d/a": "a\n", "d/sub/b": "b\n", "d/sub/deep/c": "c\n"}   # a small tree

C.note("--- files")
case("no operand", [])
case("a file", ["f"], scratch=F)
case("two files", ["f", "g"], scratch={"f": "1\n", "g": "2\n", "keep": "3\n"})
case("a missing name", ["missing"])
case("a missing name among files", ["f", "missing", "g"], scratch={"f": "1\n", "g": "2\n"})
case("an empty name", [""])
case("a file named twice", ["f", "f"], scratch=F)
case("a name under a file", ["f/x"], scratch=F)
case("a file with a trailing slash", ["f/"], scratch=F)
case("a file with two trailing slashes", ["f//"], scratch=F)
case("an empty file", ["e"], scratch={"e": ""})
case("a file in a subdirectory", ["d/a"], scratch=T)
case("an absolute path", ["{scratch}/f"], scratch={"f": "1\n", "keep": "2\n"})
case("the cwd is a subdirectory", ["a"], scratch=T, cwd="d")
case("one of two hard links", ["one"], scratch={"one": "x\n"}, scratch_hardlinks={"two": "one"})
case("a fifo", ["p"], scratch_fifos=["p"])
case("a socket", ["s"], scratch_sockets=["s"])
case("a file nobody may write", ["wp"], scratch={"wp": "x\n"}, scratch_modes={"wp": 0o444})
case("a file with no permissions at all", ["z"], scratch={"z": "x\n"}, scratch_modes={"z": 0o000})
case("in a directory that may not be written", ["ro/f"], scratch={"ro/f": "x\n"}, scratch_modes={"ro": 0o555})
case("in a directory that may not be searched", ["no/f"], scratch={"no/f": "x\n"}, scratch_modes={"no": 0o000})
case("names that need quoting, missing", ["q'x", "tab\tx", "sp x", "new\nline", "é", "a\"b", "back\\slash", "#h"])
case("names that need quoting, removed", ["-v", "q'x", "tab\tx", "sp x", "new\nline", "é", "a\"b", "c'd\"e"],
     scratch={"q'x": "", "tab\tx": "", "sp x": "", "new\nline": "", "é": "", "a\"b": "", "c'd\"e": ""})

C.note("--- links: removed, never followed")
case("a link to a file", ["l"], scratch=F, scratch_links={"l": "f"})
case("a link to a directory", ["l"], scratch=T, scratch_links={"l": "d"})
case("a dangling link", ["l"], scratch_links={"l": "nowhere"})
case("a link to a directory, with a slash", ["l/"], scratch=T, scratch_links={"l": "d"})
case("a link to a file, with a slash", ["l/"], scratch=F, scratch_links={"l": "f"})
case("a dangling link, with a slash", ["l/"], scratch_links={"l": "nowhere"})
case("a link that points at itself", ["l"], scratch_links={"l": "l"})
case("through a link to a directory", ["l/a"], scratch=T, scratch_links={"l": "d"})

C.note("--- directories without -r")
case("a directory", ["d"], scratch=T)
case("an empty directory", ["e"], scratch_dirs=["e"])
case("the working directory", ["."])
case("a directory, then a file", ["d", "f"], scratch={**T, **F})
case("-f does not make a directory removable", ["-f", "d"], scratch=T)

C.note("--- -f")
case("-f: no operand", ["-f"])
case("-f: a missing name", ["-f", "missing"])
case("-f: a file", ["-f", "f"], scratch=F)
case("-f: an empty name", ["-f", ""])
case("-f: a name under a file", ["-f", "f/x"], scratch=F)
case("-f: missing names among files", ["-f", "", "missing", "f", "d/missing"], scratch={**F, **T})
case("-f does not forgive a directory that may not be written", ["-f", "ro/f"], scratch={"ro/f": "x\n"}, scratch_modes={"ro": 0o555})
case("--force", ["--force", "missing"])
case("--for abbreviates", ["--for", "missing"])
case("-rf: no operand", ["-rf"])
case("-r: no operand", ["-r"])
case("-v: no operand", ["-v"])
case("-i: no operand", ["-i"])

C.note("--- -d")
case("-d: an empty directory", ["-d", "e"], scratch_dirs=["e"])
case("-d: a directory that is not empty", ["-d", "d"], scratch=T)
case("-d: a file", ["-d", "f"], scratch=F)
case("-d: a missing name", ["-d", "missing"])
case("-d: two, the first not empty", ["-d", "k1", "k2"], scratch={"k1/f": ""}, scratch_dirs=["k2"])
case("-dv", ["-dv", "e", "missing", "d"], scratch={**T}, scratch_dirs=["e"])
case("-d: the working directory", ["-d", "."])
case("-d: a directory with no permissions, empty", ["-d", "z"], scratch_dirs=["z"], scratch_modes={"z": 0o000})
case("-d: a directory with no permissions, not empty", ["-d", "ne"], scratch_dirs=["ne/x"], scratch_modes={"ne": 0o000})
case("-d: a link to an empty directory", ["-d", "l"], scratch_dirs=["e"], scratch_links={"l": "e"})
case("--dir", ["--dir", "e"], scratch_dirs=["e"])
case("-rd: -r wins", ["-rd", "d"], scratch=T)

C.note("--- -v")
case("-v: files", ["-v", "f", "e"], scratch={"f": "x\n", "e": ""})
case("-v: links", ["-v", "ld", "lf", "dang"], scratch={**T, **F}, scratch_links={"ld": "d", "lf": "f", "dang": "nowhere"})
case("-v: a failure says nothing on stdout", ["-v", "missing", "f"], scratch=F)
case("--verbose", ["--verbose", "f"], scratch=F)
case("--v is ambiguous", ["--v", "f"], scratch=F)

C.note("--- -r: the walk")
case("-r: a tree", ["-r", "d"], scratch={**T, "keep": "k\n"})
case("-R", ["-R", "d"], scratch=T)
case("--recursive", ["--recursive", "d"], scratch=T)
case("--rec abbreviates", ["--rec", "d"], scratch=T)
case("--r abbreviates", ["--r", "d"], scratch=T)
case("-rv: a tree", ["-rv", "d"], scratch=T)
case("-rv: a trailing slash", ["-rv", "d/"], scratch=T)
case("-rv: two trailing slashes", ["-rv", "d//"], scratch=T)
case("-rv: a leading ./ and a dot in the middle", ["-rv", "./d/sub/", "d/./a"], scratch=T)
case("-r: a file", ["-r", "f"], scratch=F)
case("-r: an empty directory", ["-rv", "e"], scratch_dirs=["e"])
case("-r: two trees and a file", ["-rv", "d", "e", "f"], scratch={**T, **F}, scratch_dirs=["e"])
case("-r: the same tree twice", ["-r", "d", "d"], scratch=T)
case("-r: a missing name", ["-r", "missing"])
case("-rf: a missing name", ["-rf", "missing"])
case("-rf: a name under a file", ["-rf", "f/x"], scratch=F)
case("-r: an empty name", ["-r", ""])
case("-rf: an empty name", ["-rf", ""])
case("-r: a subtree by an absolute path", ["-r", "{scratch}/d/sub"], scratch=T)
case("-r: twelve files in one directory", ["-rv", "big"], scratch={f"big/f{i}": f"{i}\n" for i in range(1, 13)})
case("-r: a wide and deep tree", ["-r", "w"],
     scratch={f"w/{a}/{b}/{c}": "x" for a in "abcd" for b in "efgh" for c in "ijkl"})
case("-r: names that need quoting", ["-rv", "q'u", "new\nline", "sp ace"],
     scratch={"q'u/a b": "", "new\nline/x": "", "sp ace/tab\tx": ""})
case("-r: every kind of file inside", ["-rv", "k"], scratch={"k/f": "x\n", "k/e": ""}, scratch_dirs=["k/d"],
     scratch_links={"k/l": "f", "k/dang": "nowhere"}, scratch_fifos=["k/p"], scratch_sockets=["k/s"],
     scratch_hardlinks={"k/h": "k/f"})
case("-r: hard links to a file outside the tree", ["-r", "k"], scratch={"out": "kept\n"}, scratch_dirs=["k"],
     scratch_hardlinks={"k/h": "out"})

C.note("--- -r never follows a link\nThe first of these is the case a planted break must turn red (the\nlane's contract): a link inside the tree that points OUT of it, at a\ndirectory beside it in the same scratch directory. The link goes; what\nit names stays, with everything in it.")
case("-r: a link out of the tree is removed, and what it names is not", ["-r", "t"],
     scratch={"t/in": "x\n", "outside/keep": "kept\n", "outside/sub/deeper": "kept too\n"},
     scratch_links={"t/link": "../outside"})
case("-rv: the same, said", ["-rv", "t"],
     scratch={"t/in": "x\n", "outside/keep": "kept\n"}, scratch_links={"t/link": "../outside"})
case("-r: links up, across and to nothing", ["-rv", "m"],
     scratch={"m/a/b/c/d/f": "x\n", "side/keep": "k\n"},
     scratch_links={"m/a/b/c/up": "../../..", "m/a/lb": "b", "m/dang": "nowhere", "m/out": "../side", "m/self": "self"})
case("-r: an operand that is a link to a directory", ["-r", "l"], scratch=T, scratch_links={"l": "d"})
case("-rv: an operand that is a link to a directory", ["-rv", "l"], scratch=T, scratch_links={"l": "d"})
case("-r: a link to a directory, with a slash, empties the directory", ["-r", "l/"], scratch=T, scratch_links={"l": "d"})
case("-rv: a link to a directory, with a slash", ["-rv", "l/"], scratch=T, scratch_links={"l": "d"})
case("-r: a link to a file, with a slash", ["-r", "l/"], scratch=F, scratch_links={"l": "f"})
case("-r: a dangling link, with a slash", ["-r", "l/"], scratch_links={"l": "nowhere"})
case("-r: a file with a slash", ["-r", "f/"], scratch=F)
case("-r: a link to a directory nobody may list", ["-r", "t"], scratch={"t/in": "x\n", "outside/keep": "k\n"},
     scratch_links={"t/link": "../outside"}, scratch_modes={"outside": 0o000})

C.note("--- -r: . and ..\nNo case names `..`: the harness refuses one for every utility that\nchanges the file system, and src/change_test.lu covers the rule.")
case("-r: the working directory", ["-r", "."], scratch=T)
case("-rf: the working directory", ["-rf", "."], scratch=T)
case("-r: ./", ["-r", "./"], scratch=T)
case("-r: a directory's own dot", ["-r", "d/."], scratch=T)
case("-r: a directory's own dot, with a slash", ["-r", "d/./"], scratch=T)
case("-r: the dot is skipped and the rest removed", ["-rv", ".", "d", "./", "f"], scratch={**T, **F})
case("-rv: a name that only begins with a dot", ["-rv", ".hidden", "..."], scratch={".hidden/x": "", ".../y": ""})

C.note("--- -r: what the host refuses")
case("-r: a directory that may not be written", ["-r", "ro"], scratch={"ro/f": "x\n", "ro/sub/g": "x\n"}, scratch_modes={"ro": 0o555})
case("-rf: the same; -f forgives none of it", ["-rf", "ro"], scratch={"ro/f": "x\n", "ro/sub/g": "x\n"}, scratch_modes={"ro": 0o555})
case("-rv: a directory that may not be written, said", ["-rv", "ro"], scratch={"ro/f": "x\n", "ro/sub/g": "x\n"}, scratch_modes={"ro": 0o555})
case("-r: a directory that may not be listed, not empty", ["-r", "no"], scratch={"no/sub/h": "x\n"}, scratch_modes={"no": 0o000})
case("-rfv: the same", ["-rfv", "no"], scratch={"no/sub/h": "x\n"}, scratch_modes={"no": 0o000})
case("-r: a directory that may not be listed, empty", ["-rv", "z"], scratch_dirs=["z"], scratch_modes={"z": 0o000})
case("-r: a directory that may be listed and not searched", ["-r", "rx"], scratch={"rx/f": "x\n"}, scratch_modes={"rx": 0o444})
case("-rv: one branch refused, the others removed, the top left", ["-rv", "u"],
     scratch={"u/a/1": "1\n", "u/b/2": "2\n", "u/c/3": "3\n"}, scratch_modes={"u/b": 0o555})
case("-r: the refused branch does not stop the next operand", ["-rv", "u", "v"],
     scratch={"u/b/2": "2\n", "v/x": "x\n"}, scratch_modes={"u/b": 0o555})
case("-r: an unlistable directory deep inside", ["-r", "o"], scratch={"o/a/f": "x\n", "o/no/in/g": "x\n"}, scratch_modes={"o/no": 0o000})

C.note("--- -i")
case("-i: yes", ["-i", "f"], scratch=F, stdin="y\n")
case("-i: no", ["-i", "f"], scratch=F, stdin="n\n")
case("-i: the end of input is no", ["-i", "f"], scratch=F, stdin="")
case("-i: no input at all", ["-i", "f"], scratch=F)
case("-i: Y", ["-i", "f"], scratch=F, stdin="Y\n")
case("-i: yes spelled out", ["-i", "f"], scratch=F, stdin="yes\n")
case("-i: a space before the y", ["-i", "f"], scratch=F, stdin=" y\n")
case("-i: y with no newline", ["-i", "f"], scratch=F, stdin="y")
case("-i: an empty line", ["-i", "f"], scratch=F, stdin="\n")
case("-i: one answer a file", ["-i", "f", "e"], scratch={"f": "x\n", "e": ""}, stdin="x\ny\n")
case("-i: answers run out", ["-i", "f", "e", "g"], scratch={"f": "x\n", "e": "", "g": "x\n"}, stdin="y\n")
case("-i: several answers on separate lines", ["-i", "a", "b", "c", "d", "e"], scratch={k: "x\n" for k in "abcde"}, stdin="yes\nYES\nyep\nYo\nnope\n")
case("-i: every kind", ["-i", "ld", "dang", "p", "s", "wp", "e", "f"],
     scratch={"d/x": "", "wp": "x\n", "e": "", "f": "x\n"}, scratch_links={"ld": "d", "dang": "nowhere"},
     scratch_fifos=["p"], scratch_sockets=["s"], scratch_modes={"wp": 0o444}, stdin="y\n" * 7)
case("-i: a write-protected empty file", ["-i", "we"], scratch={"we": ""}, scratch_modes={"we": 0o400}, stdin="n\n")
case("-i: a missing name is not asked about", ["-i", "missing"], stdin="y\n")
case("-i: a directory is not asked about", ["-i", "d"], scratch=T, stdin="y\n")
case("-iv: said after the answer", ["-iv", "f"], scratch=F, stdin="y\n")
case("-iv: nothing said after a no", ["-iv", "f"], scratch=F, stdin="n\n")
case("-i: names that need quoting", ["-i", "q'x", "sp x", "new\nline"], scratch={"q'x": "", "sp x": "", "new\nline": ""}, stdin="n\nn\nn\n")
case("-di: an empty directory", ["-di", "e"], scratch_dirs=["e"], stdin="y\n")
case("-di: no", ["-di", "e"], scratch_dirs=["e"], stdin="n\n")
case("-di: a directory that is not empty", ["-di", "d"], scratch=T, stdin="y\n")
case("-div", ["-div", "e"], scratch_dirs=["e"], stdin="y\n")
case("-ri: yes to everything", ["-ri", "d", "e"], scratch=T, scratch_dirs=["e"], stdin="y\n" * 12)
case("-ri: no to the descent", ["-ri", "d"], scratch=T, stdin="n\n")
case("-ri: no to a subdirectory leaves its parents", ["-ri", "d"], scratch={"d/sub/b": "b\n", "d/a": "a\n"}, stdin="y\nn\ny\ny\ny\n")
case("-ri: no to one file leaves its directory", ["-ri", "d"], scratch={"d/a": "a\n", "d/b": "b\n"}, stdin="y\nn\ny\ny\n")
case("-ri: no to the directory itself, emptied", ["-ri", "d"], scratch={"d/a": "a\n"}, stdin="y\ny\nn\n")
case("-ri: no to an emptied subdirectory", ["-ri", "d"], scratch={"d/sub/b": "b\n"}, stdin="y\ny\ny\nn\ny\n")
case("-ri: no to a file in a subdirectory", ["-ri", "d"], scratch={"d/sub/b": "b\n", "d/a": "a\n"}, stdin="y\ny\nn\ny\ny\ny\n")
case("-ri: no to a file, then no to its directory", ["-ri", "d"], scratch={"d/a": "a\n", "d/b": "b\n"}, stdin="y\nn\ny\nn\n")
case("-ri: no to an empty subdirectory", ["-ri", "d"], scratch_dirs=["d/e"], stdin="y\nn\ny\n")
case("-ri: no to a link", ["-ri", "d"], scratch={"d/a": "a\n"}, scratch_links={"d/l": "a"}, stdin="y\ny\nn\ny\n")
case("-rif then -i again: a missing name inside is asked nothing", ["-r", "-f", "-i", "d", "missing"], scratch={"d/a": "a\n"}, stdin="y\ny\ny\n")
case("-ri: an empty directory", ["-ri", "e"], scratch_dirs=["e"], stdin="n\n")
case("-ri: the end of input in the middle", ["-ri", "d"], scratch=T, stdin="y\ny\n")
case("-ri: links are asked about and not followed", ["-ri", "L"], scratch_dirs=["L/x"], scratch_links={"L/lx": "x", "L/dang": "nowhere"}, stdin="y\n" * 5)
case("-ri: a socket and a fifo", ["-ri", "s1"], scratch_sockets=["s1/sock"], scratch_fifos=["s1/pipe"], scratch_dirs=["s1"], stdin="y\n" * 4)
case("-ri: write-protected things", ["-ri", "wd"], scratch={"wd/f": "x\n"}, scratch_dirs=["wd/wpd"], scratch_modes={"wd/f": 0o444, "wd/wpd": 0o555}, stdin="y\n" * 5)
case("-ri: a write-protected directory that is not empty", ["-ri", "wp"], scratch={"wp/in/f": "x\n"}, scratch_modes={"wp": 0o555}, stdin="y\n" * 4)
case("-ri: a directory that may not be listed, not empty", ["-ri", "un"], scratch_dirs=["un/in"], scratch_modes={"un": 0o000}, stdin="y\ny\n")
case("-ri: a directory that may not be listed, empty", ["-ri", "ez"], scratch_dirs=["ez"], scratch_modes={"ez": 0o000}, stdin="y\n")
case("-riv", ["-riv", "d"], scratch={"d/a": "a\n"}, stdin="y\ny\ny\n")

C.note("--- -I")
case("-I: three files, no question", ["-I", "a", "b", "c"], scratch={k: "" for k in "abc"}, stdin="n\n")
case("-I: four files, yes", ["-I", "a", "b", "c", "d"], scratch={k: "" for k in "abcd"}, stdin="y\n")
case("-I: four files, no", ["-I", "a", "b", "c", "d"], scratch={k: "" for k in "abcd"}, stdin="n\n")
case("-I: four files, the end of input", ["-I", "a", "b", "c", "d"], scratch={k: "" for k in "abcd"})
case("-I: missing names count", ["-Iv", "a", "b", "c", "d", "missing"], scratch={k: "" for k in "abcd"}, stdin="y\n")
case("-Ir: one argument", ["-Ir", "d"], scratch=T, stdin="y\n")
case("-I -r: two arguments, no", ["-I", "-r", "d", "f"], scratch={**T, **F}, stdin="n\n")
case("-rI: three arguments", ["-rI", "d", "e", "f"], scratch={**T, **F}, scratch_dirs=["e"], stdin="y\n")
case("-I asks once and then not per file", ["-I", "a", "b", "c", "d"], scratch={k: "x\n" for k in "abcd"}, scratch_modes={"a": 0o444}, stdin="y\nn\n")

C.note("--- --interactive, and which of -f -i -I wins")
case("--interactive alone is always", ["--interactive", "f"], scratch=F, stdin="n\n")
case("--interactive=always", ["--interactive=always", "f"], scratch=F, stdin="n\n")
case("--interactive=yes", ["--interactive=yes", "f"], scratch=F, stdin="n\n")
case("--interactive=a abbreviates", ["--interactive=a", "f"], scratch=F, stdin="n\n")
case("--interactive=never", ["--interactive=never", "f"], scratch=F, stdin="n\n")
case("--interactive=no", ["--interactive=no", "f"], scratch=F, stdin="n\n")
case("--interactive=none", ["--interactive=none", "f"], scratch=F, stdin="n\n")
case("--interactive=n: three words, one meaning", ["--interactive=n", "f"], scratch=F, stdin="n\n")
case("--interactive=never still reports a missing name", ["--interactive=never", "missing"])
case("--interactive=once: one file", ["--interactive=once", "f"], scratch=F, stdin="n\n")
case("--interactive=once: four files", ["--interactive=once", "a", "b", "c", "d"], scratch={k: "" for k in "abcd"}, stdin="n\n")
case("--interactive=o abbreviates", ["--interactive=o", "a", "b", "c", "d"], scratch={k: "" for k in "abcd"}, stdin="n\n")
case("--interactive=bogus", ["--interactive=bogus", "f"], scratch=F)
case("--interactive= is ambiguous", ["--interactive=", "f"], scratch=F)
case("--inter abbreviates the option", ["--inter", "f"], scratch=F, stdin="n\n")
case("-f -i: the last wins, and asks", ["-f", "-i", "f"], scratch=F, stdin="n\n")
case("-i -f: the last wins, and does not", ["-i", "-f", "f"], scratch=F, stdin="n\n")
case("-I -i", ["-I", "-i", "f"], scratch=F, stdin="n\n")
case("-i -I", ["-i", "-I", "f"], scratch=F, stdin="n\n")
case("-If: four files, no question", ["-If", "a", "b", "c", "d"], scratch={k: "" for k in "abcd"}, stdin="n\n")
case("-fI: four files, one question", ["-fI", "a", "b", "c", "d"], scratch={k: "" for k in "abcd"}, stdin="n\n")
case("-i --interactive=never reports a missing name", ["-i", "--interactive=never", "missing"], stdin="n\n")
case("-f --interactive=never keeps -f's silence", ["-f", "--interactive=never", "missing"])
case("-i -f: a missing name is forgiven", ["-i", "-f", "missing"])
case("-f -i: a missing name is not", ["-f", "-i", "missing"])

C.note("--- the root rule's options, on names that are not the root")
case("--preserve-root", ["--preserve-root", "f"], scratch=F)
case("--pre abbreviates", ["--pre", "missing"])
case("-r --preserve-root", ["-r", "--preserve-root", "d"], scratch=T)
case("--preserve-root=bogus", ["-r", "--preserve-root=bogus", "d"], scratch=T)
case("--no-pres may not be abbreviated", ["--no-pres", "missing"])
case("--no-preserve-root=1 takes no argument", ["--no-preserve-root=1", "f"], scratch=F)
case("--one-file-system on one file system", ["-r", "--one-file-system", "d"], scratch=T)
case("--one abbreviates", ["-rv", "--one", "d"], scratch=T)
NOROOT = "this rm refuses --no-preserve-root by name, status 1: it does not remove '/' (see the header of src/rm.lu)"
case("--no-preserve-root", ["--no-preserve-root", "f"], scratch=F, skip=NOROOT)
case("-r --no-preserve-root", ["-r", "--no-preserve-root", "d"], scratch=T, skip=NOROOT)
case("--preserve-root=all", ["-r", "--preserve-root=all", "d"], scratch=T, skip="--preserve-root=all is not written yet: refused by name, status 1")

C.note("--- options")
case("-- ends the options", ["--", "-f"], scratch={"-f": ""})
case("./-f names the file", ["./-f"], scratch={"-f": ""})
case("a bad option", ["-x"])
case("a bad option, and a file of that name", ["-x"], scratch={"-x": ""})
case("a bad option, and a file whose name has a space", ["-a b"], scratch={"-a b": ""})
case("a bad option, and a file whose name has a quote", ["-q'x"], scratch={"-q'x": ""})
case("a bad long option, and a file with a dash", ["--bogus", "-y"], scratch={"-y": ""})
case("a bad option, and the first such file is the one named", ["-x", "-y", "-z"], scratch={"-y": "", "-z": ""})
case("an unknown long option", ["--bogus", "f"], scratch=F)
case("POSIXLY_CORRECT: the first operand ends the options", ["f", "-v"], scratch={"f": "", "-v": ""}, env={"POSIXLY_CORRECT": "1"})
case("--help", ["--help"], compare=["exit"])
case("--version", ["--version"], compare=["exit"])
case("--help wins over a later bad option", ["--help", "--bogus"], compare=["exit"])
case("stdout closed, nothing to write", ["f"], scratch=F, stdout_closed=True)
case("stdout closed under -v", ["-v", "f"], scratch=F, stdout_closed=True)

head = '''# rm — GNU coreutils 9.11, black-box, on linux x86-64 and macOS arm64.
# Written by notes/bu21/gen/rm_cases.py; this file is the record.
#
# rm removes, so every case runs in a scratch directory the harness made
# under its root and checked by prefix immediately before each side
# starts (tools/difftest, bu21), and the harness refuses the whole run
# when any case names `/`, a `~`, a `..` component or an absolute path
# outside `{scratch}`. NO CASE RUNS ANY rm ON THE ROOT: the refusal of
# `/` is a function, unit-tested in src/change_test.lu. A link in a
# fixture points inside the scratch directory or at nothing.
#
# What each side leaves is compared as `files` (names, kinds, bytes)
# and `tree` (modes, link counts): a removal that reached further than
# GNU's is a difference in what is LEFT.
#
# What this rm cannot match is named, never imitated:
#   --no-preserve-root   refused by name: this rm does not remove `/`
#   --preserve-root=all  not written yet
#   wolf-lang#633        "may I write it?" is the owner's write bit
'''
C.write(sys.argv[1], head)
