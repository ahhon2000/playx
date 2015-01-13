#!/usr/bin/python3

import os
import sys
from Playx import *

if len(sys.argv) < 2: raise Exception("no filename given")
args = sys.argv[1:]

home = os.getenv("HOME")
fcfg = home + "/.playx.py"

p = Playx(fcfg, args)

p.play()
