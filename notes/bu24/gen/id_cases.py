#!/usr/bin/env python3
"""bu24: write tests/ids/cases.toml — the identity tools' container cases.

Run from the repository root: python3 notes/bu24/gen/id_cases.py
Every case runs in tools/idtest's throwaway container; its accounts are
the image's own (tools/idtest ACCOUNTS)."""
import json
import shlex

cases = []
seen = set()


def case(util, args, as_="root", **kw):
    named = "name" in kw
    name = kw.pop("name", None) or f"{util}: {shlex.join(args) or '(none)'} as {as_}"
    if kw.get("tty"):
        name += " on a terminal"
    if kw.get("utmp"):
        name += " with " + ", ".join(f"{t}/{l}/{u}" for t, l, u in kw["utmp"])
    # A case given its own name says what its setup is for in it.
    if kw.get("setup") and not named:
        name += f" after `{kw['setup']}`"
    assert name not in seen, name
    seen.add(name)
    c = {"name": name, "util": util, "args": args}
    if as_ != "root":
        c["as"] = as_
    c.update(kw)
    cases.append(c)


ACTORS = ["root", "rootgroups", "alice", "bob", "carol", "dotty", "nobody",
          "gid4242", "split", "splitg", "nogroups", "twin"]
FORMS = [[], ["-u"], ["-un"], ["-ur"], ["-urn"], ["-g"], ["-gn"], ["-gr"],
         ["-grn"], ["-G"], ["-Gn"], ["-Gr"], ["-Grn"], ["-Gz"], ["-Gnz"],
         ["-uz"], ["-unz"], ["-gz"], ["-a"], ["--user", "--name"],
         ["-G", "--zero", "--name"]]
for a in ACTORS:
    for f in FORMS:
        case("id", f, a)
    case("whoami", [], a)
    case("groups", [], a)
    case("logname", [], a)

USERS = ["alice", "bob", "carol", "dot.ty", "twin", "root", "1001", "+1001",
         "1002", "0", "007", "4242", "nosuch", "", "-", "4294967295",
         "4294967294", "99999999999", "ghost", "pack"]
for who in ("root", "alice"):
    for u in USERS:
        case("id", [u], who)
        case("groups", [u], who)
    for f in (["-u"], ["-un"], ["-g"], ["-gn"], ["-G"], ["-Gn"], ["-Gnz"], ["-ur"], ["-Grn"]):
        for u in ("alice", "bob", "carol", "twin", "1001"):
            case("id", f + [u], who)
    case("id", ["alice", "bob"], who)
    case("id", ["alice", "nosuch", "bob"], who)
    case("id", ["--", "alice"], who)
    case("id", ["-u", "--", "-alice"], who)
    case("groups", ["alice", "bob", "carol"], who)
    case("groups", ["alice", "nosuch", "bob"], who)
    case("groups", ["--", "alice"], who)

for f in (["-n"], ["-r"], ["-z"], ["-nz"], ["-rz"], ["-ug"], ["-uG"], ["-Gg"],
          ["-ugG"], ["-ugn"], ["-ugz"], ["-Z"], ["-Zu"], ["-uZ"], ["-Zn"],
          ["--context"], ["-Z", "alice"], ["--us"], ["--u"], ["--na"],
          ["--nam", "-u"], ["--zero", "-G"], ["-G", "-n"], ["-nG"], ["-a", "-u"],
          ["-uaz"], ["--real", "--group"], ["-n", "nosuch"], ["-ug", "nosuch"],
          ["-z", "alice"], ["--groups", "--zero", "alice", "bob"], ["-uz", "alice", "bob"],
          ["-gnz", "alice", "bob"], ["-Gz", "alice", "nosuch", "bob", "carol"], ["-G", "alice", "bob"]):
    case("id", f)
for u in ("whoami", "logname"):
    case(u, ["x"])
    case(u, ["-x"])
    case(u, ["--"])
    case(u, ["--", "x"])
    case(u, ["--help"], compare=["exit", "stderr"])
    case(u, ["--version"], compare=["exit", "stderr"])
    case(u, ["--he"], compare=["exit", "stderr"])
