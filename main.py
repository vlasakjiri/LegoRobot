#!/usr/bin/env python3

import time

import modules.helpers as helpers
from modules.io import IO


def Main():
    io = IO()
    while(True):
        helpers.debug_print(io.directions_free())
        time.sleep(5)


if __name__ == "__main__":
    Main()
