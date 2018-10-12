#!/usr/bin/env python3

import time

from modules.helpers import *
from modules.io import IO


def Main():
    io = IO()
    while(True):
        debug_print(io.directions_free())
        time.sleep(5)


if __name__ == "__main__":
    Main()
