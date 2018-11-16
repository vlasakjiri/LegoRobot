import json
from modules.map_module import Map_tile
from modules.helpers import debug_print

class Map_saver():
    def __init__(self, mapObj):
        self.map = mapObj

    def save_map(self):
        debug_print("saved")
        with open("map.json", "w") as f:
            json.dump(self.map.map, f, default=lambda obj: obj.value)                

    def load_map(self):
        debug_print("loaded")
        debug_print(self.map)
        with open("map.json", "r+") as f:
            self.map.map = [[Map_tile(item) for item in col]for col in json.load(f)]