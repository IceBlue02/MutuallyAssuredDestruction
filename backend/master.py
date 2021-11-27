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

class game():
    def __init__(self):
        self.bombs = [None]

    def initalBomb(self,number):
        square = bomb("Square", [
            [1,1,1,1,0],
            [1,1,1,1,0],
            [1,1,1,1,0],
            [1,1,1,1,0],
            [1,1,1,1,0],
        ])
        self.bombs.append(square)

        circle = bomb("Circle",[
            [0,1,1,1,0],
            [1,1,1,1,1],
            [1,1,1,1,1],
            [1,1,1,1,1],
            [0,1,1,1,0],
        ]
        )
        self.bombs.append(circle)

        diamond = bomb("Bomb", [
            [0,1,1,1,0,],
            [1,1,1,1,1,],
            [1,1,1,1,1,],
            [1,1,1,1,1,],
            [0,1,1,1,0,],
        ])

        self.bombs.append(diamond)

        target= bomb("Target", [
            [1,1,1,1,1],
            [1,0,0,0,1],
            [1,0,1,0,1],
            [1,0,0,0,1],
            [1,1,1,1,1], 
        ])
        self.bombs.append(target)

        www_dot_bomb = bomb("wwwDotBomb ", [
            [1,0,1,0,1],
            [0,1,0,1,0],
            [1,0,1,0,1],
            [0,1,0,1,0],
            [1,0,1,0,1], 
        ])
        self.bombs.append(www_dot_bomb)

        one = bomb("One", [ 
            [1,0,0,0,1],
            [0,1,0,1,0],
            [0,0,1,0,0],
            [0,1,0,1,0],
            [1,0,0,0,1], 
        ])
        self.bombs.append(1)

        H0 = bomb("H0", [ 
            [1,0,0,0,1],
            [1,0,0,0,1],
            [1,1,1,1,1],
            [1,0,0,0,1],
            [1,0,0,0,1],         
        ])
        self.bombs.append(H0)

        PO = bomb("P0", [ 
            [1,1,1,1,0],
            [1,1,1,1,0],
            [1,1,1,1,0],
            [1,0,0,0,0],
            [1,0,0,0,0],
        ])
        self.bombs.append(P0)

        cherry = bomb("Cherry", [ 
            [0,0,1,0,0],
            [0,0,1,0,0],
            [0,0,1,0,0],
            [1,1,0,1,1],
            [1,1,0,1,1],
        ])
        self.bombs.append(cherry)

        e = bomb("e", [ 
            [1,1,1,1,1],
            [1,0,0,0,1],
            [1,1,1,1,1],
            [1,0,0,0,0],
            [1,1,1,1,1], 
        ])
        self.bombs.append(e)

        A0 = bomb("A0", [ 
            [0,0,1,0,0],
            [0,1,0,1,0],
            [0,1,1,1,0],
            [1,0,0,0,1], 
            [1,0,0,0,1],           
        ])
        self.bombs.append(A0)

        England = bomb("ENGLAND", [ 
            [0,0,1,0,0],
            [0,0,1,0,0],
            [1,1,1,1,1],
            [0,0,1,0,0],
            [0,0,1,0,0], 
        ])
        self.bombs.append(England)
    


