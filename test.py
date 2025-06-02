import unittest
from game_logic import Game, symbols, combos

class TestGameLogic(unittest.TestCase):
    def setUp(self):
        self.game = Game()

    def test_initial_state(self):
        self.assertEqual(self.game.board, [''] * 9)
        self.assertEqual(self.game.current_turn, 0)
        self.assertEqual(self.game.symbols, symbols)

    def test_make_move_valid(self):
        symbol = self.game.make_move(4)
        self.assertEqual(symbol, symbols[0])
        self.assertEqual(self.game.board[4], symbols[0])

    def test_make_move_invalid_out_of_bounds(self):
        self.assertIsNone(self.game.make_move(-1))
        self.assertIsNone(self.game.make_move(9))

    def test_make_move_invalid_already_taken(self):
        self.game.make_move(0)
        self.assertIsNone(self.game.make_move(0))

    def test_check_winner_rows(self):
        for i in combos[0]:
            self.game.board[i] = symbols[0]
        self.assertTrue(self.game.check_winner(symbols[0]))

    def test_check_winner_columns(self):
        for i in combos[3]:  # (0,3,6)
            self.game.board[i] = symbols[1]
        self.assertTrue(self.game.check_winner(symbols[1]))

    def test_check_winner_diagonals(self):
        for i in combos[6]:  # (0,4,8)
            self.game.board[i] = symbols[0]
        self.assertTrue(self.game.check_winner(symbols[0]))

    def test_no_winner(self):
        moves = [0, 1, 4, 2, 3]
        for move in moves:
            self.game.board[move] = symbols[0] if move % 2 == 0 else symbols[1]
        self.assertFalse(self.game.check_winner(symbols[0]))
        self.assertFalse(self.game.check_winner(symbols[1]))

    def test_is_full(self):
        self.assertFalse(self.game.is_full())
        self.game.board = [symbols[i % 2] for i in range(9)]
        self.assertTrue(self.game.is_full())

    def test_next_turn(self):
        self.game.next_turn()
        self.assertEqual(self.game.current_turn, 1)
        self.game.next_turn()
        self.assertEqual(self.game.current_turn, 0)

    def test_reset(self):
        self.game.board = [symbols[i % 2] for i in range(9)]
        self.game.current_turn = 1
        self.game.symbols = [symbols[1], symbols[0]]
        self.game.reset()
        self.assertEqual(self.game.board, [''] * 9)
        self.assertEqual(self.game.current_turn, 0)
        self.assertEqual(self.game.symbols, symbols)

if __name__ == '__main__':
    unittest.main()
