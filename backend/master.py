from enum import IntEnum
import random
import threading


RARITY_BOMB_LOGIC = True


class Player(IntEnum):
    RED = 1
    BLUE = -1


class State(IntEnum):
    RED = 1
    GREY = 0
    BLUE = -1


class Building(IntEnum):
    EMPTY = 0
    FACTORY = 1
    SILO = 2


class Tile:
    def __init__(self, state, building):
        self.state = state
        self.building = building

    @property
    def serial(self):
        return [self.state, self.building]


def blank_board(width, height):
    return [[None for _ in range(height)] for _ in range(width)]


class Board:
    WIDTH = 30
    HEIGHT = 15

    def __init__(self):
        self.board = blank_board(self.WIDTH, self.HEIGHT)
        self.fill_board()

    @property
    def width(self):
        return len(self.board)

    @property
    def height(self):
        return len(self.board[0])

    def fill_board(self):
        for x in range(self.width):
            for y in range(self.height):
                if x < self.WIDTH // 2:
                    self.board[x][y] = Tile(State.RED, Building.EMPTY)
                else:
                    self.board[x][y] = Tile(Player.BLUE, Building.EMPTY)

    def get_serial_board(self, player):
        board = blank_board(self.WIDTH, self.HEIGHT)
        for x in range(self.width):
            for y in range(self.height):
                if self.board[x][y].state != -player:
                    board[x][y] = self.board[x][y].serial
                else:
                    board[x][y] = Tile(
                        State.BLUE if player == Player.RED else State.RED,
                        Building.EMPTY,
                    ).serial
        return board

    def get_factory_count(self, player):
        factories = 0
        for x in range(self.width):
            for y in range(self.height):
                if (
                    self.board[x][y].building == Building.FACTORY
                    and self.board[x][y].state == player
                ):
                    factories += 1
        return factories

    def get_silo_count(self, player):
        silo = 0
        for x in range(self.width):
            for y in range(self.height):
                if (
                    self.board[x][y].building == Building.SILO
                    and self.board[x][y].state == player
                ):
                    silo += 1
        return silo

    def apply_bomb(self, bomb_template, x, y):
        for dx in range(len(bomb_template)):
            for dy in range(len(bomb_template[dx])):
                if bomb_template[dx][dy] == 1:
                    x_pos = x + (dy - 2)
                    y_pos = y + (dx - 2)
                    if x_pos < 0 or y_pos < 0 or x_pos > 29 or y_pos > 14:
                        continue
                    # if self.board[x_pos][y_pos].building == Building.SILO:
                    # self.lost_silo()
                    # else:
                    self.board[x_pos][y_pos].state = State.GREY

    def get_destroyed_counts(self):
        counts = [0, 0]
        for y, col in enumerate(self.board):
            for elem in col:
                if elem.state == 0:
                    if y >= 15:
                        counts[1] += 1
                    else:
                        counts[0] += 1

        return counts


class Bomb:
    def __init__(self, id, name, rarity, description, shape):
        self.name = name
        self.id = id
        self.rarity = rarity
        self.description = description
        self.shape = shape


RARITY_SUPER_RARE = 5
RARITY_RARE = 4
RARITY_AVERAGE = 3
RARITY_COMMON = 2
RARITY_YES = 1