for u in ("id", "groups"):
    case(u, ["--help"], compare=["exit", "stderr"])
    case(u, ["--version"], compare=["exit", "stderr"])
    case(u, ["-x"])
case("groups", ["--"])

# logname: the login record of standard input's terminal.
for who in ("root", "alice", "nobody"):
    case("logname", [], who, tty=True)
    case("logname", [], who, tty=True, utmp=[[7, "{tty}", "alice"]])
    case("logname", [], who, tty=True, utmp=[[6, "{tty}", "LOGIN"]])
    case("logname", [], who, tty=True, utmp=[[8, "{tty}", "alice"]])
    case("logname", [], who, tty=True, utmp=[[7, "pts/77", "bob"]])
    case("logname", [], who, tty=True, utmp=[[7, "pts/77", "bob"], [7, "{tty}", "carol"], [7, "{tty}", "bob"]])
    case("logname", [], who, tty=True, utmp=[[7, "{tty}", "zed"]])
    case("logname", [], who, utmp=[[7, "{tty}", "alice"]])
case("logname", [], "root", tty=True, utmp=[[1, "{tty}", "alice"], [7, "{tty}", "dot.ty"]])
case("logname", [], "root", tty=True, utmp=[[7, "{tty}", ""]])
case("logname", ["x"], "root", tty=True, utmp=[[7, "{tty}", "alice"]])

# chown and chgrp: the spec.
SPECS = ["alice", "alice:", "alice:pack", ":pack", "alice.pack", "1002", "+1002",
         "alice:+2000", ":", "", "nosuch", "alice:nosuch", ":nosuch", "4242:4243",
         "4242", "4294967295", "4294967294", "4294967296", "alice.", ".pack",
         "alice:pack:x", "bob.", "nosuch.pack", "alice.nosuch", " alice", "1002:",
         "+0", "0x10", "007", "root:root", "alice::pack", "dot.ty", "dot.ty:pack",
         "dot.ty.pack", "dot.ty.", "bob:", "carol:", "twin", "twin:", "1001:pack",
         "nosuch:pack", "nosuch:", ":1500", ":zeta", "alice:4243", "4242:", "+",
         ":+", "-", "alice:-1", "-1:pack", "root.root", "a:b:c"]
for s in SPECS:
    case("chown", ["-v", s, "f"])
for s in ["pack", "2000", "+2000", "nosuch", "", "4243", "4294967295", " pack",
          "root", "zeta", "1500", "crew2", "pack2", "alice", ":pack", "pack:",
          "007", "+"]:
    case("chgrp", ["-v", s, "f"])

