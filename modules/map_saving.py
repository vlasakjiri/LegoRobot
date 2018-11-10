from ev3dev.ev3 import Button
import threading 
from time import sleep
import json
from modules.map_module import Map_tile

class Map_saver():
    def __init__(self, map):
        self.button = Button()
        self.thread = threading.Thread(target=self.save_on_interval)
        self.thread.setDaemon(True)
        self.button.on_up += self.load_map
        self.button.on_down += self.thread.start
        self.lock = threading.Lock()
        self.interval = 3
        self.map = map
        self.thread.start()
        

    def save_on_interval(self):
        while True:
            sleep(self.interval)
            self.save_map()

    def save_map(self):
        self.lock.acquire()
        with open("map.json", "w") as f:
            json.dump(self.map.map, f, default=lambda obj: obj.value)                
        self.lock.release()

    def load_map(self):
        self.lock.acquire()
        with open("map.json", "r+") as f:
            self.map.map = [[Map_tile(item) for item in col]for col in json.load(f)]


        print(self.map)
        self.lock.release()