class Cards:
    def __init__(self):
        self.bombs = []
        self.init_bombs()

    def init_bombs(self):
        self.bombs.append(
            Bomb(
                1,
                "Square",
                RARITY_AVERAGE,
                "Simple, but effective.",
                [
                    [1, 1, 1, 1, 0],
                    [1, 1, 1, 1, 0],
                    [1, 1, 1, 1, 0],
                    [1, 1, 1, 1, 0],
                    [0, 0, 0, 0, 0],
                ],
            )
        )

        self.bombs.append(
            Bomb(
                2,
                "Circle",
                RARITY_RARE,
                "The circle of (no) life.",
                [
                    [0, 1, 1, 1, 0],
                    [1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1],
                    [0, 1, 1, 1, 0],
                ],
            )
        )

        self.bombs.append(
            Bomb(
                3,
                "Bomb",
                RARITY_COMMON,
                "Diamonds are forever. So is the damage left by this.",
                [
                    [0, 0, 1, 0, 0],
                    [0, 1, 1, 1, 0],
                    [1, 1, 1, 1, 1],
                    [0, 1, 1, 1, 0],
                    [0, 0, 1, 0, 0],
                ],
            )
        )

        self.bombs.append(
            Bomb(
                4,
                "Target",
                RARITY_AVERAGE,
                "You can't miss.",
                [
                    [1, 1, 1, 1, 1],
                    [1, 0, 0, 0, 1],
                    [1, 0, 1, 0, 1],
                    [1, 0, 0, 0, 1],
                    [1, 1, 1, 1, 1],
                ],
            )
        )

        self.bombs.append(
            Bomb(
                5,
                "wwwDotBomb ",
                RARITY_COMMON,
                "...................",
                [
                    [1, 0, 1, 0, 1],
                    [0, 1, 0, 1, 0],
                    [1, 0, 1, 0, 1],
                    [0, 1, 0, 1, 0],
                    [1, 0, 1, 0, 1],
                ],
            )
        )

        self.bombs.append(
            Bomb(
                6,
                "X",
                RARITY_COMMON,
                "It marks the spot. And hits it.",
                [
                    [1, 0, 0, 0, 1],
                    [0, 1, 0, 1, 0],
                    [0, 0, 1, 0, 0],
                    [0, 1, 0, 1, 0],
                    [1, 0, 0, 0, 1],
                ],
            )
        )

        self.bombs.append(
            Bomb(
                7,
                "H0",
                RARITY_COMMON,
                "Can you add the H0,Bomb to the game?' 'Yeah sure I got you'",
                [
                    [1, 0, 0, 0, 1],
                    [1, 0, 0, 0, 1],
                    [1, 1, 1, 1, 1],
                    [1, 0, 0, 0, 1],
                    [1, 0, 0, 0, 1],
                ],
            )
        )

        self.bombs.append(
            Bomb(
                8,
                "P0",
                RARITY_AVERAGE,
                "Not sure why you'd make a bomb like this, but there you go.",
                [
                    [1, 1, 1, 1, 0],
                    [1, 1, 1, 1, 0],
                    [1, 1, 1, 1, 0],
                    [1, 0, 0, 0, 0],
                    [1, 0, 0, 0, 0],
                ],
            )
        )

        self.bombs.append(
            Bomb(
                9,
                "Cherry",
                RARITY_COMMON,
                "Yep, it's a pair of Cherries. ",
                [
                    [0, 0, 1, 0, 0],
                    [0, 0, 1, 0, 0],
                    [0, 0, 1, 0, 0],
                    [1, 1, 0, 1, 1],
                    [1, 1, 0, 1, 1],
                ],
            )
        )

        self.bombs.append(
            Bomb(
                10,
                "e",
                RARITY_AVERAGE,
                "2.71828182845904523536028747135",
                [
                    [1, 1, 1, 1, 1],
                    [1, 0, 0, 0, 1],
                    [1, 1, 1, 1, 1],
                    [1, 0, 0, 0, 0],
                    [1, 1, 1, 1, 1],
                ],
            )
        )

        self.bombs.append(
            Bomb(
                11,
                "A0",
                RARITY_COMMON,
                "I know I'll be A0,O, A0,O0,K.",
                [
                    [0, 0, 1, 0, 0],
                    [0, 1, 0, 1, 0],
                    [0, 1, 1, 1, 0],
                    [1, 0, 0, 0, 1],
                    [1, 0, 0, 0, 1],
                ],
            )
        )

        self.bombs.append(
            Bomb(
                12,
                "ENGLAND",
                RARITY_COMMON,
                "RULE BRITANNIA, BRITANNIA RULES THE WAVES",
                [
                    [0, 0, 1, 0, 0],
                    [0, 0, 1, 0, 0],
                    [1, 1, 1, 1, 1],
                    [0, 0, 1, 0, 0],
                    [0, 0, 1, 0, 0],
                ],
            )
        )


