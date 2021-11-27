from enum import IntEnum

class state(IntEnum):
    blue = -1
    grey = 0
    red = 1

class building(IntEnum):
    empty = 0
    factory = 1
    silo = 2

class bomb(IntEnum):
    H_Bomb = 0
    A_Bomb = 1
    Tsar_Bomb = 2
    Proton_Bomb = 3

class Tile:
    def __init__(self, state, building):
        self.state = state
        self.building = building

    def get_building(self):
        return building

    def get_state(self):
        return state

    def set_building(self, building):
        self.building = building

    def set_state(self, state):
        self.state = state