#!/usr/bin/env python3
"""Container-only disk/process integration, semantics and shape witnesses.

Run with python3 -I tests/disk-process/check.py inside the lane's Ubuntu
container, BORE_DISK_CONTAINER=1. No process outside this script's own
children is signalled. Every mutating operand is in one fresh scratch tree.
"""
import os
from pathlib import Path
import pty
import re
import select
import signal
import subprocess as sp
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[2]
assert os.environ.get("BORE_DISK_CONTAINER") == "1", "requires throwaway container"
GNU = ROOT / ".gnu-bin/bin"
passed = 0

def run(argv, **kw):
    return sp.run([str(x) for x in argv], capture_output=True, timeout=15, **kw)

def check(ok, name):
    global passed
    assert ok, name
    passed += 1
    print("ok integration:", name, flush=True)

def tty_run(name, mask, top):
    with tempfile.TemporaryDirectory(dir=top) as cwd:
        master, slave = pty.openpty()
        try:
            closed = mask >= 8
            child = sp.Popen([str(name), "/bin/sh", "-c", "printf out; printf err >&2"], cwd=cwd,
                             stdin=slave if mask & 1 else sp.DEVNULL,
                             stdout=slave if mask & 2 else sp.PIPE,
                             stderr=slave if mask & 4 or closed else sp.PIPE,
                             preexec_fn=(lambda: os.close(1)) if closed else None,
                             start_new_session=True)
            os.close(slave); slave = -1
            out, err = child.communicate(timeout=10)
            terminal = b""
            while select.select([master], [], [], 0)[0]:
                try: part = os.read(master, 65536)
                except OSError: break
                if not part: break
                terminal += part
            files = {p.name: (p.read_bytes(), p.stat().st_mode & 0o777) for p in Path(cwd).iterdir()}
            return child.returncode, out, err, terminal.replace(b"\r\n", b"\n"), files
        finally:
            os.close(master)
            if slave >= 0: os.close(slave)

