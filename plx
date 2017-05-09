#!/usr/bin/python3

import os
import sys
from Playx import *

import argparse

argp = argparse.ArgumentParser()

argp.add_argument('-c', '--current-directory', action="store_true", help="only search files under current DIR")
argp.add_argument("arguments", nargs='*')

opt = argp.parse_args(sys.argv[1:])
args = opt.arguments

if len(args) < 1: raise Exception("no filename given")

home = os.getenv("HOME")
fcfg = home + "/.playx.py"

onlyUnderDir = ""
if opt.current_directory:
	onlyUnderDir = os.path.abspath('.')

p = Playx(fcfg, args,
	onlyUnderDir = onlyUnderDir
)

print("playing `%s' with `%s'" % (p.fname, p.player))
p.play()
