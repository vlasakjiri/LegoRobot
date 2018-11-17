#!/usr/bin/env python3

import time
import sys
from modules.helpers import debug_print
from modules.map_module import Map
from modules.io import IO
from modules.logic import Logic, Moves
from modules.map_saving import Map_saver


def Main():
    map_var = Map()
    io = IO()
    logic = Logic(map_var)
    saver = Map_saver(map_var)
    while(True):
        io.read_sensors()
        sensors = io.directions_free()
        map_var.write_sensor_values(sensors)
        helpers.debug_print(map_var)
        move = logic.get_next_move()
        helpers.debug_print(map_var.current_position)
        helpers.debug_print(map_var.rotation)

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
    for _ in range(8):
        io._IO__turn_left()
        time.sleep(0.5)


if __name__ == "__main__":
    Main()
