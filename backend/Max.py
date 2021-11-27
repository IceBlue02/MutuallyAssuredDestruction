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
    def __init__(self, name, rarity, description, shape):
        self.name = name 
        self.rarity = rarity
        self.description = description
        self.shape = shape


class cards):
    def __init__(self):
        self.bombs = [None]


    def rarity(occurance):
        if occurance == "super rare":
            return 1
        if occurance == "rare":
            return 2
        if occurance == "uncommon":
            return 4
        if occurance == "average":
            return 8
        if occurance == "common":
            return 16
        else:
            return 0

    def initaliseBombs(self):
        square = bomb("Square",rarity("average"), "Simple, but effective.", [
            [1,1,1,1,0],
            [1,1,1,1,0],
            [1,1,1,1,0],
            [1,1,1,1,0],
            [1,1,1,1,0],
        ])
        self.bombs.append(square)

        circle = bomb("Circle", rarity("rare"), "The circle of (no) life.", [
            [0,1,1,1,0],
            [1,1,1,1,1],
            [1,1,1,1,1],
            [1,1,1,1,1],
            [0,1,1,1,0],
        ]
        )
        self.bombs.append(circle)

        diamond = bomb("Bomb",rarity("common"), "Diamonds are forever. So is the damage left by this."[
            [0,1,1,1,0,],
            [1,1,1,1,1,],
            [1,1,1,1,1,],
            [1,1,1,1,1,],
            [0,1,1,1,0,],
        ])

        self.bombs.append(diamond)

        target= bomb("Target",rarity("rare"), "You can't miss.",[
            [1,1,1,1,1],
            [1,0,0,0,1],
            [1,0,1,0,1],
            [1,0,0,0,1],
            [1,1,1,1,1], 
        ])
        self.bombs.append(target)


        www_dot_bomb = bomb("wwwDotBomb ", rarity("common"),"...................", [
            [1,0,1,0,1],
            [0,1,0,1,0],
            [1,0,1,0,1],
            [0,1,0,1,0],
            [1,0,1,0,1], 
        ])
        self.bombs.append(www_dot_bomb)

        X = bomb("X", rarity(""),"It marks the spot. And hits it.", [ 
            [1,0,0,0,1],
            [0,1,0,1,0],
            [0,0,1,0,0],
            [0,1,0,1,0],
            [1,0,0,0,1],
        ])
        self.bombs.append(X)

        H0 = bomb("H0",rarity("common"), "Can you add the H0,Bomb to the game?' 'Yeah sure I got you'", [ 
            [1,0,0,0,1],
            [1,0,0,0,1],
            [1,1,1,1,1],
            [1,0,0,0,1],
            [1,0,0,0,1],         
        ])
        self.bombs.append(H0)

        PO = bomb("P0", rarity("average"),"Not sure why you'd make a bomb like this, but there you go.", [ 
            [1,1,1,1,0],
            [1,1,1,1,0],
            [1,1,1,1,0],
            [1,0,0,0,0],
            [1,0,0,0,0],
        ])
        self.bombs.append(P0)

        cherry = bomb("Cherry", rarity("super rare"), "Yep, it's a pair of Cherries. ", [ 
            [0,0,1,0,0],
            [0,0,1,0,0],
            [0,0,1,0,0],
            [1,1,0,1,1],
            [1,1,0,1,1],
        ])
        self.bombs.append(cherry)

        e = bomb("e", rarity("rare"), "2.71828182845904523536028747135", [ 
            [1,1,1,1,1],
            [1,0,0,0,1],
            [1,1,1,1,1],
            [1,0,0,0,0],
            [1,1,1,1,1], 
        ])
        self.bombs.append(e)

        A0 = bomb("A0",rarity("common"), "I know I'll be A0,O, A0,O0,K." [ 
            [0,0,1,0,0],
            [0,1,0,1,0],
            [0,1,1,1,0],
            [1,0,0,0,1], 
            [1,0,0,0,1],           
        ])
        self.bombs.append(A0)

        England = bomb("ENGLAND",rarity("common"), "RULE BRITANNIA, BRITANNIA RULES THE WAVES", [ 
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

def cards():
    cards = cards()
    cards.initaliseBombs()
    

cards =[None]
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