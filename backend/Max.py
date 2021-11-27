from enum import Enum
import enum

class state(Emun):
    blue = -1
    grey = 0
    red = 1

class building(Enum):
    empty = 0
    factory = 1
    silo = 2