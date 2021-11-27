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
    def __init__(self, id, name, rarity, description, shape):
        self.name = name 
        self.id = id
        self.rarity = rarity
        self.description = description
        self.shape = shape


class cards():
    def __init__(self):
        self.bombs = [None]

    def rarity(self, occurance):
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
        square = bomb(1,"Square", self.rarity("average"), "Simple, but effective.", [
            [1,1,1,1,0],
            [1,1,1,1,0],
            [1,1,1,1,0],
            [1,1,1,1,0],
            [1,1,1,1,0],
        ])
        self.bombs.append(square)

        circle = bomb(2,"Circle", self.rarity("rare"), "The circle of (no) life.", [
            [0,1,1,1,0],
            [1,1,1,1,1],
            [1,1,1,1,1],
            [1,1,1,1,1],
            [0,1,1,1,0],
        ]
        )
        self.bombs.append(circle)

        diamond = bomb(3,"Bomb",self.rarity("common"), "Diamonds are forever. So is the damage left by this."[
            [0,1,1,1,0,],
            [1,1,1,1,1,],
            [1,1,1,1,1,],
            [1,1,1,1,1,],
            [0,1,1,1,0,],
        ])

        self.bombs.append(diamond)

        target= bomb(4,"Target",self.rarity("rare"), "You can't miss.",[
            [1,1,1,1,1],
            [1,0,0,0,1],
            [1,0,1,0,1],
            [1,0,0,0,1],
            [1,1,1,1,1], 
        ])
        self.bombs.append(target)

        www_dot_bomb = bomb(5,"wwwDotBomb ", self.rarity("common"),"...................", [
            [1,0,1,0,1],
            [0,1,0,1,0],
            [1,0,1,0,1],
            [0,1,0,1,0],
            [1,0,1,0,1], 
        ])
        self.bombs.append(www_dot_bomb)

        X = bomb(6,"X", self.rarity("common"),"It marks the spot. And hits it.", [ 
            [1,0,0,0,1],
            [0,1,0,1,0],
            [0,0,1,0,0],
            [0,1,0,1,0],
            [1,0,0,0,1],
        ])
        self.bombs.append(X)

        H0 = bomb(7,"H0",self.rarity("common"), "Can you add the H0,Bomb to the game?' 'Yeah sure I got you'", [ 
            [1,0,0,0,1],
            [1,0,0,0,1],
            [1,1,1,1,1],
            [1,0,0,0,1],
            [1,0,0,0,1],         
        ])
        self.bombs.append(H0)

        PO = bomb(8,"P0", self.rarity("average"),"Not sure why you'd make a bomb like this, but there you go.", [ 
            [1,1,1,1,0],
            [1,1,1,1,0],
            [1,1,1,1,0],
            [1,0,0,0,0],
            [1,0,0,0,0],
        ])
        self.bombs.append(P0)

        cherry = bomb(9,"Cherry", self.rarity("super rare"), "Yep, it's a pair of Cherries. ", [ 
            [0,0,1,0,0],
            [0,0,1,0,0],
            [0,0,1,0,0],
            [1,1,0,1,1],
            [1,1,0,1,1],
        ])
        self.bombs.append(cherry)

        e = bomb(10,"e", self.rarity("rare"), "2.71828182845904523536028747135", [ 
            [1,1,1,1,1],
            [1,0,0,0,1],
            [1,1,1,1,1],
            [1,0,0,0,0],
            [1,1,1,1,1], 
        ])
        self.bombs.append(e)

        A0 = bomb(11,"A0",self.rarity("common"), "I know I'll be A0,O, A0,O0,K." [ 
            [0,0,1,0,0],
            [0,1,0,1,0],
            [0,1,1,1,0],
            [1,0,0,0,1], 
            [1,0,0,0,1],           
        ])
        self.bombs.append(A0)

        England = bomb(12, "ENGLAND",self.rarity("common"), "RULE BRITANNIA, BRITANNIA RULES THE WAVES", [ 
            [0,0,1,0,0],
            [0,0,1,0,0],
            [1,1,1,1,1],
            [0,0,1,0,0],
            [0,0,1,0,0], 
        ])
        self.bombs.append(England)


class game():
    def __init__(self):
        self.deck = [None]
        self.player = 1
        self.red_hand =[]
        self.blue_hand = []
        self.red_hand_size = board.get_silo_red()
        self.blue_hand_size = board.get_silo_blue()
        self.setup = 0
        self.game_state = 1

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


    def get_card():
        return random.choice(deck)


    def deck_builder(self,deck):
        card_holder = cards()
        card_holder.initaliseBombs()
        for i in range(0,card_holder.length()):
            for _ in range(0,card_holder[i].rarity):
                deck.apped(card_holder[i])
   
    def main(self):
        deck = [None]
        game.deck_builder(self.deck)
        #1 = red
        # -1 = blue
        #set factories
        while self.setup == 0:
            if self.player == 1:
                game.placeFactories(self.player, data)
                game.placeSilo(self.player, data)
                self.player = self.player* (-1)
            if self.player == -1:
                game.placeFactories(self.player, data)
                game.placeSilo(self.player, data)
                self.player = self.player* (-1)
                self.setup = 1

        while self.game_state == 1:
            board.get_board(player)
            board.get_hand_options(get_factory(player))
            if player ==1:
                self.red_hand.append(data["chosen"][0])
            if player ==-1:
                self.blue_hand.append(data["chosen"][0])

            selected_card = data['selected'][0]
            if player ==1:
                selected_card = self.red_hand.pop(selected_card)
            if player ==-1:
                selected_card = self.blue_hand.pop(selected_card)
            #need to implement placing of bomb 

            board.get_board(player)
            player = player*(-1)

#need to write a function to get card.