with tempfile.TemporaryDirectory(prefix="bu34.") as raw:
    top = Path(raw)
    shim = top / "read-eio.so"
    sp.run(["cc", "-shared", "-fPIC", str(ROOT / "tests/disk-process/read-eio.c"), "-ldl", "-o", str(shim)], check=True)
    for tier in ("release", "dev"):
        bin = ROOT / "target" / tier
        for name in (GNU / "nohup", bin / "nohup"):
            result = run([name, "/bin/sh", "-c", "kill -HUP $$; printf alive"], start_new_session=True)
            check(result.returncode == 0 and result.stdout == b"alive", f"{tier} {name}: ignored HUP survives exec")
        for name in (GNU / "nohup", bin / "nohup"):
            with tempfile.TemporaryDirectory(dir=top) as cwd:
                master, slave = pty.openpty()
                try:
                    child = sp.Popen([str(name), "/bin/sh", "-c", "printf saved"], cwd=cwd,
                                     stdin=sp.DEVNULL, stdout=slave, stderr=sp.PIPE,
                                     start_new_session=True)
                    _, err = child.communicate(timeout=10)
                    output = Path(cwd) / "nohup.out"
                    check(child.returncode == 0 and output.read_bytes() == b"saved" and output.stat().st_mode & 0o777 == 0o600,
                          f"{tier} {name}: terminal stdout creates private nohup.out")
                finally:
                    os.close(master); os.close(slave)
        for name in (GNU / "nohup", bin / "nohup"):
            with tempfile.TemporaryDirectory(dir=top) as cwd:
                home = Path(cwd) / "home"; home.mkdir()
                (Path(cwd) / "nohup.out").mkdir()
                master, slave = pty.openpty()
                try:
                    child = sp.Popen([str(name), "/bin/sh", "-c", "printf home"], cwd=cwd,
                                     env=dict(os.environ, HOME=str(home)), stdin=sp.DEVNULL,
                                     stdout=slave, stderr=sp.PIPE, start_new_session=True)
                    child.communicate(timeout=10)
                    check(child.returncode == 0 and (home / "nohup.out").read_bytes() == b"home",
                          f"{tier} {name}: HOME fallback")
                finally:
                    os.close(master); os.close(slave)
        for mask in range(10):
            expected = tty_run(GNU / "nohup", mask, top)
            got = tty_run(bin / "nohup", mask, top)
            check(expected == got, f"{tier}: nohup tty descriptor mask {mask}: {expected!r} vs {got!r}")
        f = top / "shred-me"
        f.write_bytes(b"secret" * 13)
        result = run([bin / "shred", "-xvz", "-n", "25", f])
        lines = re.findall(rb"pass (\d+)/(\d+) \(([^)]+)\)", result.stderr)
        patterns = {x[2] for x in lines[:-1] if x[2] != b"random"}
        check(result.returncode == 0 and len(lines) == 26 and len(patterns) == 22 and lines[-1] == (b"26", b"26", b"000000") and f.read_bytes() == b"\0" * 78,
              tier + ": 25 mixed passes cover 22 patterns and final zero pass")
        source = top / "entropy"
        source.write_bytes(bytes(range(256)) * 512)
        for n in (1, 2, 3):
            outputs = []
            for name in (GNU / "shred", bin / "shred"):
                f.write_bytes(b"secret" * 13)
                result = run([name, "-x", "-n", str(n), "--random-source", source, f])
                assert result.returncode == 0, result.stderr
                outputs.append(f.read_bytes())
            check(outputs[0] == outputs[1], tier + f": deterministic random source, {n} passes")
        db = run([bin / "dircolors", "-p"])
        file = top / "colors"; file.write_bytes(db.stdout)
        for term in ("dumb", "xterm", "screen", "linux", "con5x8"):
            env = dict(os.environ, TERM=term, COLORTERM="", LC_ALL="C")
            expected = run([GNU / "dircolors", "-b"], env=env)
            got = run([GNU / "dircolors", "-b", file], env=env)
            check(db.returncode == 0 and got.returncode == 0 and expected.stdout == got.stdout,
                  tier + ": emitted database has GNU's color-rule semantics for " + term)
        fixture = top / "read-eio-input"
        fixture.write_bytes(b"abcdefghijkl")
        for conv in ("noerror", "noerror,sync"):
            outputs = []
            for name in (GNU / "dd", bin / "dd"):
                result = run([name, "if=" + str(fixture), "bs=4", "count=3", "conv=" + conv, "status=noxfer"],
                             env=dict(os.environ, LD_PRELOAD=str(shim), BU34_EIO_PATH=str(fixture)))
                assert b"Input/output error" in result.stderr, result.stderr
                outputs.append((result.returncode, result.stdout, result.stderr.replace(str(name).encode(), b"dd")))
            check(outputs[0] == outputs[1], tier + ": recover one EIO with " + conv + repr(outputs))
        for name in (GNU / "dd", bin / "dd"):
            child = sp.Popen([str(name), "bs=512", "count=2", "status=noxfer"], stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE, start_new_session=True)
            try:
                child.stdin.write(b"ab"); child.stdin.flush()
                ready = select.select([child.stdout], [], [], 2)[0]
                check(bool(ready) and os.read(child.stdout.fileno(), 2) == b"ab", tier + ": bs preserves immediate short read " + str(name))
                child.stdin.write(b"cd"); child.stdin.flush(); child.stdin.close(); child.stdin = None
                stdout, stderr = child.communicate(timeout=10)
                check(child.returncode == 0 and stdout == b"cd" and stderr == b"dd: warning: partial read (2 bytes); suggest iflag=fullblock\n0+2 records in\n0+2 records out\n", tier + ": short record counters " + str(name))
            finally:
                if child.poll() is None: child.kill(); child.wait()
        for name in (GNU / "dd", bin / "dd"):
            child = sp.Popen([str(name), "bs=1", "count=2", "status=noxfer"], stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE, start_new_session=True)
            try:
                # Signal only this child, after its first byte proves it initialized.
                child.stdin.write(b"a"); child.stdin.flush()
                assert select.select([child.stdout], [], [], 3)[0]
                assert os.read(child.stdout.fileno(), 1) == b"a"
                status = Path(f"/proc/{child.pid}/status").read_text()
                print("signal witness", tier, name, re.findall(r"Sig(?:Blk|Ign):\s+[0-9a-f]+", status), flush=True)
                os.kill(child.pid, signal.SIGUSR1)
                child.stdin.write(b"b"); child.stdin.flush(); child.stdin.close(); child.stdin = None
                stdout, stderr = child.communicate(timeout=10)
                check(child.returncode == 0 and stderr.count(b"records in") == 2 and stderr.count(b"records out") == 2,
                      tier + ": USR1 reports while copying " + str(name))
            finally:
                if child.poll() is None: child.kill(); child.wait()
    # GNU's preload distinguishes dynamic libc streams from static/raw IO.
    dynamic, static, wolf = (top / x for x in ("dynamic", "static", "wolf"))
    sp.run(["cc", str(ROOT / "tests/disk-process/stdio.c"), "-o", str(dynamic)], check=True)
    sp.run(["cc", "-static", str(ROOT / "tests/disk-process/stdio.c"), "-o", str(static)], check=True)
    sp.run([str(ROOT / ".wolf-bin/wolf"), "build", "--release", str(ROOT / "tests/disk-process/raw/main.lu"), "-o", str(wolf)], check=True)
    for name, immediate in ((dynamic, True), (static, False), (wolf, True)):
        child = sp.Popen([str(GNU / "stdbuf"), "-o0", str(name)], stdout=sp.PIPE, stderr=sp.PIPE)
        try:
            ready = select.select([child.stdout], [], [], 0.4)[0]
            check(bool(ready) == immediate, "GNU stdbuf -o0 effect: " + name.name)
            stdout, stderr = child.communicate(timeout=10)
            check(child.returncode == 0 and stdout == b"AB\n", "GNU stdbuf child output: " + name.name)
        finally:
            if child.poll() is None: child.kill(); child.wait()
print(f"disk-process: {passed} passed, 0 failed, 0 skipped", flush=True)
