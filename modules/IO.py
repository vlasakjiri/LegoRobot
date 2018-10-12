
import time
from ev3dev2.motor import Motor, LargeMotor
from ev3dev2.sensor.lego import ColorSensor, UltrasonicSensor
from typing import List


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
        self.move_degrees = 500
        self.move_speed = 35
        self.steering_turn_speed = 35
        self.steering_turn_degrees = 270

        # small motor
        self.sm_port = "outC"
        self.sm = Motor(self.sm_port)
        self.sm_turn_speed = 30

        # color sensonr
        self.color_sensor_port = "in1"
        self.color_sensor = ColorSensor(self.color_sensor_port)
        self.color_sensor.mode = ColorSensor.MODE_COL_REFLECT

    def go_left(self):
        self.__turn_left()
        self.__move()

    def go_right(self):
        self.__turn_right()
        self.__move()

    def go_forward(self):
        self.__move()

    def go_back(self):
        self.__turn_around()
        self.__move()

    def __turn_left(self):
        self.__turn(self.steering_turn_speed,
                    -self.steering_turn_speed, self.steering_turn_degrees)

    def __turn_right(self):
        self.__turn(-self.steering_turn_speed,
                    self.steering_turn_speed, self.steering_turn_degrees)

    def __turn_around(self):
        self.__turn(-self.steering_turn_speed,
                    self.steering_turn_speed, self.steering_turn_degrees*2)

    def __turn(self, left_speed: int, right_speed: int, degrees: int)->None:
        self.lm_left.on_for_degrees(left_speed, degrees, block=False)
        self.lm_right.on_for_degrees(right_speed, degrees, block=True)

    def __move(self)->None:
        self.lm_left.on_for_degrees(
            -self.move_speed, self.move_degrees, block=False)
        self.lm_right.on_for_degrees(
            -self.move_speed, self.move_degrees, block=True)

    def directions_free(self)->List[bool]:
        '''
        Returns list of bools (left, center, right), representing if the directions are free to move.
        '''
        values = []  # List[bool]
        self.sm.on_for_degrees(self.sm_turn_speed, 90)
        values.append(self.color_sensor.reflected_light_intensity == 0)
        self.sm.on_for_degrees(-self.sm_turn_speed, 90)
        values.append(self.color_sensor.reflected_light_intensity == 0)
        self.sm.on_for_degrees(-self.sm_turn_speed, 90)
        values.append(self.color_sensor.reflected_light_intensity == 0)
        self.sm.on_for_degrees(self.sm_turn_speed, 90)
        return values
