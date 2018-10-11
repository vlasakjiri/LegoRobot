
import time

from ev3dev2.motor import Motor, LargeMotor
from ev3dev2.sensor.lego import ColorSensor, UltrasonicSensor


class IO():
    """
    Provides functions for high-level IO operations (move left, move forward, is left side free to move etc.).
    """
    def __init__(self):
        self.lm_left = LargeMotor("outB")
        self.lm_right = LargeMotor("outA")
        self.sensor_motor = Motor("outC")
        self.color_sensor = ColorSensor("in1")
        self.color_sensor.mode = ColorSensor.MODE_COL_REFLECT

    
    def go_left(self):
        pass

    def go_right(self):
        pass

    def go_forward(self):
        pass

    def go_back(self):
        pass

    def __turn_left(self):
        pass
        
    def __turn_right(self):
        pass
    
    def __turn_around(self):
        pass

    def directions_free(self):
        '''
        Returns tuple of bools of sides (left, center, right)
        '''
        values = []
        self.sensor_motor.on_for_degrees(-20, 90)
        values.append(self.color_sensor.reflected_light_intensity)
        time.sleep(0.5)
        self.sensor_motor.on_for_degrees(20, 90)
        values.append(self.color_sensor.reflected_light_intensity)
        time.sleep(0.5)        
        self.sensor_motor.on_for_degrees(20, 90)
        values.append(self.color_sensor.reflected_light_intensity)
        time.sleep(0.5)        
        self.sensor_motor.on_for_degrees(-20,90)
        return values

