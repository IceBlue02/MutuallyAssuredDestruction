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


def placeFactories(turn, data):
    for i in range (0,3):
        x = data["factories"][i][0]
        y = data["factories"][i][1]
        if(board[x][y].state != turn):
            return False
        else:
            board[x][y].building = 1

def placeSilo(turn, data):
    for i in range (0,3):
        x = data["silo"][i][0]
        y = data["silo"][i][1]
        if(board[x][y].state != turn):
            return False
        else:
            board[x][y].building = 2   

def get_hand_options(factories):
    hand_options = [None]
    for i in range(0, factories):
        hand_options.append(get_card())
    return hand_options

#1 = red
# -1 = blue
player = 1
red_hand_size = board.get_silo_red()
blue_hand_size = board.get_silo_blue()
red_hand = []
blue_hand = []
gameOver = -1
set = 0 
#set factories
while set == 0:
    if player == 1:
        placeFactories(player, data)
        placeSilo(player, data)
        player = player* (-1)
    if player == -1:
        placeFactories(player, data)
        placeSilo(player, data)
        player = player* (-1)
        set = 1

while gameOver == -1:
    get_board(player)
    get_hand_options(get_factory(player))
    if player ==1:
        red_hand.append(data["chosen"][0])
    if player ==-1:
        blue_hand.append(data["chosen"][0])

    selected_card = data['selected'][0]
    if player ==1:
        selected_card = red_hand.pop(selected_card)
    if player ==-1:
        selected_card = blue_hand.pop(selected_card)
    #need to implement placing of bomb 

    get_board(player)
    player = player*(-1)

#need to write a function to get card.














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