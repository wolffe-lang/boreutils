#!/usr/bin/env python3
"""PAX live-image login regression, run on a disposable QEMU boot.

Prediction before implementation: the image's current tools reject the x86-64
PAX ABI; after accepting that layout, empty who/users succeed, a constructed
USER_PROCESS is listed, and uptime identifies missing procfs sources.
The 384-byte record and field offsets are documented in utmp(5) and in
PAX's login record writer at pax#453 (user/auth/utmp.lu). The image and
guest are disposable.
"""
import os
import re
import socket
import subprocess
import sys
import time

image = os.path.abspath(sys.argv[1])
scratch = os.environ['TL42_SCRATCH']
path = os.path.join(scratch, 'pax-login-serial.sock')
try:
    os.unlink(path)
except FileNotFoundError:
    pass
cmd = ['qemu-system-x86_64', '-enable-kvm', '-m', '2048', '-smp', '2',
       '-cdrom', image, '-boot', 'd', '-display', 'none', '-monitor', 'none',
       '-serial', 'unix:' + path + ',server=on,wait=off', '-no-reboot']
record = bytearray(384)
record[0] = 7
record[8:12] = b'tty0'
record[44:49] = b'alice'
fixture = ''.join('\\%03o' % b for b in record)
commands = [
    "who >/tmp/tl42-out 2>/tmp/tl42-err; if test $? -eq 0 && test ! -s /tmp/tl42-out; then echo PASS-who-empty; else echo FAIL-who-empty; cat /tmp/tl42-err; fi",
    "users >/tmp/tl42-out 2>/tmp/tl42-err; if test $? -eq 0 && test ! -s /tmp/tl42-out; then echo PASS-users-empty; else echo FAIL-users-empty; cat /tmp/tl42-err; fi",
    "pinky >/tmp/tl42-out 2>/tmp/tl42-err; if test $? -eq 0; then echo PASS-pinky-abi; else echo FAIL-pinky-abi; cat /tmp/tl42-err; fi",
    "uptime >/tmp/tl42-out 2>/tmp/tl42-err; if test $? -ne 0 && grep /proc/uptime /tmp/tl42-err && grep /proc/loadavg /tmp/tl42-err; then echo PASS-uptime-sources; else echo FAIL-uptime-sources; cat /tmp/tl42-err; fi",
    "printf '" + fixture + "' > /tmp/tl42-utmp; echo TL42_WROTE",
    "who /tmp/tl42-utmp >/tmp/tl42-out 2>/tmp/tl42-err; if grep alice /tmp/tl42-out; then echo PASS-who-record; else echo FAIL-who-record; cat /tmp/tl42-err; fi",
    "echo TL42_COMPLETE",
]
q = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
s = socket.socket(socket.AF_UNIX)
data = b''
try:
    for _ in range(100):
        try:
            s.connect(path)
            break
        except (FileNotFoundError, ConnectionRefusedError):
            time.sleep(.1)
    else:
        raise RuntimeError('serial socket unavailable')
    s.settimeout(1)
    end = time.monotonic() + 90
    sent = False
    done = re.compile(rb'\r\n(PASS-|FAIL-)\S+\r\n|\r\nTL42_WROTE\r\n')
    seen = 0
    while time.monotonic() < end:
        try:
            chunk = s.recv(65536)
        except socket.timeout:
            continue
        if not chunk:
            break
        data += chunk
        if not sent and b'run 1: /bin/env' in data and b'$ ' in data:
            time.sleep(1)
            sent = True
            seen = len(data)
            pending = list(commands)
            s.sendall((pending.pop(0) + '\r').encode())
        elif sent and pending:
            # One command at a time: a burst of typed lines is lost or
            # garbled on the serial console while the shell is busy.
            tail = data[seen:]
            if done.search(tail) and tail.endswith(b'$ '):
                seen = len(data)
                s.sendall((pending.pop(0) + '\r').encode())
        if b'\r\nTL42_COMPLETE\r\n' in data:
            break
    sys.stdout.buffer.write(data)
    if b'\r\nTL42_COMPLETE\r\n' not in data:
        raise RuntimeError('guest did not complete rows')
    names = ('who-empty', 'users-empty', 'pinky-abi', 'uptime-sources', 'who-record')
    failed = False
    for name in names:
        ok = ('\r\nPASS-' + name + '\r\n').encode() in data
        print(('PASS ' if ok else 'FAIL ') + name, flush=True)
        failed |= not ok
    sys.exit(int(failed))
finally:
    q.terminate()
    q.wait(timeout=5)
    s.close()
