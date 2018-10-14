from enum import Enum

class Map_tile(Enum):
    empty = 0
    empty_driven_through = 1
    not_discovered = 2
    wall = 3
    ghost_path = 4
    robot = 5