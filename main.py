#!/usr/bin/env python3

import os
import sys
import time

from ev3dev.ev3 import Button
from modules.helpers import debug_print
from modules.io import IO
from modules.logic import Logic, Moves
from modules.map_module import Ghost_mapping_type, Map
from modules.map_saving import Map_saver

os.system('setfont Lat15-TerminusBold14')

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
    map_var = Map(Ghost_mapping_type.none)
    io = IO()
    logic = Logic(map_var)
    button = Button()
    saver = Map_saver(map_var, button)
    saver.wait_for_load()
    print("READY")
    motors = {
        Moves.fwd: lambda: io.go_forward(),
        Moves.left: lambda: io.go_left(),
        Moves.right: lambda: io.go_right(),
        Moves.back: lambda: io.go_back()
    }
    mapping = {
        Moves.fwd: lambda: map_var.go_forward(),
        Moves.left: lambda: map_var.go_left(),
        Moves.right: lambda: map_var.go_right(),
        Moves.back: lambda: map_var.go_back()
    }
    motors[Moves.fwd]()
    mapping[Moves.fwd]()
    while(True):
        clr_sensor = io.directions_free()
        us_sensor = io.ghost_distance()
        map_var.write_sensor_values(clr_sensor, us_sensor)
        debug_print(map_var)
        move = logic.get_next_move()
        debug_print(map_var)
        switch[move]()
        if button.any():
            saver.wait_for_load()
        
        ok = motors[move]()
        if(ok is False):
            io.after_crash()
            map_var.rotation += int(move)
            continue
        elif(ok is None):
            saver.wait_for_load()
            continue
        mapping[move]()
        saver.save_map()


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
        io._IO__turn_left()
        time.sleep(.5)
        io._IO__turn_right()
        time.sleep(.5)


def logic_test():
    map_var = Map(Ghost_mapping_type.none)
    logic = Logic(map_var)
    switch = {
        Moves.fwd: lambda: [map_var.go_forward()],
        Moves.left: lambda: [map_var.go_left()],
        Moves.right: lambda: [map_var.go_right()],
        Moves.back: lambda: [map_var.go_back()]
    }
    while(True):
        switch[logic.get_next_move()]()
        print(map_var)
        sensors = [a == "t" for a in input("write values")]
        map_var.write_color_sensor(sensors)


def touch_sensor_test():
    io = IO()
    val = False
    while True:
        debug_print(io.go_forward())
        time.sleep(1)


if __name__ == "__main__":
    Main()
