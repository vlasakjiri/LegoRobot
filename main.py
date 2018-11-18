#!/usr/bin/env python3

import time
import sys
from modules.helpers import debug_print
from modules.map_module import Map
from modules.io import IO
from modules.logic import Logic, Moves
from modules.map_saving import Map_saver
from ev3dev.ev3 import Button

def Main():
    map_var = Map()
    io = IO()
    logic = Logic(map_var)
    button = Button()
    saver = Map_saver(map_var, button)
    saver.wait_for_load()
    while(True):
        io.read_sensors()
        sensors = io.directions_free()
        map_var.write_sensor_values(sensors)
        debug_print(map_var)
        move = logic.get_next_move()
        debug_print(map_var.current_position)
        debug_print(map_var.rotation)

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

        if button.any():
            saver.wait_for_load()
        
        saver.save_map()


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
