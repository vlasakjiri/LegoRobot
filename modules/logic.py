"""
Provides logic for finding the best move.
"""
import numpy as np

from enum import Enum
from map import Map_tile
from map import Rotation
from map import Map


class Test():
    def act(self, mapObj: Map):
        adjacent = []
        adjacent.append(mapObj.get_forward_tile_value())
        mapObj.rotation += 1
        adjacent.append(mapObj.get_forward_tile_value())
        mapObj.rotation += 1
        adjacent.append(mapObj.get_forward_tile_value())
        mapObj.rotation += 1
        adjacent.append(mapObj.get_forward_tile_value())

        try:
            return Moves(adjacent.index(Map_tile.empty))
        except ValueError:
            return Moves(adjacent.index(Map_tile.empty_driven_through))


class Moves(Enum):
    fwd = 0
    right = 1
    back = 2
    left = 3
