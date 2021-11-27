from backend.master import building, state


class Tile:
    def __init__(self, state, building):
        self.state = state
        self.building = building

    def get_building():
        return building
    
    def get_state():
        return state

    def set_building(self, building):
        self.building = building

    def set_state(self, state):
        self.state = state

class Board:
    def __init__(self, board):
        self.board = [15][30]
        self.board.fill_board()

    def fill_board(self):
        for i in range(0, len(self.board)):
            for j in range(len(self.board[i])):
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



                
    
    def get_silo(self):
        pass

    def apply_bomb(self):
        pass