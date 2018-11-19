#!/usr/bin/env python3

import time
import sys
from modules.helpers import debug_print
from modules.map_module import Map
from modules.io import IO
from modules.logic import Logic, Moves
from modules.map_saving import Map_saver
from ev3dev.ev3 import Button

# def make_move(map_var, io, move):

#         if(move == Moves.left):
#             map_var.go_left()
#             io.go_left()

#         elif(move == Moves.fwd):
#             map_var.go_forward()
#             io.go_forward()

#         elif(move == Moves.right):
#             map_var.go_right()
#             io.go_right()

#         elif(move == Moves.back):
#             map_var.go_back()
#             io.go_back()


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
    saver = Map_saver(map_var)
    switch = {
        Moves.fwd: lambda: [io.go_forward(), map_var.go_forward()],
        Moves.left: lambda: [io.go_left(), map_var.go_left()],
        Moves.right: lambda: [io.go_right(), map_var.go_right()],
        Moves.back: lambda: [io.go_back(), map_var.go_back()]
    }
    switch[Moves.fwd]()
    while(True):
        io.read_sensors()
        clr_sensor = io.directions_free()
        us_sensor = io.ghost_distance()
        map_var.write_sensor_values(clr_sensor, us_sensor)
        move = logic.get_next_move()
        debug_print(move)
        switch[move]()


def test():
    io = IO()
    while True:
        io._IO__turn_right()
        time.sleep(1)
        io._IO__turn_left()
        time.sleep(1)


def reg_test():
    io = IO()
    while True:
        io._IO__move_reg()
        io.read_sensors()

        if button.any():
            saver.wait_for_load()
        
        saver.save_map()

def sensors_test():
    io = IO()
    for _ in range(8):
        io.read_sensors()
        debug_print("us", io.ultrasonic_sensor_values)
        debug_print("color", io.color_sensor_values)


def range_test():
    io = IO()
    while True:
        io.go_forward()
        # time.sleep(5)
        # io._IO__move()
        # debug_print(io.move_degrees)
        # io.move_degrees += 10
        time.sleep(5)


def io_test():
    io = IO()
    io.go_forward()
    io.read_sensors()
    io.go_left()
    io.read_sensors()
    io.go_forward()
    io.read_sensors()
    io.go_back()
    io.read_sensors()
    io.go_forward()
    io.read_sensors()
    io.go_right()


def turn_test():
    io = IO()
    while True:
        debug_print(io.steering_turn_degrees)
        io._IO__turn_left()
        io.steering_turn_degrees += 10


def around_test():
    io = IO()
    io.go_back()


if __name__ == "__main__":
    io_test()
