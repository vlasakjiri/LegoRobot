"""
Provides logic for finding the best move.
"""

from enum import Enum
from modules.map_module import Map, Map_tile, Rotation


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
