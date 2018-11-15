#!/usr/bin/env python3

import time
import sys
from modules.helpers import debug_print
from modules.map_module import Map
from modules.io import IO
from modules.logic import Test, Moves
from modules.map_saving import Map_saver


def Main():
    map_var = Map()
    io = IO()
    logic = Test()
    saver = Map_saver(map_var)
    while(True):
        sensors = io.directions_free()
        debug_print(sensors)
        map_var.write_sensor_values(sensors)
        debug_print(map_var)
        move = logic.act(map_var)

        if(move == Moves.left):
            map_var.go_left()
            io.go_left()

        elif(move == Moves.fwd):
            map_var.go_forward()
            io.go_forward()

        elif(move == Moves.right):
            map_var.go_right()
            io.go_right()

        elif(move == Moves.back):
            map_var.go_back()
            io.go_back()

        time.sleep(1)


def test():
    io = IO()
    debug_print(io.lm_left.position_p,
                io.lm_left.position_i, io.lm_left.position_d)

    debug_print(io.lm_left.speed_p,
                io.lm_left.speed_i, io.lm_left.speed_d)
    for i in range(8):
        io._IO__turn_left()
        time.sleep(0.5)


if __name__ == "__main__":
    Main()
