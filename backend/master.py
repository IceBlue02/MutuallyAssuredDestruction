from enum import IntEnum

class state(IntEmun):
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