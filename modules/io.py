
import time
from ev3dev2.motor import Motor, LargeMotor
from ev3dev2.sensor.lego import ColorSensor, UltrasonicSensor, TouchSensor
from typing import List
from math import sqrt
from modules.helpers import debug_print
from threading import Thread


class IO():
    """
    Provides functions for high-level IO operations (move left, move forward, is left side free to move etc.).
    """

    def __init__(self):
        # Large motors
        self.lm_left_port = "outB"
        self.lm_right_port = "outA"
        self.lm_left = LargeMotor(self.lm_left_port)
        self.lm_right = LargeMotor(self.lm_right_port)
        # distance at which sensor motor start moving
        self.move_sensor_check_degrees = 400
        self.move_degrees = 570  # one tile distance
        self.move_speed = 35
        self.after_crash_degrees = 200
        self.steering_turn_speed = 30  # turning left or right
        self.steering_turn_degrees = 450
        self.steering_turn_fwd_degrees = 150  # distance to move after turning
        # distance at which sensors start spinning
        self.steering_sensor_check_degrees = 50

        # small motor
        self.sm_port = "outC"
        self.sm = Motor(self.sm_port)
        self.sm_turn_speed = 30
        self.sm_center_turn_angle = 90
        self.sm_side_turn_angle = 110
        self.sm_is_left = False

        # color sensor
        self.color_sensor_port = "in1"
        self.color_sensor = ColorSensor(self.color_sensor_port)
        self.color_sensor.mode = ColorSensor.MODE_COL_REFLECT
        self.color_sensor_values = []

        # regulations
        self.regulation_desired_value = 4
        self.regulation_max_diff = 3
        self.regulation_p = 1.5
        self.regulation_tick = 0.03

        # ultrasonic sensor
        self.ultrasonic_sensor_port = "in4"
        self.ultrasonic_sensor = UltrasonicSensor(self.ultrasonic_sensor_port)
        self.ultrasonic_sensor.mode = 'US-DIST-CM'
        self.ultrasonic_tile_length = 30
        self.ultrasonic_max_value = 255
        self.ultrasonic_sensor_values = []

        # touch sensors
        self.touch_right = TouchSensor("in2")
        self.touch_left = TouchSensor("in3")

    def go_left(self):
        ok = self.__turn_left()
        if(ok):
            ok = self.__move_reg(self.steering_turn_fwd_degrees,
                                 self.steering_sensor_check_degrees)
        return ok

    def go_right(self):
        ok = self.__turn_right()
        if(ok):
            ok = self.__move_reg(self.steering_turn_fwd_degrees,
                                 self.steering_sensor_check_degrees)
        return ok

    def go_forward(self):
        return self.__move_reg(self.move_degrees, self.move_sensor_check_degrees)

    def go_back(self):
        self.__turn(stop_motor=self.lm_left, turn_motor=self.lm_right,
                    degrees=self.steering_turn_degrees, speed=self.steering_turn_speed)
        return self.__turn(stop_motor=self.lm_right, turn_motor=self.lm_left,
                           degrees=self.steering_turn_degrees, speed=-self.steering_turn_speed)

    def after_crash(self):
        debug_print("crash")
        self.__move(self.after_crash_degrees, self.move_speed)
        self.read_sensors()

    def __turn(self, stop_motor: Motor, turn_motor: Motor, degrees: int, speed: int):
        stop_motor.stop()
        start = turn_motor.degrees
        turn_motor.on(speed)
        while(abs(turn_motor.degrees - start) < degrees):
            if(not self.__check_button()):
                self.lm_left.stop()
                self.lm_right.stop()
                return False
        return True

    def __turn_left(self):
        return self.__turn(stop_motor=self.lm_left, turn_motor=self.lm_right,
                           degrees=self.steering_turn_degrees, speed=-self.steering_turn_speed)

    def __turn_right(self):
        return self.__turn(stop_motor=self.lm_right, turn_motor=self.lm_left,
                           degrees=self.steering_turn_degrees, speed=-self.steering_turn_speed)

    def __move(self, degrees, speed)->None:
        self.lm_left.on_for_degrees(
            speed, degrees, block=False)
        self.lm_right.on_for_degrees(
            speed, degrees, block=True)

    def __reg(self):
        val = self.color_sensor.reflected_light_intensity
        diff = (self.regulation_desired_value - val)
        if diff >= 0 and val > 0:
            diff = min(diff, self.regulation_max_diff)
        elif val == 0:
            diff = 0
        else:
            diff = -min(abs(diff), self.regulation_max_diff)
        diff *= self.regulation_p
        if self.sm_is_left:
            return (-self.move_speed + diff, -self.move_speed - diff)

        return (-self.move_speed - diff, -self.move_speed + diff)

    def __check_button(self):
        timeout = time.time() + self.regulation_tick
        while(time.time() <= timeout):  # check for touch sensor
            if(self.touch_left.is_pressed or self.touch_right.is_pressed):
                return False
            time.sleep(0.01)
        return True

    def __move_reg(self, degrees, sensor_degrees):
        t = Thread(target=self.read_sensors)
        start_l, start_r = (self.lm_left.degrees, self.lm_right.degrees)
        distance_l, distance_r = 0, 0
        while (distance_l < degrees
               or distance_r < degrees):
            speed_l, speed_r = self.__reg()
            self.lm_left.on(speed_l, brake=True)
            self.lm_right.on(speed_r, brake=True)
            if(not self.__check_button()):
                self.lm_left.stop()
                self.lm_right.stop()
                return False
            if((distance_l >= sensor_degrees or distance_r >= sensor_degrees)
               and not t.isAlive()):
                t.start()

            distance_l = abs(start_l - self.lm_left.degrees)
            distance_r = abs(start_r - self.lm_right.degrees)
        t.join()
        return True

    def read_sensors(self):
        self.color_sensor_values = []  # List[float]
        self.ultrasonic_sensor_values = []
        speed = self.sm_turn_speed
        if(self.sm_is_left):
            speed = -self.sm_turn_speed

        # side 1
        self.color_sensor_values.append(
            self.color_sensor.reflected_light_intensity)
        self.ultrasonic_sensor_values.append(
            self.ultrasonic_sensor.distance_centimeters)

        # center
        self.sm.on_for_degrees(speed, self.sm_center_turn_angle)
        self.color_sensor_values.append(
            self.color_sensor.reflected_light_intensity)
        self.ultrasonic_sensor_values.append(
            self.ultrasonic_sensor.distance_centimeters)

        # side 2
        self.sm.on_for_degrees(speed, self.sm_side_turn_angle)
        self.color_sensor_values.append(
            self.color_sensor.reflected_light_intensity)
        self.ultrasonic_sensor_values.append(
            self.ultrasonic_sensor.distance_centimeters)

        if not self.sm_is_left:
            self.ultrasonic_sensor_values.reverse()
            self.color_sensor_values.reverse()
        self.sm_is_left = not self.sm_is_left

    def directions_free(self)->List[bool]:
        '''
        Returns list of bools (left, center, right), representing if the directions are free to move.
        '''
        return [a == 0 for a in self.color_sensor_values]

    def ghost_distance(self)->List[int]:
        '''
        Returns list of ints (left, center, right), representing the distance from closest ghost.
        '''
        return [int(a) // self.ultrasonic_tile_length
                if a < self.ultrasonic_max_value and a // self.ultrasonic_tile_length > 0
                else None
                for a in self.ultrasonic_sensor_values]
