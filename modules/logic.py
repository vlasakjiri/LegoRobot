"""
Provides logic for finding the best move.
"""

from enum import Enum
from modules.map_module import Map, Map_tile, Rotation
from queue import Queue

class Logic():
    def __init__(self, mapObj: Map):
        self.mapObj = mapObj

    def __get_dist(self, target: tuple):
        curr_pos = self.mapObj.current_position
        return (abs(curr_pos[0] - target[0]), abs(curr_pos[1] - target[1]))

    def __get_move(self, position: tuple):
        pass

    def get_next_move(self):
        position = (-1, -1)
        min_dist = 999

        for col_num in range(0, len(self.mapObj.map)):
            for row_num in range(self.mapObj.map[col_num]):
                distance = self.__get_dist((col_num, row_num))
                tile = self.mapObj.map[col_num][row_num]
                if(tile is Map_tile.empty or tile is Map_tile.not_discovered):
                    if(distance < min_dist):
                        min_dist = distance
                        position = (col_num, row_num)
        
        return self.__get_move(position)
        


class Moves(Enum):
    fwd = 0
    right = 1
    back = 2
    left = 3
