import tkinter as tk
from tkinter import messagebox
from logic import Game

class GameUI:
    def __init__(self, root):
        self.root = root
        self.game = Game()
        self.buttons = []

        self.create_widgets()

    def create_widgets(self):
        # Ігрове поле
        for i in range(9):
            btn = tk.Button(self.root, text="", font=("Arial", 24),
                            width=5, height=2, command=lambda i=i: self.handle_click(i))
            btn.grid(row=i // 3, column=i % 3)
            self.buttons.append(btn)

        # Кнопка перезапуску
        reset_btn = tk.Button(self.root, text="Перезапустити гру", font=("Arial", 14),
                              command=self.reset_game)
        reset_btn.grid(row=3, column=0, columnspan=3, pady=10)

    def handle_click(self, index):
        result = self.game.make_move(index)
        self.update_board()

        if result:
            if result == "Нічия":
                messagebox.showinfo("Гра закінчена", "Нічия!")
            else:
                messagebox.showinfo("Гра закінчена", f"Гравець {result} переміг!")
            self.disable_board()

    def update_board(self):
        for i in range(9):
            self.buttons[i].config(text=self.game.board[i])
            if self.game.board[i] != "":
                self.buttons[i].config(state="disabled")

    def disable_board(self):
        for btn in self.buttons:
            btn.config(state="disabled")

    def reset_game(self):
        self.game.reset()
        for btn in self.buttons:
            btn.config(text="", state="normal")
