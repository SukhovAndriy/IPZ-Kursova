import socket
import threading
import tkinter as tk
from tkinter import messagebox

class TicTacToeClient:
    def __init__(self, host="127.0.0.1", port=5555):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        self.symbol = ""
        self.my_turn = False
        self.board = [""] * 9

        self.root = tk.Tk()
        self.root.title("Хрестики-Нулики")
        self.buttons = []
        self.create_ui()

        threading.Thread(target=self.receive_data, daemon=True).start()
        self.root.mainloop()

    def create_ui(self):
        for i in range(9):
            btn = tk.Button(self.root, text="", font=("Arial", 24), width=5, height=2,
                            command=lambda i=i: self.make_move(i))
            btn.grid(row=i//3, column=i%3)
            self.buttons.append(btn)

    def make_move(self, index):
        if self.my_turn and self.board[index] == "":
            self.client.sendall(f"MOVE:{index}".encode())

    def receive_data(self):
        while True:
            try:
                data = self.client.recv(1024).decode()
                if data.startswith("SYMBOL:"):
                    self.symbol = data.split(":")[1]
                    self.root.title(f"Ви гравець {self.symbol}")
                    if self.symbol == "X":
                        self.my_turn = True

                elif data.startswith("TURN:"):
                    turn = data.split(":")[1]
                    self.my_turn = (turn == self.symbol)

                elif data.startswith("UPDATE:"):
                    index, sym = data.split(":")[1].split(",")
                    self.board[int(index)] = sym
                    self.update_ui()

                elif data.startswith("END:"):
                    winner = data.split(":")[1]
                    message = "Нічия!" if winner == "Нічия" else f"Гравець {winner} переміг!"
                    messagebox.showinfo("Гра завершена", message)
                    self.reset_ui()
            except:
                break

    def update_ui(self):
        for i in range(9):
            self.buttons[i].config(text=self.board[i])
            if self.board[i] != "":
                self.buttons[i].config(state="disabled")

    def reset_ui(self):
        self.board = [""] * 9
        for btn in self.buttons:
            btn.config(text="", state="normal")

if __name__ == "__main__":
    TicTacToeClient()
