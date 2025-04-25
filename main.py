import tkinter as tk
from Interface import GameUI

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Хрестики-Нулики")
    root.resizable(False, False)

    game_ui = GameUI(root)
    root.mainloop()
    root.mainloop()