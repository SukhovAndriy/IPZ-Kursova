symbols = ['X', 'O']

class Game:
    def __init__(self):
        self.board = [''] * 9
        self.current_turn = 0

    def make_move(self, idx):
        if 0 <= idx < 9 and self.board[idx] == '':
            symbol = symbols[self.current_turn]
            self.board[idx] = symbol
            return symbol
        return None

    def check_winner(self, symbol):
        combos = [
            (0,1,2),(3,4,5),(6,7,8),
            (0,3,6),(1,4,7),(2,5,8),
            (0,4,8),(2,4,6)
        ]
        return any(all(self.board[i] == symbol for i in combo) for combo in combos)

    def is_full(self):
        return all(cell != '' for cell in self.board)

    def next_turn(self):
        self.current_turn = 1 - self.current_turn

    def reset(self):
        self.board = [''] * 9
        self.current_turn = 0