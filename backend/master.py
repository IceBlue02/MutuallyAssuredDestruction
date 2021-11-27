from enum import IntEnum
import random


class Tile:
    def __init__(self, state, building):
        self.state = state
        self.building = building

    def get_building(self):
        return self.building
    
    def get_state(self):
        return self.state

    def set_building(self, building):
        self.building = building

    def set_state(self, state):
        self.state = state

class Board:
    def __init__(self):
        self.board = [15][30]
        self.board.fill_board()

    def fill_board(self):
        for i in range(0, len(self.board)):
            for j in range(0, len(self.board[i])):
                if j < 15:
                    self.board[i][j] = Tile(1, 0)
                else:
                    self.board[i][j] = Tile(-1, 0)

    def get_board(self, player):
        board = [15][30]
        for i in range (0, len(self.board)):
            for j in range(0, len(self.board[i])):
                if player == 1:
                    if self.board[i][j].get_state() >= 0:
                        board[i][j] = self.board[i][j]
                    else:
                        board[i][j] = Tile(-1, 0)
                if player == -1:
                    if self.board[i][j].get_state() <= 0:
                        board[i][j] = self.board[i][j]
                    else:
                        board[i][j] = Tile(1, 0)
        return board

    def get_factory(self, player):
        factories = 0
        for i in range (0, len(self.board)):
            for j in range(0, len(self.board[i])):
                if player == 1:
                    if self.board[i][j].get_building() == 1 & self.board[i][j].get_state() == 1:
                        factories  += 1
                if player == -1:
                    if self.board[i][j].get_building() == 1 & self.board[i][j].get_state() == -1:
                        factories  += 1
        return factories

    def get_silo(self, player):
        silo = 0
        for i in range (0, len(self.board)):
            for j in range(0, len(self.board[i])):
                if player == 1:
                    if self.board[i][j].get_building() == 2 & self.board[i][j].get_state() == 1:
                        silo  += 1
                if player == -1:
                    if self.board[i][j].get_building() == 2 & self.board[i][j].get_state() == -1:
                        silo  += 1
        return silo

    def apply_bomb(self, bomb_template, x, y):
        for i in range(0, len(bomb_template)):
            for j in range(0, len(bomb_template[i])):
                if bomb_template[i][j] == 1:
                    self.board[x + (i - 2)][y + (j - 2)].setState(0)

class State(IntEnum):
    blue = -1
    grey = 0
    red = 1

class Building(IntEnum):
    empty = 0
    factory = 1
    silo = 2

class Bomb():
    def __init__(self, id, name, rarity, description, shape):
        self.name = name 
        self.id = id
        self.rarity = rarity
        self.description = description
        self.shape = shape

