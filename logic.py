class Game:
    def __init__(self):
        self.board = [""] * 9
        self.current_player = "X"
        self.game_over = False

    def make_move(self, index):
        if self.game_over or self.board[index] != "":
            return None  # Хід недійсний

        self.board[index] = self.current_player
        winner = self.check_winner()

        if winner:
            self.game_over = True
            return winner

        self.current_player = "O" if self.current_player == "X" else "X"
        return None  # Гра триває

    def check_winner(self):
        combos = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Горизонталі
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Вертикалі
            (0, 4, 8), (2, 4, 6)              # Діагоналі
        ]

        for i1, i2, i3 in combos:
            if self.board[i1] == self.board[i2] == self.board[i3] and self.board[i1] != "":
                return self.board[i1]

        if "" not in self.board:
            return "Нічия"

        return None

    def reset(self):
        self.board = [""] * 9
        self.current_player = "X"
        self.game_over = False