# The options, as root.
for util, spec in (("chown", "alice"), ("chown", "alice:pack"), ("chown", ":pack"),
                   ("chgrp", "pack")):
    for args in (["-v"], ["-c"], [], ["-f"], ["-vf"], ["-cv"]):
        case(util, args + [spec, "f", "g"])
        case(util, args + [spec, "nosuch", "f"])
        case(util, args + [spec, "dang"], gnu_sub=True)
        case(util, args + ["-h", spec, "dang"])
    for args in (["-v", spec, "l"], ["-vh", spec, "l"], ["-v", "--dereference", spec, "l"],
                 ["-v", "-h", "--dereference", spec, "l"], ["-v", "--dereference", "-h", spec, "l"],
                 ["-vR", spec, "d"], ["-vR", spec, "dl"], ["-vRH", spec, "dl"],
                 ["-vRL", spec, "d"], ["-vRP", spec, "dl"], ["-vRh", spec, "dl"],
                 ["-R", "--dereference", spec, "d"], ["-vRH", "--dereference", spec, "dl"],
                 ["-vRL", "--dereference", spec, "d"], ["-vRLh", spec, "d"], ["-vRHh", spec, "dl"],
                 ["-cR", spec, "d"], ["-vR", spec, "d", "f", "dl"], ["-vRLP", spec, "d"],
                 ["-vRPL", spec, "dl"], ["-vRHP", spec, "dl"], ["-vH", spec, "dl"],
                 ["-vL", spec, "dl"], ["-vR", spec, "d/e"], ["-vR", spec, "."],
                 ["-vR", spec, "d/"], ["-vR", spec, "dl/"], ["-v", spec, "dl/"],
                 ["-v", spec, "d/../f"], ["-v", spec, "./f"], ["-v", spec, "f", "f"],
                 ["-vR", "--preserve-root", spec, "/"], ["-R", "--preserve-root", spec, "//"],
                 ["-R", "--preserve-root", spec, "/work/.."], ["--preserve-root", spec, "/work/f"],
                 ["-vR", "--preserve-root", "--no-preserve-root", spec, "d"],
                 ):
        follows = ("-h" not in args and not any(a.startswith("-") and "h" in a[1:] and not a.startswith("--") for a in args)
                   and ("dang" in args or any(a.startswith("-") and not a.startswith("--") and "L" in a for a in args)))
        case(util, args, **({"gnu_sub": True} if follows else {}))
    case(util, ["-vRL", spec, "d"], setup="ln -s . d/e/self", gnu_sub=True)
    case(util, ["-vR", spec, "d"], setup="ln -s nowhere d/e/gone")
    case(util, ["-vRL", spec, "d"], setup="rm d/up; ln -s nowhere d/e/gone", gnu_sub=True)

# Missing and malformed operands, both programs.
for util in ("chown", "chgrp"):
    for args in ([], ["alice"], ["--reference=g"], ["-R"], ["-x"], ["-vx", "alice", "f"],
                 ["--from"], ["--reference"], ["--frob", "x", "f"], ["--", "pack", "f"],
                 ["pack", "--", "f"], ["-R", "--", "pack", "d"]):
        case(util, args)
    case(util, ["--help"], compare=["exit", "stderr", "tree"])
    case(util, ["--version"], compare=["exit", "stderr", "tree"])
    case(util, ["--he"], compare=["exit", "stderr", "tree"])

# --from and --reference.
for frm in ("root", "alice", ":alice", "alice:alice", "nosuch", "1001", "", ":",
            "alice:", "bob:", ":pack", "alice:pack", "4242", ":nosuch", "alice.alice",
            "root:root", "+0"):
    case("chown", ["-v", f"--from={frm}", "bob", "f", "g"])
    case("chgrp", ["-v", f"--from={frm}", "pack", "f", "g"])
case("chown", ["-v", "--from=bob:pack", "alice", "l"])
case("chown", ["-vh", "--from=bob:pack", "alice", "l"])
case("chown", ["-vR", "--from=root", "alice", "d"])
case("chown", ["-v", "--from=root", "alice", "dang"], gnu_sub=True)
for ref in ("g", "nosuch", "l", "dang", "d/e", "f"):
    case("chown", ["-v", f"--reference={ref}", "f", "d"])
    case("chgrp", ["-v", f"--reference={ref}", "f", "d"])
case("chown", ["-v", "--reference=g", "alice", "f"])
case("chown", ["-v", "--reference", "g", "f"])
case("chgrp", ["-v", "--reference=g", "pack", "f"])
case("chown", ["-vR", "--reference=d/e", "d"])
case("chown", ["-vh", "--reference=g", "l"])

