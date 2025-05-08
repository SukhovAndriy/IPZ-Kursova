from threading import Lock

class TicTacToeGame:
    WIN_COMBOS = [
        (0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)
    ]

    def __init__(self):
        self.board = [''] * 9
        self.current_player = 0
        self.lock = Lock()
        self.restart_votes = [False, False]

    def move(self, player_id, index):
        with self.lock:
            if self.board[index] or self.current_player != player_id:
                return False
            symbol = ['X','O'][player_id]
            self.board[index] = symbol
            return True

    def check_winner(self, symbol):
        return any(all(self.board[i] == symbol for i in combo) for combo in self.WIN_COMBOS)

    def is_full(self):
        return '' not in self.board

    def switch_player(self):
        self.current_player = 1 - self.current_player

    def reset(self):
        with self.lock:
            self.board = ['']*9
            self.current_player = 0
            self.restart_votes = [False, False]

    def vote_restart(self, player_id):
        with self.lock:
            self.restart_votes[player_id] = True
            return sum(self.restart_votes)