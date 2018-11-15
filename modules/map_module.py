from enum import Enum
from modules.helpers import debug_print


class Map_tile(Enum):
    empty = 0
    empty_driven_through = 1
    not_discovered = 2
    wall = 3
    ghost_path = 4
    robot = 5


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


class Map():
    """
    Provides functions for reading and modifying the enviroment.
    0,0 is at the top left, first y axis, then x axis.
    """

    def __init__(self):
        self.rotation = Rotation.up
        self.current_position = (3, 4)
        self.map = []
        for _ in range(6):
            self.map.append([Map_tile.not_discovered] * 9)
        self.shape = (6, 9)
        self.map[3][4] = Map_tile.robot
        self.map[3][3] = Map_tile.wall
        self.map[3][5] = Map_tile.wall
        self.map[2][4] = Map_tile.empty

    def __get_forward_tile_pos__(self, position, rotation):
        if rotation == Rotation.up:
            if position[0] - 1 < 0:
                return None
            return (position[0] - 1, position[1])

        if rotation == Rotation.right:
            if position[1] + 1 >= self.shape[1]:
                return None
            return (position[0], position[1] + 1)

        if rotation == Rotation.down:
            if position[0] + 1 >= self.shape[0]:
                return None
            return (position[0] + 1, position[1])

        if rotation == Rotation.left:
            if position[1] - 1 < 0:
                return None
            return (position[0], position[1] - 1)

    def get_forward_tile_value(self, rotation):
        fwd_pos = self.__get_forward_tile_pos__(self.current_position,
                                                rotation)
        if fwd_pos is None:
            return None

        return self.map[fwd_pos[0]][fwd_pos[1]]

    def go_forward(self):
        debug_print("go fwd")

        self.map[self.current_position[0]][self.current_position[1]
                                           ] = Map_tile.empty_driven_through

        self.current_position = self.__get_forward_tile_pos__(
            self.current_position, self.rotation)
        self.map[self.current_position[0]
                 ][self.current_position[1]] = Map_tile.robot

    def go_left(self):
        debug_print("go left")
        self.rotation = self.rotation - 1
        self.go_forward()

    def go_right(self):
        debug_print("go right")

        self.rotation = self.rotation + 1
        self.go_forward()

    def go_back(self):
        debug_print("go back")

        self.rotation = self.rotation + 2
        self.go_forward()

    def write_sensor_values(self, values):
        """
            Expects input in array of bools
            [left, up, right]
            1 = empty
            0 = wall
        """
        for i in range(-1, 2):
            to_set = Map_tile.wall
            if values[i + 1]:
                to_set = Map_tile.empty

            fwd_pos = self.__get_forward_tile_pos__(
                self.current_position, self.rotation + i)
            if(fwd_pos is not None):
                self.map[fwd_pos[0]][fwd_pos[1]] = to_set

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
