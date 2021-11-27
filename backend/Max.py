from enum import IntEnum

class state(IntEnum):
    blue = -1
    grey = 0
    red = 1

class building(IntEnum):
    empty = 0
    factory = 1
    silo = 2

class bomb():
    def __init__(self, name, shape):
        self.name = name 
        self.shape = shape


class game(self):
    self.bombs = [None]

    def initalBomb(number):
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
    


class AttackCards:
    def __init__(self,bomb):
        self.bomb_type = bomb
    
    def attacked(x, y):
        board[x][y].state = 0

    def bombsha(self,x,y):
        if self.bomb_type == 0:
            attacked(x, y)
            #left side
            attacked((x+1), y)
            attacked((x+2), y)
            attacked((x+2), (y+1))
            attacked((x+2), (y+2))
            attacked((x+2), (y-1))
            attacked((x+2), (y-2))

            #right side 
            attacked((x-1), y)
            attacked((x-2), y)
            attacked((x-2), (y+1))
            attacked((x-2), (y+2))
            attacked((x-2), (y-1))
            attacked((x-2), (y-2))
        
        if self.bomb_type == 4