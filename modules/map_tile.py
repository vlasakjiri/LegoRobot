from enum import Enum

class Map_tile(Enum):
    empty = 0
    wall = 1
    boundary_wall = 2
    ghost_path = 3