class Game:
    STARTING_HAND_SIZE = 5

    def __init__(self):
        self.deck = []
        self.deck_builder()
        self.player = Player.RED
        self.game_board = Board()
        self.red_hand_size = self.game_board.get_silo_count(Player.RED)
        self.blue_hand_size = self.game_board.get_silo_count(Player.BLUE)

        self.setup = 0
        self.win = False
        self.number_of_factories = 5
        self.number_of_silos = 5

        self.red_hand = self.initialise_hand(Player.RED)
        self.blue_hand = self.initialise_hand(Player.BLUE)
        self.cards = Cards()
        self.offeredcards = []

        self.playersingame = [False, False]
        self.startingboardset = [False, False]
        self.turn_change_event = threading.Event()
        self.game_start_event = threading.Event()

        self.last_played = None

    def initialise_hand(self, player):
        hand = []
        for _ in range(Game.STARTING_HAND_SIZE):
            hand.append(self.get_random_card(player))
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
        if not self.playersingame[0]:
            self.playersingame[0] = True
            return {"player": Player.RED, "ready": False}
        else:
            self.playersingame[1] = True
            self.game_start_event.set()
            self.game_start_event.clear()
            return {"player": Player.BLUE, "ready": True}

    def await_game_start(self):
        print("Waiting for game start")
        self.game_start_event.wait()
        return {"ready": True}

    def place_starting_board(self, player, factories, silos):
        valid = self.place_factories(player, factories) and self.place_silos(
            player, silos
        )
        if not valid:
            return {"valid": False}

        if player == 1:
            self.startingboardset[0] = True
        else:
            self.startingboardset[1] = True

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

        for i in range(0, len(coords)):
            x = coords[i][0]
            y = coords[i][1]
            if self.game_board.board[x][y].state != player:
                return False
            else:
                self.game_board.board[x][y].building = Building.FACTORY

        return True

    def place_silos(self, player, coords):
        if len(coords) != self.number_of_silos:
            return False

        for i in range(0, len(coords)):
            x = coords[i][0]
            y = coords[i][1]
            if self.game_board.board[x][y].state != player:
                return False
            else:
                self.game_board.board[x][y].building = Building.SILO

        return True

    def get_hand_size(self):
        return self.game_board.get_silo_count(self.player)

    def get_game_state(self, player):
        hand = self.red_hand if player == Player.RED else self.blue_hand
        other_hand = self.red_hand if player != Player.RED else self.blue_hand

        return {
            "hand": [i.id for i in hand],
            "otherHand": len(other_hand),
            "board": self.game_board.get_serial_board(player),
            "lastPlayed": self.last_played,
            "destroyedCount": self.game_board.get_destroyed_counts(),
        }

    def deck_builder(self):
        card_holder = Cards()
        card_holder.init_bombs()
        for bomb in card_holder.bombs:
            for _ in range(bomb.rarity):
                self.deck.append(bomb)

    def get_random_card(self, player):
        possible = [
            card
            for card in self.deck
            if (not RARITY_BOMB_LOGIC)
            or (
                card.rarity
                <= (
                    self.game_board.get_factory_count(player)
                    or self.number_of_factories
                )
            )
        ]
        if not possible:
            return None

        return random.choice(possible)

    def get_hand_options(self, player):
        silos = self.game_board.get_silo_count(player)
        hand = self.red_hand if player == Player.RED else self.blue_hand
        if silos < len(hand):
            return []

        hand_options = []
        for _ in range(self.game_board.get_factory_count(player)):
            card = self.get_random_card(player)
            if card is None:
                break
            hand_options.append(card.id)

        self.offeredcards = hand_options
        return hand_options

    def choose_card(self, player, cardid):
        if player != self.player:
            return False

        if cardid not in self.offeredcards:
            return False

        if player == Player.RED:
            self.red_hand.append(self.cards.bombs[cardid - 1])
            self.red_hand_size += 1
        elif player == Player.BLUE:
            self.blue_hand.append(self.cards.bombs[cardid - 1])
            self.blue_hand_size += 1
        else:
            return False

        return True

    def remove_card(self, bomb_id, to_remove, player=None):
        if player is None:
            player = self.player
        hand = self.red_hand if player == Player.RED else self.blue_hand

        if [i.id for i in hand].count(bomb_id) < to_remove:
            return False

        for card in hand:
            if to_remove == 0:
                break
            if card.id == bomb_id:
                hand.remove(card)
                to_remove -= 1
        return True

    def deploy_bomb(self, player, coord, bomb_id, extra):
        if player != self.player:
            return False

        bomb = self.cards.bombs[bomb_id - 1]

        if RARITY_BOMB_LOGIC:
            hand = self.red_hand if player == Player.RED else self.blue_hand

            if len(extra) < bomb.rarity - 1:
                return False
            if not all([self.cards.bombs[i - 1].rarity >= bomb.rarity for i in extra]):
                return False

            to_remove = extra + [bomb_id]
            hand_ids = [i.id for i in hand]
            for i in set(to_remove):
                if hand_ids.count(i) < to_remove.count(i):
                    return False

            for i in set(to_remove):
                self.remove_card(i, to_remove.count(i), player)
        else:
            if not self.remove_card(bomb_id, 1, player):
                return False

        self.game_board.apply_bomb(bomb.shape, int(coord[0]), int(coord[1]))
        self.last_played = bomb.id
        self.swap_turns()
        return True

    def skip_turn(self, player):
        if player != self.player:
            return False
        self.swap_turns()
        return True

    def swap_turns(self):
        self.player *= -1
        self.turn_change_event.set()
        print("Turn change")
        self.turn_change_event.clear()

    def await_turn_change(self):
        print("Waiting for turn change")
        self.turn_change_event.wait()
        print("Got turn change")

        return self.player

    def lost_silo(self):
        hand = self.red_hand if self.player == Player.RED else self.blue_hand
        hand.pop(random.randrange(0, len(hand)))

    def game_over(self):
        red_tiles = 0
        blue_tiles = 0
        for x in range(self.game_board.HEIGHT):
            for y in range(self.game_board.WIDTH):
                if self.game_board.board[x][y].state == State.BLUE:
                    blue_tiles += 1
                if self.game_board.board[x][y].state == State.RED:
                    red_tiles += 1
        if red_tiles == 0:
            self.win = True
            return Player.Red
        if blue_tiles == 0:
            self.win = True
            return Player.Blue
        hand = self.red_hand if self.player == Player.RED else self.blue_hand
        if len(hand) == 0:
            if self.game_board.get_factory_count(self.player) == 0:
                self.win = True
                return self.player


if __name__ == "__main__":
    g = Game()
