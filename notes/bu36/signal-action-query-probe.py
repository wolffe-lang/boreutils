#!/usr/bin/env python3
"""Read only this process's signal actions through the documented C API.
No new action is supplied, no signal is sent, no implementation source read.
"""
import ctypes
import json
import platform
import signal

lib = ctypes.CDLL(None, use_errno=True)
lib.sigaction.argtypes = [ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p]
lib.sigaction.restype = ctypes.c_int
for sig in [signal.SIGKILL, signal.SIGSTOP, signal.SIGTERM, signal.SIGPIPE]:
    old = (ctypes.c_long * 128)()
    ctypes.set_errno(0)
    result = lib.sigaction(sig, None, ctypes.byref(old))
    print(json.dumps({
        'host': platform.platform(), 'machine': platform.machine(),
        'operation': 'sigaction(sig, NULL, &old): GET only, no setter',
        'signal': sig.name, 'number': int(sig),
        'return': result, 'errno': ctypes.get_errno(),
    }, sort_keys=True))