class Cards():
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
        square = Bomb(1,"Square", self.rarity("average"), "Simple, but effective.", [
            [1,1,1,1,0],
            [1,1,1,1,0],
            [1,1,1,1,0],
            [1,1,1,1,0],
            [0,0,0,0,0],
        ])
        self.bombs.append(square)

        circle = Bomb(2,"Circle", self.rarity("rare"), "The circle of (no) life.", [
            [0,1,1,1,0],
            [1,1,1,1,1],
            [1,1,1,1,1],
            [1,1,1,1,1],
            [0,1,1,1,0],
        ]
        )
        self.bombs.append(circle)

        diamond = Bomb(3,"Bomb",self.rarity("common"), "Diamonds are forever. So is the damage left by this."[
            [0,1,1,1,0,],
            [1,1,1,1,1,],
            [1,1,1,1,1,],
            [1,1,1,1,1,],
            [0,1,1,1,0,],
        ])

        self.bombs.append(diamond)

        target= Bomb(4,"Target",self.rarity("rare"), "You can't miss.",[
            [1,1,1,1,1],
            [1,0,0,0,1],
            [1,0,1,0,1],
            [1,0,0,0,1],
            [1,1,1,1,1], 
        ])
        self.bombs.append(target)

        www_dot_bomb = Bomb(5,"wwwDotBomb ", self.rarity("common"),"...................", [
            [1,0,1,0,1],
            [0,1,0,1,0],
            [1,0,1,0,1],
            [0,1,0,1,0],
            [1,0,1,0,1], 
        ])
        self.bombs.append(www_dot_bomb)

        X = Bomb(6,"X", self.rarity("common"),"It marks the spot. And hits it.", [ 
            [1,0,0,0,1],
            [0,1,0,1,0],
            [0,0,1,0,0],
            [0,1,0,1,0],
            [1,0,0,0,1],
        ])
        self.bombs.append(X)

        H0 = Bomb(7,"H0",self.rarity("common"), "Can you add the H0,Bomb to the game?' 'Yeah sure I got you'", [ 
            [1,0,0,0,1],
            [1,0,0,0,1],
            [1,1,1,1,1],
            [1,0,0,0,1],
            [1,0,0,0,1],         
        ])
        self.bombs.append(H0)

        PO = Bomb(8,"P0", self.rarity("average"),"Not sure why you'd make a bomb like this, but there you go.", [ 
            [1,1,1,1,0],
            [1,1,1,1,0],
            [1,1,1,1,0],
            [1,0,0,0,0],
            [1,0,0,0,0],
        ])
        self.bombs.append(P0)

        cherry = Bomb(9,"Cherry", self.rarity("super rare"), "Yep, it's a pair of Cherries. ", [ 
            [0,0,1,0,0],
            [0,0,1,0,0],
            [0,0,1,0,0],
            [1,1,0,1,1],
            [1,1,0,1,1],
        ])
        self.bombs.append(cherry)

        e = Bomb(10,"e", self.rarity("rare"), "2.71828182845904523536028747135", [ 
            [1,1,1,1,1],
            [1,0,0,0,1],
            [1,1,1,1,1],
            [1,0,0,0,0],
            [1,1,1,1,1], 
        ])
        self.bombs.append(e)

        A0 = Bomb(11,"A0",self.rarity("common"), "I know I'll be A0,O, A0,O0,K." [ 
            [0,0,1,0,0],
            [0,1,0,1,0],
            [0,1,1,1,0],
            [1,0,0,0,1], 
            [1,0,0,0,1],           
        ])
        self.bombs.append(A0)

        England = Bomb(12, "ENGLAND",self.rarity("common"), "RULE BRITANNIA, BRITANNIA RULES THE WAVES", [ 
            [0,0,1,0,0],
            [0,0,1,0,0],
            [1,1,1,1,1],
            [0,0,1,0,0],
            [0,0,1,0,0], 
        ])
        self.bombs.append(England)

class Game():
    def __init__(self):
        self.deck = [None]
        self.player = 1
        self.red_hand =[]
        self.blue_hand = []
        self.red_hand_size = Board.get_silo(1)
        self.blue_hand_size = Board.get_silo(-1)
        self.setup = 0
        self.game_state = 1
        self.board_width = 30
        self.board_height = 15

    def placeFactories(turn, data):
        for i in range (0,3):
            x = data["factories"][i][0]
            y = data["factories"][i][1]
            if(Board[x][y].state != turn):
                return False
            else:
                Board[x][y].building = 1


    def placeSilo(turn, data):
        for i in range (0,3):
            x = data["silo"][i][0]
            y = data["silo"][i][1]
            if(Board[x][y].state != turn):
                return False
            else:
                Board[x][y].building = 2   


    def get_hand_options(self, factories):
        hand_options = [None]
        for i in range(0, factories):
            hand_options.append(self.get_card())
        return hand_options


    def get_card(self):
        return random.choice(self.deck)
        

    def gameOver(self):
        board = Board()
        board = board.get_Board(self.player)
        red_tiles = 0
        blue_tiles = 0
        for i in range(0, self.board_height):
            for j in range(0, self.board_width):
                if board[i][j].get_state() == -1:
                    blue_tiles += 1
                if board[i][j].get_state() == 1:
                    red_tiles += 1
        if red_tiles == 0:
            self.game_state = 0
        if blue_tiles ==0:
            self.game_state = 0


    def deck_builder(self,deck):
        card_holder = Cards()
        card_holder.initaliseBombs()
        for i in range(0,card_holder.length()):
            for _ in range(0,card_holder[i].rarity):
                deck.append(card_holder[i])
   
    def main(self):
        deck = [None]
        Game.deck_builder(self.deck)
        #1 = red
        # -1 = blue
        #set factories
        while self.setup == 0:
            if self.player == 1:
                Game.placeFactories(self.player, data)
                Game.placeSilo(self.player, data)
                self.player = self.player* (-1)
            if self.player == -1:
                Game.placeFactories(self.player, data)
                Game.placeSilo(self.player, data)
                self.player = self.player* (-1)
                self.setup = 1
        #start the game 
        while self.game_state == 1:
            Board.get_board(player)
            Board.get_hand_options(Board.get_factory(player))
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
            self.gameOver()
            Board.get_board(player)
            player = player*(-1)

#need to write a function to get card.