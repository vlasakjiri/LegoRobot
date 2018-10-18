from enum import Enum

class Rotation(Enum):
    up = 0
    right = 1
    down = 2
    left = 3

    def __add__(self, other):
        return Rotation((self.value + other) % 4)
    
    def __sub__(self, other):
        if(other > self.value):
            return Rotation((self.value - other) % 4)
        else:
            return Rotation(self.value - other)