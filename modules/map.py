import numpy as np

class Map():
    """
    Provides functions for reading and modifying the enviroment.
    """

    def __init__(self, size):
        self.__map = np.zeros((size, size))