#!/usr/bin/env python3

import time

from modules.helpers import *
from modules.IO import IO
import os

def Main():
	os.system("setfont Lat15-Terminus24x12")
	io = IO()
	for _ in range(100):
		print(io.directions_free())
		time.sleep(0.3)

if __name__ == "__main__":
    Main()