from enum import IntEnum
import random
import threading


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
        self.board = [[None for x in range(30)] for x in range(15)]
        self.fill_board()

    def fill_board(self):
        for i in range(0, len(self.board)):
            for j in range(0, len(self.board[i])):
                if j < 15:
                    self.board[i][j] = Tile(1, 0)
                else:
                    self.board[i][j] = Tile(-1, 0)

    def get_board(self, player):
        board = [[None for x in range(30)] for x in range(15)]
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
                    x_pos = x + (j - 2)
                    y_pos = y + (i - 2)
                    if x_pos < 0 | y_pos < 0 | x_pos > 14| y_pos > 29:
                        continue
                    else:
                        self.board[x_pos][y_pos].setState(0)

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
        self.initaliseBombs()

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

        diamond = Bomb(3,"Bomb",self.rarity("common"), "Diamonds are forever. So is the damage left by this.", [
            [0,1,1,1,0],
            [1,1,1,1,1],
            [1,1,1,1,1],
            [1,1,1,1,1],
            [0,1,1,1,0],
        ])

        self.bombs.append(diamond)

        target= Bomb(4,"Target",self.rarity("rare"), "You can't miss.", [
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
        self.bombs.append(PO)

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

        A0 = Bomb(11,"A0",self.rarity("common"), "I know I'll be A0,O, A0,O0,K.", [ 
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
        self.red_hand = Game.initialise_hand
        self.blue_hand = Game.initialise_hand
        self.game_board = Board()
        self.red_hand_size = self.game_board.get_silo(1)
        self.blue_hand_size = self.game_board.get_silo(-1)
        self.setup = 0
        self.win = 1
        self.board_width = 30
        self.board_height = 15
        
        self.cards = Cards()
        
        self.playersingame = 0
        self.turn_change_event = threading.Event()
        self.game_start_event = threading.Event()


#start of game
    def initialise_hand(self):
        hand = [None]
        for _ in range(0, self.game_board.get_factories(1)):
            hand.append(self.get_card())
        return hand

    def on_game_entry(self):
        self.playersingame += 1
        if self.playersingame == 1:
            return {"player": 1, "ready": False}
        else:
            self.game_start_event.set()
            self.game_start_event.clear()
            return {"player": -1, "ready": True}

    def await_game_start(self):
        print("Waiting for game start")
        self.game_start_event.wait()
        return {"ready": True}

    def deck_builder(self,deck):
        card_holder = Cards()
        card_holder.initaliseBombs()
        for i in range(0,len(card_holder)):
            for _ in range(0,card_holder[i].rarity):
                self.deck.append(card_holder[i])

    def place_factories(self,turn, data):
        for i in range (0,3):
            x = data["factories"][i][0]
            y = data["factories"][i][1]
            if(self.game_board[x][y].state != turn):
                return False
            else:
                self.game_board[x][y].building = 1

    def place_silo(self,turn, data):
        for i in range (0,3):
            x = data["silo"][i][0]
            y = data["silo"][i][1]
            if(self.game_board[x][y].state != turn):
                return False
            else:
                self.game_board[x][y].building = 2  

#getters
    def get_cards(self):
        data = []
        for c in self.cards.bombs:
            if not c:
                continue
            print(c.id)
            carddata = {}
            carddata["id"] = c.id
            carddata["name"] = c.name
            carddata["rarity"] = c.rarity
            carddata["shape"] = c.shape
            data.append(carddata)

        return data

    def get_game_state(self):
        if self.player == -1:
            hand_id = [None]
            for i in range(0,len(self.blue_hand)):
                bomb = self.blue_hand[i]
                hand_id.append(bomb.id)
           
            return self.game_board.get_board(self.player), hand_id
        if self.player == 1:
            hand_id = [None]
            for i in range(0,len(self.red_hand)):
                bomb = self.red_hand[i]
                hand_id.append(bomb.id)
            
            return self.game_board.get_board(self.player), hand_id
        else: 
            print("Error")

    def get_hand_size(self):
        return self.game_board.get_silo(self.player)

    def get_card(self):
        return random.choice(self.deck)

    def get_arsenal():
        card_holder = Cards()
        card_holder.initaliseBombs()
        arsenal = [None]
        for i in range(0,len(card_holder)):
            for _ in range(0,card_holder[i].rarity):
                bomb = card_holder[i]
                arsenal.append(bomb.id)
        return arsenal

    def get_hand_options(self, factories):
        hand_options = [None]
        for i in range(0, factories):
            card = self.get_card()
            hand_options.append(card.id)
        return hand_options

    def get_hand_options(self, factories):
        hand_options = [None]
        for i in range(0, factories):
            card = self.get_card()
            hand_options.append(card.id)
        return hand_options

    def deploy_bomb(self, bomb_id):
        if self.player == -1:
            for i in range(0, len(self.blue_hand)):
                if self.blue_hand[i].id == bomb_id:
                    return True
            return False
        if self.player == 1:
            for i in range(0, len(self.red_hand)):
                if self.red_hand[i].id == bomb_id:
                    return True
            return False
   
   
    def main(self):
        game_board = Board()
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
            self.game_board.get_board(self.player)
            Game.get_hand_size(self.game_board)
            self.game_board.get_hand_options(self.game_board.get_factory(player))
            if self.player ==1:
                self.red_hand.append(data["chosen"][0])
            if self.player ==-1:
                self.blue_hand.append(data["chosen"][0])

            selected_card = data["selected"][0]
            if self.player ==1:
                selected_card = self.red_hand.pop(selected_card)
            if self.player ==-1:
                selected_card = self.blue_hand.pop(selected_card)
            #need to implement placing of bomb 
            x = data["coordinates"][0]
            y = data["coordinates"][1]
            self.game_board.apply_bomb(self, selected_card.shape, x, y)
            self.gameOver()
            self.game_board.get_board(self.player)
            self.player = self.player*(-1)

    def swap_turns(self):
        self.player = self.player * -1
        self.turn_change_event.set()
        print("Turn change")
        self.turn_change_event.clear()

    def await_turn_change(self):
        print("Waiting for turn change")
        self.turn_change_event.wait()
        return self.player

    def game_over(self):
        red_tiles = 0
        blue_tiles = 0
        for i in range(0, self.board_height):
            for j in range(0, self.board_width):
                if self.game_board[i][j].get_state() == -1:
                    blue_tiles += 1
                if self.game_board[i][j].get_state() == 1:
                    red_tiles += 1
        if red_tiles == 0:
            self.win= 0
        if blue_tiles ==0:
            self.win = 0

#need to write a function to get card.

if __name__ == "__main__":
    g = Game()
    print(g.get_cards())