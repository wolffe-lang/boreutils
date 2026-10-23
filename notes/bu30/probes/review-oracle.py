#!/usr/bin/env python3
"""GNU 9.11 review measurements, only in the lane's oracle container."""
import os
from pathlib import Path
import subprocess
import tempfile

root = Path(__file__).resolve().parents[4]
gnu = root / '.gnu-bin/bin'
cases = [
    ('2 empty reference relative', 'truncate', ['-r', '', '-s', '+1', 'f']),
    ('2 empty reference alone', 'truncate', ['-r', '', 'f']),
    ('3 fifo', 'truncate', ['-s', '0', 'fifo']),
    ('3 fifo no-create', 'truncate', ['-c', '-s', '0', 'fifo']),
    ('3 fifo symlink', 'truncate', ['-s', '0', 'lfifo']),
    ('4 link target slash existing', 'realpath', ['-e', 'lf']),
    ('4 link target slash E', 'realpath', ['-E', 'lf']),
    ('4 readlink target slash existing', 'readlink', ['-e', 'lf']),
    ('5 cyclic prefix recovers', 'realpath', ['-m', 'cycle/../l']),
    ('5 readlink cyclic prefix recovers', 'readlink', ['-m', 'cycle/../l']),
    ('6 empty relative-to', 'realpath', ['--relative-to=', 'f']),
    ('6 empty relative-base', 'realpath', ['--relative-base=', 'f']),
    ('U write-only sync', 'sync', ['f']),
    ('U write-only data sync', 'sync', ['-d', 'f']),
]
for label, utility, args in cases:
    with tempfile.TemporaryDirectory(prefix='bu30-oracle-review.') as top:
        p = Path(top)
        (p/'f').write_bytes(b'abcdef')
        (p/'d').mkdir()
        (p/'lf').symlink_to('f/')
        (p/'l').symlink_to('d')
        (p/'cycle').symlink_to('cycle')
        os.mkfifo(p/'fifo')
        (p/'lfifo').symlink_to('fifo')
        if label.startswith('U '): (p/'f').chmod(0o200)
        print(label, 'uid', os.geteuid(), 'argv', args, flush=True)
        try:
            done = subprocess.run([utility]+args, executable=str(gnu/utility), cwd=top,
                                  stdin=subprocess.DEVNULL, capture_output=True, timeout=2,
                                  env={'PATH':str(gnu)+':/usr/bin:/bin','LC_ALL':'C'})
            print('exit',done.returncode,'stdout',repr(done.stdout),'stderr',repr(done.stderr),flush=True)
        except subprocess.TimeoutExpired:
            print('BOUNDED TIMEOUT 2 seconds',flush=True)