# As users: what the host refuses, and what it lets a user do.
for who in ("alice", "bob", "carol", "nobody", "split"):
    for util, args in (("chown", ["-v", "alice", "g"]), ("chown", ["-v", "bob", "g"]),
                       ("chown", ["-v", ":pack", "g"]), ("chown", ["-v", ":crew", "g"]),
                       ("chown", ["-v", ":root", "g"]), ("chown", ["-v", ":zeta", "g"]),
                       ("chgrp", ["-v", "pack", "f"]), ("chgrp", ["-vf", "pack", "f"]),
                       ("chown", ["-v", "root", "f"]), ("chown", ["-vc", "alice:alice", "g"]),
                       ("chown", ["-c", "alice:alice", "g"]), ("chown", ["-c", "bob", "g"]),
                       ("chown", ["-v", "alice", "f"]), ("chgrp", ["-v", "pack", "g"]),
                       ("chgrp", ["-v", "crew", "g"]), ("chown", ["-v", ":pack", "d/e"]),
                       ("chown", ["-vR", ":crew", "d"]), ("chgrp", ["-v", "crew", "l"]),
                       ("chgrp", ["-vh", "crew", "l"]), ("chown", ["-v", "", "f"]),
                       ("chown", ["-v", ":", "g"]), ("chgrp", ["-vR", "crew", "d/e"]),
                       ("chown", ["-v", "--from=alice", ":crew", "f", "g"]),
                       ("chgrp", ["-v", "--reference=d/e", "g"])):
        case(util, args, who)
    case("chgrp", ["-vR", "crew", "d"], who, setup="chown -R alice d && chmod 0300 d/e")
    case("chgrp", ["-vR", "crew", "d"], who, setup="chown -R alice d && chmod 0600 d/e")
    case("chown", ["-v", "alice", "d/e/y"], who, setup="chmod 0700 d")

# CI's macOS runner (--engine none): as the runner's own user, on a tree
# the case makes, only to ids it already has. Names are compared nowhere
# here: macOS keeps the runner in its directory service, so GNU names it
# and this repository prints its number; the exit, the errors and every
# owner and mode after the run are compared.
SELF = ["exit", "stderr", "tree"]
for util, args in (("chgrp", ["-v", "{g2}", "f"]), ("chgrp", ["-v", "{gid}", "f"]),
                   ("chgrp", ["-vh", "{g2}", "l"]), ("chgrp", ["-v", "{g2}", "l"]),
                   ("chgrp", ["-vR", "{g2}", "d"]), ("chgrp", ["-vRL", "{g2}", "d"]),
                   ("chgrp", ["-vRH", "{g2}", "dl"]), ("chgrp", ["-c", "{g2}", "f"]),
                   ("chgrp", ["-v", "0", "f"]), ("chgrp", ["-vf", "0", "f"]),
                   ("chgrp", ["-v", "{g2}", "dang"]), ("chgrp", ["-vh", "{g2}", "dang"]),
                   ("chgrp", ["-v", "--from=:{gid}", "{g2}", "f", "g"]),
                   ("chgrp", ["-v", "{g2}", "nosuch", "f"]),
                   ("chown", ["-v", "{uid}", "f"]), ("chown", ["-v", ":{g2}", "f"]),
                   ("chown", ["-v", "{uid}:{g2}", "f"]), ("chown", ["-vh", ":{g2}", "l"]),
                   ("chown", ["-vR", ":{g2}", "d"]), ("chown", ["-vR", "{uid}", "d"]),
                   ("chown", ["-v", "0", "f"]), ("chown", ["-v", ":0", "f"]),
                   ("chown", ["-v", "0:{gid}", "f"]), ("chown", ["-v", "{uid}:", "f"]),
                   ("chown", ["-v", "--from={uid}", ":{g2}", "f"]),
                   ("chown", ["-v", "--from=0", ":{g2}", "f"]),
                   ("chown", ["-v", "", "f"]), ("chown", ["-v", ":", "f"])):
    case(util, args, "root", name=f"{util}: {shlex.join(args)} as this runner", self=True, compare=SELF)

# hostid (boreutils#70): the identifier from sources the case itself writes
# in the container, so no row depends on the runner. boreutils reads the
# first four bytes of /etc/hostid, else this host's IPv4 line of /etc/hosts
# when the host database reads files first; GNU asks the resolver, which in
# a container with no network answers from the files alone. Each answer
# below was measured against GNU 9.11's binary by hand first, in a fresh
# --network none ubuntu:24.04 container: 12345678 for the bytes 78 56 34
# 12, 140a281e for 10.20.30.40, and 00000000 when nothing answers.
HOSTS = "printf '10.20.30.40 %s\\n' \"$(uname -n)\" > /etc/hosts"
REFUSED = {"exit": 1, "stdout": "",
           "stderr": "hostid: host address unavailable: wolf has no host-address resolver\n"}
