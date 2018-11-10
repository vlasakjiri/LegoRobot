#!/usr/bin/env python3

import time
import sys
import modules.helpers as helpers
from modules.map_module import Map
from modules.io import IO
from modules.logic import Test, Moves
from modules.map_saving import Map_saver

def Main():
    map = Map()
    io = IO()
    logic = Test()
    saver = Map_saver(map)
    while(True):
        sensors = io.directions_free()
        helpers.debug_print(sensors)
        map.write_sensor_values(sensors)
        helpers.debug_print(map)
        move = logic.act(map)
        helpers.debug_print(map.current_position)
        helpers.debug_print(map.rotation)

        if(move == Moves.left):
            map.go_left()
            io.go_left()

        elif(move == Moves.fwd):
            helpers.debug_print("fwd")
            map.go_forward()
            io.go_forward()

        elif(move == Moves.right):
            map.go_right()
            io.go_right()

        elif(move == Moves.back):
            map.go_back()
            io.go_back()

        time.sleep(1)


def test():
    io = IO()
    helpers.debug_print(io.lm_left.position_p,
                        io.lm_left.position_i, io.lm_left.position_d)

    helpers.debug_print(io.lm_left.speed_p,
                        io.lm_left.speed_i, io.lm_left.speed_d)
    for i in range(8):
        io._IO__turn_left()
        time.sleep(0.5)


if __name__ == "__main__":
    # Main()
    test()
