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
    H-Bomb = 0
    A-Bomb = 1
    Tsar-Bomb = 2
    Proton-Bomb = 3

class Tile:
    def __init__(self, state, building):
        self.state = state
        self.building = building

    def get_building():
        return building

    def get_state():
        return state

    def set_building(building):
        self.building = building

    def set_state(state):
        self.state = state