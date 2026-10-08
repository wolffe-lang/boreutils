#!/usr/bin/env python3
# ls-columns-sweep.py (bu18): random directories, GNU ls 9.11 against
# boreutils ls, -C, -x and -m at every width 1-29 and 40, 57, 80, 0, with
# -T 0, -T 3, the default 8 and -q, names drawn from letters, digits,
# `.`, `_`, `-`, space, `~`, NEWLINE, TAB, \x01 and `é`. Run on kasumi as
# `python3 ls-columns-sweep.py SEED TRIALS` against the staged oracle;
# seeds 1 and 7 (40 trials each, 15,840 runs each), 3 (15 trials, 5,940
# runs) and, at the PR's head, 11 (40 trials): 0 differences once the
# first run's one finding was fixed (-w 0 is one line, never a grid).
import os, random, shutil, subprocess, sys
G = os.path.expanduser("~/lanes/bu18/boreutils/.gnu-bin/bin/ls")
B = os.path.expanduser("~/lanes/bu18/boreutils/target/release/ls")
ROOT = os.path.expanduser("~/lanes/bu18/sweep")
env = {"PATH": "/usr/bin:/bin", "LC_ALL": "C", "_POSIX2_VERSION": "200112"}
rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
alphabet = list("abcdefghijklmnopqrstuvwxyzABC0123456789._-") + ["\n", "\t", "\x01", "é", " ", "~"]
fails = runs = 0
for trial in range(int(sys.argv[2]) if len(sys.argv) > 2 else 40):
    shutil.rmtree(ROOT, ignore_errors=True)
    os.makedirs(ROOT)
    n = rng.choice([1, 2, 3, 4, 5, 7, 9, 13, 20, 31, 50])
    names = set()
    while len(names) < n:
        L = rng.choice([1, 1, 2, 3, 4, 5, 6, 8, 11, 15, 22])
        nm = "".join(rng.choice(alphabet) for _ in range(L))
        if nm in (".", "..") or "/" in nm or nm.startswith("."):
            continue
        names.add(nm)
    for nm in names:
        open(os.path.join(ROOT, nm), "w").close()
    for fmt in ("-C", "-x", "-m"):
        for w in list(range(1, 30)) + [40, 57, 80, 0]:
            for extra in ([], ["-T", "0"], ["-T", "3"], ["-q"]):
                args = [fmt, "-w", str(w)] + extra + [ROOT]
                g = subprocess.run([G] + args, env=env, capture_output=True)
                b = subprocess.run([B] + args, env=env, capture_output=True)
                runs += 1
                if g.stdout != b.stdout or g.returncode != b.returncode:
                    fails += 1
                    if fails <= 8:
                        print("DIFF", repr(sorted(names)), args)
                        print("  gnu ", repr(g.stdout))
                        print("  bore", repr(b.stdout))
print(f"runs={runs} fails={fails}")
