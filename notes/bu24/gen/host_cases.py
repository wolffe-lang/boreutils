#!/usr/bin/env python3
"""bu24: write tests/cases/{id,whoami,groups,logname,chown,chgrp}.toml —
the cases tools/difftest runs ON A HOST, as whoever runs it: the readers,
and chown/chgrp cases that name no file (tools/difftest refuses any
other). Run from the repository root."""
import json
import shlex

out = {u: [] for u in ("id", "whoami", "groups", "logname", "chown", "chgrp")}


def case(util, args, **kw):
    c = {"name": f"{shlex.join(args) or '(none)'}", "args": args}
    if kw.get("stdout_closed"):
        c["name"] += " >&-"
    if kw.get("stdout_file"):
        c["name"] += " > " + kw["stdout_file"]
    if "stdin" in kw:
        c["name"] += " < a pipe"
    c.update(kw)
    assert c["name"] not in [x["name"] for x in out[util]], (util, c["name"])
    out[util].append(c)


NAMES = "the host's names: macOS keeps its users in the directory service"
for f in ([], ["-a"]):
    case("id", f, accounts=True)
for f in (["-u"], ["-ur"], ["-g"], ["-gr"], ["-G"], ["-Gr"], ["-uz"], ["-gz"], ["-Gz"],
          ["--user"], ["--group", "--real"], ["--groups", "--zero"]):
    case("id", f)
for f in (["-un"], ["-urn"], ["-gn"], ["-grn"], ["-Gn"], ["-Grn"], ["-Gnz"], ["-unz"]):
    case("id", f, accounts=True)
for f in (["-n"], ["-r"], ["-z"], ["-nz"], ["-rz"], ["-ug"], ["-uG"], ["-Gg"], ["-ugG"],
          ["-ugn"], ["-ugz"], ["-Z"], ["-Zu"], ["-uZ"], ["--context"], ["-x"], ["--us"],
          ["--na"], ["-n", "nosuch-bu24"], ["-z", "root"], ["--frob"]):
    case("id", f)
for u in ("root", "0", "+0", "root root", "nosuch-bu24", "", "-", "4294967295",
          "99999999999"):
    args = u.split(" ") if " " in u else [u]
    known = u in ("root", "0", "+0", "root root")
    case("id", args, **({"accounts": True} if known else {}))
    if not u.startswith("+") and not u.isdigit() and " " not in u:
        case("groups", args, **({"accounts": True} if known else {}))
for f in (["-u"], ["-g"], ["-G"], ["-Gn"], ["-un"]):
    case("id", f + ["root"], accounts=True)
case("id", ["root", "nosuch-bu24"], accounts=True)
case("id", ["nosuch-bu24", "root"], accounts=True)
case("id", ["--help"], compare=["exit"])
case("id", ["--version"], compare=["exit"])
case("id", [], stdout_closed=True, accounts=True)
case("id", ["-u"], stdout_closed=True)
case("id", ["-u"], stdout_file="/dev/full")
case("groups", [], accounts=True)
case("groups", ["0"])
case("groups", ["--", "root"], accounts=True)
case("groups", ["root", "nosuch-bu24"], accounts=True)
case("groups", ["-x"])
case("groups", ["--help"], compare=["exit"])
case("groups", ["--version"], compare=["exit"])
case("groups", [], stdout_closed=True, accounts=True)
for u in ("whoami", "logname"):
    host = {"accounts": True} if u == "whoami" else {
        "skip_on": {"Darwin": "macOS answers getlogin from the kernel, which wolf cannot ask (bu24 note)"}}
    case(u, [], **host)
    case(u, ["x"])
    case(u, ["x", "y"])
    case(u, ["-x"])
    case(u, ["--"], **host)
    case(u, ["--", "x"])
    case(u, ["--help"], compare=["exit"])
    case(u, ["--version"], compare=["exit"])
    case(u, ["--he"], compare=["exit"])
    case(u, [], stdout_closed=True, **host)
case("logname", [], stdin="not a terminal\n",
     skip_on={"Darwin": "macOS answers getlogin from the kernel, which wolf cannot ask (bu24 note)"})
for u in ("chown", "chgrp"):
    for a in ([], ["x"], ["-R"], ["-R", "x"], ["-v", "x"], ["-x"], ["--frob"], ["-x", "y"],
              ["--from"], ["--from=nosuch-bu24", "x"], ["-R", "--dereference", "x"],
              ["--", "x"], ["-h"], ["--preserve-root", "x"]):
        case(u, a)
    case(u, ["--help"], compare=["exit"])
    case(u, ["--version"], compare=["exit"])
    case(u, ["--help"], stdout_closed=True)

for u, cs in out.items():
    with open(f"tests/cases/{u}.toml", "w") as fh:
        fh.write(f"# tests/cases/{u}.toml — written by notes/bu24/gen/host_cases.py.\n"
                 "# Run on a HOST by tools/difftest, as whoever runs it: nothing here\n"
                 "# changes an owner (tools/difftest refuses a chown/chgrp case naming\n"
                 "# a file). As root and as other users: tests/ids/, tools/idtest.\n")
        for c in cs:
            fh.write("\n[[case]]\n")
            for k, v in c.items():
                if isinstance(v, dict):
                    v = "{ " + ", ".join(f"{kk} = {json.dumps(vv)}" for kk, vv in v.items()) + " }"
                    fh.write(f"{k} = {v}\n")
                else:
                    fh.write(f"{k} = {json.dumps(v)}\n")
    print(u, len(cs))
