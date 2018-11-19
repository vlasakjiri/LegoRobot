from ev3dev.ev3 import Button
import threading
from time import sleep
import json
from modules.map_module import Map_tile
from modules.helpers import debug_print


class Map_saver():
    def __init__(self, map):
        self.button = Button()
        self.thread = threading.Thread(target=self.__saver_loop)
        self.thread.setDaemon(True)
        self.lock = threading.Lock()
        self.interval = 3
        self.map = map
        self.thread.start()

    def __wait_for_btn(self):
        while True:
            sleep(0.01)
            if self.button.any() and self.button.down:
                break

    def __saver_loop(self):
        debug_print("started")
        cycles = 0
        cycles_max = self.interval * 100
        self.__wait_for_btn()
        while True:
            sleep(0.01)
            cycles += 1
            if self.button.any():
                if self.button.up:
                    self.load_map()

                elif self.button.down:
                    self.__wait_for_btn()

            if cycles >= cycles_max:
                self.save_map()
                cycles = 0

    def save_map(self):
        self.lock.acquire()
        with open("map.json", "w") as f:
            json.dump(self.map.map, f, default=lambda obj: obj.value)
        debug_print("map saved")
        self.lock.release()

    def load_map(self):
        self.lock.acquire()
        with open("map.json", "r+") as f:
            self.map.map = [[Map_tile(item) for item in col]
                            for col in json.load(f)]
        debug_print("map loaded")
        self.lock.release()
