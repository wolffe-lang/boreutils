#!/usr/bin/env python3
"""Construct utmp(5)'s Linux x86-64 ABI, not libc implementation data."""
from pathlib import Path
import struct

def record(kind, user='', line='', host='', pid=42, ident='ab', seconds=946818245):
    b=bytearray(384)
    struct.pack_into('<h',b,0,kind)
    struct.pack_into('<i',b,4,pid)
    for at,size,text in [(8,32,line),(40,4,ident),(44,32,user),(76,256,host)]:
        data=text.encode()[:size]
        b[at:at+len(data)]=data
    struct.pack_into('<i',b,340,seconds)
    return b

if __name__ == '__main__':
    root=Path(__file__).resolve().parents[1]/'fixtures'
    rows=[record(7,'zed','pts/999','host.example:0'),record(7,'amy','tty9'),
          record(7,'zed','tty8'),record(6,line='tty1'),record(5,line='tty2'),
          record(8,'old','tty3'),record(2,'reboot','~'),
          record(1,'runlevel','~',pid=ord('5')+ord('3')*256),
          record(3,'date','|'),record(4,'date','{')]
    (root/'bu35-logins.utmp').write_bytes(b''.join(rows))
    (root/'bu35-empty.utmp').write_bytes(b'')
    (root/'bu35-truncated.utmp').write_bytes(b''.join(rows[:2])+b'\x07'*17)
