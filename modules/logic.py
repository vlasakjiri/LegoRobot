"""
Provides logic for finding the best move.
"""

from enum import Enum
from modules.map_module import Map, Map_tile, Rotation
from queue import Queue
import collections

class Logic():
    def __init__(self, mapObj: Map):
        self.mapObj = mapObj

    def __move_from_adj_position(self, position: tuple):
        rotation = self.mapObj.rotation
        for _ in range(4):
            rotation += 1
            if(self.mapObj.get_forward_tile_pos(self.mapObj.current_position, rotation) == position):
                return Moves((rotation - self.mapObj.rotation.value).value)
                


    def get_next_move(self) -> tuple:
        queue = collections.deque([[self.mapObj.current_position]])
        seen = set([self.mapObj.current_position])
        while queue:
            path = queue.popleft()
            x, y = reversed(path[-1])
            if self.mapObj.map[y][x] == Map_tile.empty or self.mapObj.map[y][x] == Map_tile.not_discovered or self.mapObj.map[y][x] == Map_tile.ghost_path:
                return self.__move_from_adj_position(path[1])
            for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1)):
                if 0 <= x2 < 9 and 0 <= y2 < 6 and self.mapObj.map[y2][x2] != Map_tile.wall and (x2, y2) not in seen:
                    queue.append(path + [(x2, y2)])
                    seen.add((x2, y2))
                    
class Moves(Enum):
    fwd = 0
    right = 1
    back = 2
    left = 3
