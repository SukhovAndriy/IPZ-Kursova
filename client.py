import socket
import threading
import tkinter as tk
from tkinter import messagebox

class TicTacToeClient:
    def __init__(self, host="127.0.0.1", port=5555):
        self.root = tk.Tk()
        self.root.title("Хрестики-Нулики — Онлайн")
        self.board = [""] * 9
        self.buttons = []
        self.my_symbol = ""
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        self.create_ui()
        threading.Thread(target=self.receive_data, daemon=True).start()

    def create_ui(self):
        for i in range(9):
            btn = tk.Button(self.root, text="", font=("Arial", 24),
                            width=5, height=2, command=lambda i=i: self.send_move(i))
            btn.grid(row=i // 3, column=i % 3)
            self.buttons.append(btn)

    def send_move(self, index):
        if self.board[index] == "" and self.my_symbol:
            self.client.sendall(str(index).encode())

    def receive_data(self):
        self.my_symbol = self.client.recv(1024).decode()
        self.root.title(f"Гравець: {self.my_symbol}")
        while True:
            data = self.client.recv(1024).decode()
            if data.startswith("END:"):
                winner = data.split(":")[1]
                messagebox.showinfo("Гра завершена!", f"Результат: {winner}")
                self.reset_board()
            else:
                index, symbol = data.split(",")
                self.board[int(index)] = symbol
                self.update_ui()

    def update_ui(self):
        for i in range(9):
            self.buttons[i].config(text=self.board[i])
            if self.board[i] != "":
                self.buttons[i].config(state="disabled")

    def reset_board(self):
        self.board = [""] * 9
        for btn in self.buttons:
            btn.config(text="", state="normal")

if __name__ == "__main__":
    client = TicTacToeClient()
    client.root.mainloop()
