from enum import Enum, IntEnum
from modules.helpers import debug_print


class Map_tile(IntEnum):
    empty = 0
    empty_driven_through = 1
    not_discovered = 2
    wall = 3
    ghost_path = 4
    robot = 5
    ghost = 6


class Ghost_mapping_type(IntEnum):
    none = 0
    static = 1
    rows = 2
    columns = 4


class Rotation(IntEnum):
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

    def __init__(self, mapping_type):
        self.rotation = Rotation.up
        self.current_position = (3, 4)
        self.map = []
        for _ in range(6):
            self.map.append([Map_tile.not_discovered] * 9)
        self.shape = (6, 9)
        self.mapping_type = mapping_type
        self.map[3][4] = Map_tile.robot
        self.map[3][3] = Map_tile.wall
        self.map[3][5] = Map_tile.wall
        self.map[2][4] = Map_tile.empty

    def load_map_data(self, map_data):
        self.rotation = Rotation.up
        self.current_position = (3, 4)
        self.map = map_data
        self.shape = (6, 9)
        self.map[3][4] = Map_tile.robot
        self.map[3][3] = Map_tile.wall
        self.map[3][5] = Map_tile.wall
        self.map[2][4] = Map_tile.empty

    def get_forward_tile_pos(self, position, rotation, cells):
        if rotation == Rotation.up:
            if position[0] - cells < 0:
                return None
            return (position[0] - cells, position[1])

        if rotation == Rotation.right:
            if position[1] + cells >= self.shape[1]:
                return None
            return (position[0], position[1] + cells)

        if rotation == Rotation.down:
            if position[0] + cells >= self.shape[0]:
                return None
            return (position[0] + cells, position[1])

        if rotation == Rotation.left:
            if position[1] - cells < 0:
                return None
            return (position[0], position[1] - cells)

    def get_forward_tile_value(self, rotation):
        fwd_pos = self.get_forward_tile_pos(self.current_position,
                                            rotation, 1)
        if fwd_pos is None:
            return None

        return self.map[fwd_pos[0]][fwd_pos[1]]

    def go_forward(self):

        self.map[self.current_position[0]][self.current_position[1]
                                           ] = Map_tile.empty_driven_through

        self.current_position = self.get_forward_tile_pos(
            self.current_position, self.rotation, 1)
        self.map[self.current_position[0]
                 ][self.current_position[1]] = Map_tile.robot

    def go_left(self):
        self.rotation = self.rotation - 1
        self.go_forward()

    def go_right(self):
        self.rotation = self.rotation + 1
        self.go_forward()

    def go_back(self):
        self.rotation = self.rotation + 2
        self.go_forward()

    def write_color_sensor(self, values):
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

            fwd_pos = self.get_forward_tile_pos(
                self.current_position, self.rotation + i, 1)
            if(fwd_pos is not None and self.map[fwd_pos[0]][fwd_pos[1]] is not Map_tile.empty_driven_through):
                self.map[fwd_pos[0]][fwd_pos[1]] = to_set

    def ghost_static(self, pos):
        self.map[pos[0]][pos[1]] = Map_tile.ghost

    def write_us_values(self, values):
        for i in range(-1, 2):
            distance = values[i+1]
            if(distance is not None):
                fwd_pos = self.get_forward_tile_pos(
                    self.current_position, self.rotation + i, distance)
                if(fwd_pos is not None):
                    if(self.mapping_type == Ghost_mapping_type.static):
                        self.ghost_static(fwd_pos)

    def write_sensor_values(self, clr_sensor, us_sensor):
        self.write_color_sensor(clr_sensor)
        self.write_us_values(us_sensor)

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