case("hostid", [], name="hostid: /etc/hostid, read before /etc/hosts",
     setup="printf '\\170\\126\\064\\022' > /etc/hostid; " + HOSTS)
case("hostid", [], name="hostid: this host's IPv4 line in /etc/hosts",
     setup="rm -f /etc/hostid; " + HOSTS)
case("hostid", [], name="hostid: /etc/hosts with a comment, another host, a tab, an alias "
     "and this host's name in capitals",
     setup="rm -f /etc/hostid; N=$(uname -n); printf '# %s\\n10.9.8.7 other\\n\\n"
     "10.20.30.40\\talias %s # x\\n10.1.1.1 %s\\n' \"$N\" \"$(printf %s \"$N\" | tr a-z A-Z)\" "
     "\"$N\" > /etc/hosts")
case("hostid", [], name="hostid: a /etc/hostid shorter than four bytes is passed over",
     setup="printf '\\170\\126' > /etc/hostid; " + HOSTS)
# Refused BY DESIGN where GNU answers: with no source, GNU prints an
# invented zero; with dns read before files, a resolver this repository
# cannot ask could answer first (with no network here, GNU's falls back).
case("hostid", [], name="hostid: no source answers, refused where GNU prints zero",
     setup="rm -f /etc/hostid; printf '127.0.0.1 localhost\\n' > /etc/hosts",
     ours=REFUSED, expect={"exit": 0, "stdout": "00000000\n"})
case("hostid", [], name="hostid: the host database reads dns first, refused",
     setup="rm -f /etc/hostid; " + HOSTS + "; "
     "sed -i 's/^hosts:.*/hosts: dns files/' /etc/nsswitch.conf",
     ours=REFUSED, expect={"exit": 0, "stdout": "140a281e\n"})
# boreutils#72: the lines of /etc/hosts GNU reads otherwise than as a plain
# dotted quad, each measured against GNU 9.11 first: a ::1 line naming this
# host reads as 127.0.0.1 (007f0100), a line with an octet above 255 is
# passed over, and 010.1.1.1 is no address at all (with nothing else to
# answer here, GNU prints its zero and this repository refuses).
case("hostid", [], name="hostid: a ::1 line naming this host, then an IPv4 line",
     setup="rm -f /etc/hostid; N=$(uname -n); printf '::1 %s\\n10.5.6.7 %s\\n' \"$N\" \"$N\" > /etc/hosts")
case("hostid", [], name="hostid: a ::1 line naming this host alone",
     setup="rm -f /etc/hostid; printf '::1 %s\\n' \"$(uname -n)\" > /etc/hosts")
case("hostid", [], name="hostid: a line with an octet above 255 is passed over",
     setup="rm -f /etc/hostid; N=$(uname -n); printf '300.1.1.1 %s\\n10.5.6.7 %s\\n' \"$N\" \"$N\" > /etc/hosts")
case("hostid", [], name="hostid: a leading zero is no address, refused where GNU prints zero",
     setup="rm -f /etc/hostid; printf '010.1.1.1 %s\\n' \"$(uname -n)\" > /etc/hosts",
     ours=REFUSED, expect={"exit": 0, "stdout": "00000000\n"})

with open("tests/ids/cases.toml", "w") as fh:
    fh.write("# tests/ids/cases.toml — written by notes/bu24/gen/id_cases.py; run by\n"
             "# tools/idtest, one throwaway container a case. Do not edit by hand:\n"
             "# change the generator and run it again.\n")
    for c in cases:
        fh.write("\n[[case]]\n")
        for k, v in c.items():
            if isinstance(v, dict):
                v = "{ " + ", ".join(f"{kk} = {json.dumps(vv)}" for kk, vv in v.items()) + " }"
                fh.write(f"{k} = {v}\n")
            else:
                fh.write(f"{k} = {json.dumps(v)}\n")
print(len(cases), "cases")
