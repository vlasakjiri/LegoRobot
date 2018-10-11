
from ev3dev2.motor import Motor, LargeMotor
from ev3dev2.sensor.lego import ColorSensor, UltrasonicSensor

class IO():
    """
    Provides functions for high-level IO operations (move left, move forward, is left side free to move etc.).
    """
    def __init__(self):
        self.lm_left = LargeMotor("")
        self.lm_right = LargeMotor("")
        self.sensor_motor = Motor("")
        self.color_sensor = ColorSensor("")
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
        pass
