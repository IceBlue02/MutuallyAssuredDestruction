from enum import IntEnum
import random
from re import match
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
        # 0 = no building
        # 1 = factory
        # 2 = silo

    def set_state(self, state):
        self.state = state
        # 0 = destoryed
        # 1 = red
        # -1 = blue

    def __int__(self):
        return self.state * (self.building + 1)
        # 0 = destroyed
        # 1/-1 = red/blue normal
        # 2/-2 = red/blue factory
        # 3/-3 = red/blue silo

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

    def get_int_board(self, player):
        board = [[None for x in range(30)] for x in range(15)]
        for i in range (0, len(self.board)):
            for j in range(0, len(self.board[i])):
                if player == 1:
                    if self.board[i][j].get_state() >= 0:
                        board[i][j] = int(self.board[i][j])
                    else:
                        board[i][j] = int(Tile(-1, 0))
                if player == -1:
                    if self.board[i][j].get_state() <= 0:
                        board[i][j] = int(self.board[i][j])
                    else:
                        board[i][j] = int(Tile(1, 0))
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
                        self.board[x_pos][y_pos].set_state(0)

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
        self.bombs = []
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
            [0,0,1,0,0],
            [0,1,1,1,0],
            [1,1,1,1,1],
            [0,1,1,1,0],
            [0,0,1,0,0],
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
    STARTING_HAND_SIZE = 5
    def __init__(self):
        self.deck = [None]
        self.deck_builder()
        self.player = 1



        self.game_board = Board()
        self.red_hand_size = self.game_board.get_silo(1)
        self.blue_hand_size = self.game_board.get_silo(-1)
        self.red_hand = self.initialise_hand()
        self.blue_hand = self.initialise_hand()

        self.setup = 0
        self.win = 1
        self.board_width = 30
        self.board_height = 15
        self.number_of_factories = 5
        self.number_of_silos = 5
        
        self.cards = Cards()

        self.playersingame = 0
        self.startingboardset = [False, False]
        self.turn_change_event = threading.Event()
        self.game_start_event = threading.Event()


    def initialise_hand(self):
        hand = []
        for _ in range(1, Game.STARTING_HAND_SIZE):
            hand.append(self.get_card())
        return hand

    def get_cards(self):
        data = []
        for c in self.cards.bombs:
            if not c:
                continue
            carddata = {}
            carddata["id"] = c.id
            carddata["name"] = c.name
            carddata["rarity"] = c.rarity
            carddata["shape"] = c.shape
            data.append(carddata)

        return data

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

    def place_starting_board(self, player, factories, silos):
        valid = self.place_factories(player, factories) or self.place_silos(player, silos)
        if not valid:
            return {"valid": False}

        self.startingboardset[0] == True if player == 1 else self.startingboardset[1] == True

        if self.startingboardset[0] and self.startingboardset[1]:
            self.start_game()
            return {"valid": True, "ready": True}
        else:
            return {"valid": True, "ready": False}

    def start_game(self):
        self.turn_change_event.set()
        self.turn_change_event.clear()


    def place_factories(self, player, coords):
        if len(coords) != self.number_of_factories:
            return False
            
        for i in range (0, len(coords)-1):
            x = coords[i][0]
            y = coords[i][1]
            if(self.game_board.board[x][y].state != player):
                return False
            else:
                self.game_board.board[x][y].building = 1

        return True

    def place_silos(self, player, coords):
        if len(coords) != self.number_of_silos:
            return False

        for i in range (0, len(coords)-1):
            x = coords[i][0]
            y = coords[i][1]
            if(self.game_board.board[x][y].state != player):
                return False
            else:
                self.game_board.board[x][y].building = 2  

        return True

    def get_hand_options(self, factories):
        hand_options = []
        for i in range(0, factories):
            card = self.get_card()
            hand_options.append(card.id)
        return hand_options

    def get_arsenal():
        card_holder = Cards()
        card_holder.initaliseBombs()
        arsenal = []
        for i in range(0,len(card_holder)):
            for _ in range(0,card_holder[i].rarity):
                bomb = card_holder[i]
                arsenal.append(bomb.id)
        return arsenal

    def get_card(self):
        return random.choice(self.deck)

    def get_hand_size(self):
        return self.game_board.get_silo(self.player)
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

    def get_game_state(self, player):
        if player == -1:
            hand_id = []
            for i in range(0,len(self.blue_hand)-1):
                bomb = self.blue_hand[i]
                hand_id.append(bomb.id)
        elif self.player == 1:
            hand_id = []
            for i in range(0,len(self.red_hand)-1):
                bomb = self.red_hand[i]
                hand_id.append(bomb.id)
        else:
            print("Error")

        x = 0
        int_board = [[self.game_board.get_int_board(player)[y][x] for y in range(15)] for x in range(30)]
        return {"hand": hand_id, "board": int_board}

    def deck_builder(self):
        card_holder = Cards()
        card_holder.initaliseBombs()
        for i in range(0,len(card_holder.bombs)):
            for _ in range(0,card_holder.bombs[i].rarity):
                self.deck.append(card_holder.bombs[i])
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

    def get_number_of_factories(self):
        return self.number_of_factories

    def get_number_of_silos(self):
        return self.number_of_silos

    def remove_card(self, bomb_id, number):
        if self.player == 1:
            while number > 0:
                i = 0
                if self.red_hand[i].id == bomb_id:
                    self.red_hand.pop(i)
                    number += -1
                    continue
                i += 1
        if self.player == -1:
            while number > 0:
                i = 0
                if self.blue_hand[i].id == bomb_id:
                    self.blue_hand.pop(i)
                    number += -1
                    continue
                i += 1

    def deploy_bomb(self, player, coord, bomb_id):
        if player == self.player:
            if self.player == -1:
                for i in range(0, len(self.blue_hand)):
                    if self.blue_hand[i].id == bomb_id:
                        bomb = self.cards.bombs[bomb_id-1]
                        self.game_board.apply_bomb(bomb.shape, int(coord[0]), int(coord[1]))
                        Game.remove_card(bomb_id, 1)
                        self.swap_turns()
                        return True
     
                return False

            if self.player == 1:
                for i in range(0, len(self.red_hand)):
                    if self.red_hand[i].id == bomb_id:
                        bomb = self.cards.bombs[bomb_id-1]
                        duplicate_bombs = 0
                        for i in range(0, len(self.red_hand)):
                            if self.red_hand[i].id == bomb_id:
                                bomb = self.cards.bombs[bomb_id-1]
                                self.game_board.apply_bomb(bomb.shape, int(coord[0]), int(coord[1]))
                                Game.remove_card(bomb_id, 1)
                                self.swap_turns()
                                return True
                return False
            return False


    def swap_turns(self):
        self.player = self.player * -1
        self.turn_change_event.set()
        print("Turn change")
        self.turn_change_event.clear()

    def await_turn_change(self):
        print("Waiting for turn change")
        self.turn_change_event.wait()
        print("Got turn change")

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

    def trigger_turn_change(self):
        self.swap_turns()

#need to write a function to get card.

if __name__ == "__main__":
    g = Game()
