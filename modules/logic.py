"""
Provides logic for finding the best move.
"""

from enum import IntEnum
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
            if(self.mapObj.get_forward_tile_pos(self.mapObj.current_position, rotation, 1) == position):
                return Moves((rotation - self.mapObj.rotation.value).value)

    def get_next_move(self):
        result = self.__get_move(Map_tile.empty)
        if result is not None:
            return result
        result = self.__get_move(Map_tile.not_discovered)
        if result is not None:
            return result
        result = self.__get_move(Map_tile.ghost_path)
        if result is not None:
            return result

    def __get_move(self, tile: Map_tile):
        queue = collections.deque([[self.mapObj.current_position[::-1]]])
        seen = set([self.mapObj.current_position])
        while queue:
            path = queue.popleft()
            x, y = path[-1]
            if self.mapObj.map[y][x] == tile:
                #print(path, queue)
                return self.__move_from_adj_position(path[1][::-1])
<<<<<<< HEAD
            for x2, y2 in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
=======
            #print("---------")
            rotation = self.mapObj.rotation
            for _ in range(4):
                #print(rotation)
                forw_pos = self.mapObj.get_forward_tile_pos((y, x), rotation, 1)
                #print(forw_pos, y, x, self.mapObj.current_position)
                rotation = rotation + 1

                if(forw_pos is None):
                    continue
                
                y2, x2 = forw_pos
>>>>>>> logic
                if 0 <= x2 < 9 and 0 <= y2 < 6 and self.mapObj.map[y2][x2] != Map_tile.wall and (x2, y2) not in seen:
                    queue.append(path + [(x2, y2)])
                    seen.add((x2, y2))


class Moves(IntEnum):
    fwd = 0
    right = 1
    back = 2
    left = 3
