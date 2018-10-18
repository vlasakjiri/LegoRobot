#!/usr/bin/env python3

import time

import modules.helpers as helpers
from modules.map import Map
from modules.io import IO
from modules.logic import Test, Moves


def Main():
    map = Map()
    io = IO()
    logic = Test()
    while(True):
        sensors = io.directions_free()
        helpers.debug_print(sensors)
        map.write_sensor_values(sensors)
        helpers.debug_print(map)
        move = logic.act(map)

        if(move == Moves.left):
            map.go_left()
            io.go_left()

        elif(move == Moves.fwd):
            map.go_forward()()
            io.go_forward()

        elif(move == Moves.right):
            map.go_right()
            io.go_right()

        elif(move == Moves.back):
            map.go_back()
            io.go_back()

        time.sleep(5)


if __name__ == "__main__":
    Main()
