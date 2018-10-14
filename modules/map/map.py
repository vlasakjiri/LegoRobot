import numpy as np
from map_tile import Map_tile
from rotation import Rotation

class Map():
    """
    Provides functions for reading and modifying the enviroment.
    """

    def __init__(self):
        self.rotation = Rotation.up
        self.current_position = (3, 4)
        self.map = np.full((6, 9), dtype=Map_tile, fill_value=Map_tile.not_discovered)
        self.map[3, 4] = Map_tile.robot
        self.map[3, 3] = Map_tile.wall
        self.map[3, 5] = Map_tile.wall
        self.map[2, 4] = Map_tile.empty

    def __get_forward_tile_pos(self, position, rotation):
        if rotation == Rotation.up:
            return (position[0] - 1, position[1])
        if rotation == Rotation.right:
            return (position[0], position[1] + 1)
        if rotation == Rotation.down:
            return (position[0] + 1, position[1])
        if rotation == Rotation.left:
            return (position[0], position[1] - 1)

    def go_forward(self):
        self.map[self.current_position] = Map_tile.empty_driven_through
        self.current_position = self.__get_forward_tile_pos(self.current_position, self.rotation)
        self.map[self.current_position] = Map_tile.robot        

    def go_left(self):
        self.rotation = self.rotation - 1
        self.go_forward()

    def go_right(self):
        self.rotation = self.rotation + 1
        self.go_forward()

    def go_back(self):
        self.rotation = self.rotation + 2
        self.go_forward()

    def write_sensor_values(self, values):
        """
            Expects input in array of bools
            [left, up, right]
            1 = empty 
            0 = wall
        """
        for i in range(-1, 2, 1):
            to_set = Map_tile.wall
            if values[i + 1]:
                to_set = Map_tile.empty    
            
            self.map[self.__get_forward_tile_pos(self.current_position, self.rotation + i)] = to_set

    def __str__(self):
        ret_str = ""
        for row in self.map:
            for cell in row:
                if not cell == Map_tile.not_discovered:
                    ret_str += str(cell.value)
                else:
                    ret_str += "*"    
            
            ret_str += "\n"

        return ret_str