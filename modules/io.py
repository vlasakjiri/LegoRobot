
import time
from ev3dev2.motor import Motor, LargeMotor
from ev3dev2.sensor.lego import ColorSensor, UltrasonicSensor, TouchSensor
from typing import List
from math import sqrt
from modules.helpers import debug_print


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
        self.move_degrees = 570
        self.move_speed = 35
        self.steering_turn_speed = 30
        self.steering_turn_degrees = 450
        self.steering_turn_fwd_degrees = 150

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
        self.regulation_desired_value = 2
        self.regulation_max_diff = 2
        self.regulation_p = 2.5
        self.move_time = 1
        self.regulation_tick = 0.03

        # ultrasonic sensor
        self.ultrasonic_sensor_port = "in4"
        self.ultrasonic_sensor = UltrasonicSensor(self.ultrasonic_sensor_port)
        self.ultrasonic_sensor.mode = 'US-DIST-CM'
        self.ultrasonic_tile_length = 30
        self.ultrasonic_max_value = 255
        self.ultrasonic_sensor_values = []

    def go_left(self):
        self.__turn_left()
        self.__move_reg(self.steering_turn_fwd_degrees)

    def go_right(self):
        self.__turn_right()
        self.__move_reg(self.steering_turn_fwd_degrees)

    def go_forward(self):
        self.__move_reg(self.move_degrees)

    def go_back(self):
        self.lm_left.stop()
        self.lm_right.on_for_degrees(
            self.steering_turn_speed, self.steering_turn_degrees)
        self.__turn_right()

    def __turn_left(self):
        self.lm_left.stop()
        self.lm_right.on_for_degrees(-self.steering_turn_speed,
                                     self.steering_turn_degrees)

    def __turn_right(self):
        self.lm_right.stop()
        self.lm_left.on_for_degrees(-self.steering_turn_speed,
                                    self.steering_turn_degrees)

    def __move(self, degrees)->None:
        self.lm_left.on_for_degrees(
            -self.move_speed, degrees, block=False)
        self.lm_right.on_for_degrees(
            -self.move_speed, degrees, block=True)

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

    def __move_reg(self, degrees):
        start_l, start_r = (self.lm_left.degrees, self.lm_right.degrees)
        while (abs(start_l - self.lm_left.degrees) < degrees
               or abs(start_r - self.lm_right.degrees) < degrees):
            speed_l, speed_r = self.__reg()
            self.lm_left.on(speed_l, brake=True)
            self.lm_right.on(speed_r, brake=True)
            time.sleep(self.regulation_tick)
        self.lm_left.stop()
        self.lm_right.stop()

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
