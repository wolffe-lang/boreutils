#!/usr/bin/env python3
import os
import sys
args = sys.argv[1:]
if args and args[0] == 'run':
    args[1:1] = ['--memory', '12g']
    for at, arg in enumerate(args):
        if arg.startswith('bore-') and ':' in arg:
            args[at + 1:at + 1] = ['taskset', '-c', '0-5']
            break
os.execv(os.path.expanduser('~/lanes/hasu-env/bin/podman'), ['podman'] + args)
