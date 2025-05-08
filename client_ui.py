import tkinter as tk
from tkinter import messagebox
from client_network import ClientNetwork

class ConnectionWindow:
    def __init__(self, on_connect):
        self.root = tk.Tk()
        self.root.title("Підключення до сервера")
        tk.Label(self.root, text="IP:").grid(row=0, column=0)
        self.ip_entry = tk.Entry(self.root)
        self.ip_entry.insert(0, "26.125.50.236")
        self.ip_entry.grid(row=0, column=1)
        tk.Label(self.root, text="Порт:").grid(row=1, column=0)
        self.port_entry = tk.Entry(self.root)
        self.port_entry.insert(0, "12345")
        self.port_entry.grid(row=1, column=1)
        tk.Button(self.root, text="Підключитись", command=self.connect).grid(row=2, column=0, columnspan=2)
        self.on_connect = on_connect

    def connect(self):
        ip = self.ip_entry.get()
        port = int(self.port_entry.get())
        self.root.destroy()
        self.on_connect(ip, port)

    def run(self):
        self.root.mainloop()

class TicTacToeUI:
    def __init__(self, ip, port):
        self.root = tk.Tk()
        self.root.title("Очікування гравця")
        self.symbol = ''
        self.my_turn = False
        self.restart_count = 0
        self.status_label = tk.Label(self.root, text="Очікування підключення іншого гравця..")
        self.status_label.pack(padx=20, pady=10)
        self.game_frame = tk.Frame(self.root)
        self.game_frame.pack()
        ctrl_frame = tk.Frame(self.root)
        ctrl_frame.pack(pady=10)
        tk.Button(ctrl_frame, text="Перезапустити гру", command=self.request_restart).grid(row=0, column=0, padx=5)
        tk.Button(ctrl_frame, text="Вийти", command=self.root.destroy).grid(row=0, column=1, padx=5)
        self.restart_label = tk.Label(ctrl_frame, text="Перезапуск: 0/2")
        self.restart_label.grid(row=0, column=2, padx=5)
        self.network = ClientNetwork(ip, port, self.process_message)

    def process_message(self, line):
        if line.startswith("START:"):
            self.symbol = line.split(":")[1]
            self.root.after(0, self.start_game_ui)
        elif line == "YOUR_TURN":
            self.my_turn = True
        elif line.startswith("UPDATE:"):
            _, idx, sym = line.split(":")
            btn = self.buttons[int(idx)]
            btn.config(text=sym, state="disabled")
        elif line.startswith("WIN:"):
            winner = line.split(":")[1]
            messagebox.showinfo("Гра завершена", f"Переміг гравець {winner}")
        elif line == "TIE":
            messagebox.showinfo("Гра завершена", "Нічия")
        elif line.startswith("RESTART_COUNT:"):
            count = int(line.split(":")[1])
            if count < 2:
                self.restart_count = count
                self.restart_label.config(text=f"Перезапуск: {count}/2")
        elif line == "RESET":
            self.reset_board()
        elif line == "OPPONENT_LEFT":
            messagebox.showinfo("Злився", "Суперник покинув гру.")
            self.root.destroy()

    def start_game_ui(self):
        self.root.title(f"Гравець {self.symbol}")
        self.status_label.config(text=f"Знак: {self.symbol}")
        self.buttons = []
        for i in range(9):
            btn = tk.Button(self.game_frame, text="", font=("Arial", 24), width=4, height=2, command=lambda i=i: self.make_move(i))
            btn.grid(row=i//3, column=i%3, padx=2, pady=2)
            self.buttons.append(btn)

    def make_move(self, idx):
        if self.my_turn and self.buttons[idx]["text"] == "":
            self.network.send(f"MOVE:{idx}")
            self.my_turn = False

    def request_restart(self):
        self.network.send("RESTART")

    def reset_board(self):
        for btn in getattr(self, 'buttons', []):
            btn.config(text="", state="normal")
        self.my_turn = False
        self.restart_count = 0
        self.restart_label.config(text="Перезапуск: 0/2")

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    ConnectionWindow(lambda ip, port: TicTacToeUI(ip, port).run()).run()