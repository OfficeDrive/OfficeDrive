#!/usr/bin/python -u

import os

from shutil import copyfile
from mpsh import MPlayer


p = MPlayer(options={'attach' : 1})
p.savefd()
