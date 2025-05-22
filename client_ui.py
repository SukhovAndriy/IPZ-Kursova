import tkinter as tk
from tkinter import messagebox, scrolledtext
from client_network import ClientNetwork
from game_logic import symbols, combos


COLOR_X = '#FF1744'
COLOR_O = '#2196F3'


class ConnectionWindow:
   def __init__(self, on_connect):
       self.root = tk.Tk()
       self.root.title("Підключення до сервера")
       self._center_window(300, 150)
       self.root.resizable(False, False)


       tk.Label(self.root, text="Нік:", font=("Helvetica", 12)).grid(row=0, column=0, pady=5, padx=5)
       self.nick_entry = tk.Entry(self.root, font=("Helvetica", 12))
       self.nick_entry.grid(row=0, column=1, pady=5, padx=5)


       tk.Label(self.root, text="IP:", font=("Helvetica", 12)).grid(row=1, column=0, pady=5, padx=5)
       self.ip_entry = tk.Entry(self.root, font=("Helvetica", 12))
       self.ip_entry.insert(0, "26.125.50.236")
       self.ip_entry.grid(row=1, column=1, pady=5, padx=5)


       tk.Label(self.root, text="Порт:", font=("Helvetica", 12)).grid(row=2, column=0, pady=5, padx=5)
       self.port_entry = tk.Entry(self.root, font=("Helvetica", 12))
       self.port_entry.insert(0, "12345")
       self.port_entry.grid(row=2, column=1, pady=5, padx=5)


       connect_btn = tk.Button(self.root, text="Підключитись", font=("Helvetica", 12, 'bold'),
           command=self.connect, bg="#4CAF50", fg="white", relief=tk.FLAT)
       connect_btn.grid(row=3, column=0, columnspan=2, pady=10, padx=5, sticky='we')


       self.on_connect = on_connect


   def _center_window(self, width, height):
       screen_w = self.root.winfo_screenwidth()
       screen_h = self.root.winfo_screenheight()
       x = (screen_w - width) // 2
       y = (screen_h - height) // 2
       self.root.geometry(f"{width}x{height}+{x}+{y}")


   def connect(self):
       nick = self.nick_entry.get().strip() or "Ноунейм"
       ip = self.ip_entry.get()
       port = int(self.port_entry.get())
       self.root.destroy()
       self.on_connect(ip, port, nick)


   def run(self):
       self.root.mainloop()


class TicTacToeUI:
   def __init__(self, ip, port, nick):
       self.nick = nick
       self.opponent_nick = None
       self.root = tk.Tk()
       self.root.title(f"Хрестики-Нулики | {self.nick}")
       self._center_window(600, 700)
       self.root.configure(bg="#F0F0F0")
       self.root.resizable(False, False)


       self.symbol = ''
       self.my_turn = False
       self.restart_count = 0


       header = tk.Label(self.root, text=f"Ваш нік: {self.nick}", font=("Helvetica", 14), bg="#F0F0F0")
       header.pack(pady=10)


       self.status_label = tk.Label(self.root, text="Очікування гравця..", font=("Helvetica", 12), bg="#F0F0F0")
       self.status_label.pack(pady=5)


       self.game_frame = tk.Frame(self.root, bg="#F0F0F0")
       self.game_frame.pack(pady=10)


       ctrl_frame = tk.Frame(self.root, bg="#F0F0F0")
       ctrl_frame.pack(pady=10)
       restart_btn = tk.Button(ctrl_frame, text="Перезапустити гру", command=self.request_restart,
           font=("Helvetica", 12), bg="#2196F3", fg="white", relief=tk.FLAT)
       restart_btn.grid(row=0, column=0, padx=5)
       exit_btn = tk.Button(ctrl_frame, text="Вийти", command=self.root.destroy,
           font=("Helvetica", 12), bg="#f44336", fg="white", relief=tk.FLAT)
       exit_btn.grid(row=0, column=1, padx=5)
       self.restart_label = tk.Label(ctrl_frame, text="Перезапуск: 0/2", font=("Helvetica", 12), bg="#F0F0F0")
       self.restart_label.grid(row=0, column=2, padx=5)


       chat_frame = tk.LabelFrame(self.root, text="Чат", font=("Helvetica", 12), bg="#F0F0F0")
       chat_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
       self.chat_box = scrolledtext.ScrolledText(chat_frame, state='disabled', height=8, font=("Courier New", 10))
       self.chat_box.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
       entry_frame = tk.Frame(chat_frame, bg="#F0F0F0")
       entry_frame.pack(fill=tk.X, padx=5, pady=5)
       self.chat_entry = tk.Entry(entry_frame, font=("Helvetica", 12))
       self.chat_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0,5))
       send_btn = tk.Button(entry_frame, text="Відправити", command=self.send_chat,
           font=("Helvetica", 12), bg="#4CAF50", fg="white", relief=tk.FLAT)
       send_btn.pack(side=tk.RIGHT)


       self.network = ClientNetwork(ip, port, self.process_message)
       self.network.send(f"NICK:{self.nick}")


   def _center_window(self, width, height):
       screen_w = self.root.winfo_screenwidth()
       screen_h = self.root.winfo_screenheight()
       x = (screen_w - width) // 2
       y = (screen_h - height) // 2
       self.root.geometry(f"{width}x{height}+{x}+{y}")


   def send_chat(self):
       msg = self.chat_entry.get().strip()
       if msg:
           self.network.send(f"CHAT:{msg}")
           self.chat_entry.delete(0, tk.END)


   def process_message(self, line):
       if line.startswith("START:"):
           new_sym = line.split(":")[1]
           self.symbol = new_sym
           if not hasattr(self, 'buttons'):
               self.root.after(0, self.start_game_ui)
           else:
               self.status_label.config(text=f"Ваш символ: {self.symbol}")


       elif line.startswith("OPPONENT_NICK:"):
           self.opponent_nick = line.split(":")[1]


       elif line == "YOUR_TURN":
           self.my_turn = True
           self.status_label.config(text="Ваш хід")


       elif line.startswith("UPDATE:"):
           _, idx, sym = line.split(":")
           btn = self.buttons[int(idx)]
           color = COLOR_X if sym == 'X' else COLOR_O
           btn.config(text=sym, disabledforeground=color, state="disabled")


       elif line.startswith("WIN:"):
           winner_sym = line.split(":")[1]
           if winner_sym == self.symbol:
               winner_nick = self.nick
           else:
               winner_nick = self.opponent_nick or f"Гравець ({winner_sym})"
           for combo in combos:
               if all(self.buttons[i]["text"] == winner_sym for i in combo):
                   for i in combo:
                       self.buttons[i].config(bg="#8BC34A")
                   break
           for btn in self.buttons:
               btn.config(state="disabled")
           messagebox.showinfo("Гра завершена", f"Переміг {winner_nick}")


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


       elif line.startswith("CHAT:"):
           _, sender_nick, msg = line.split(":", 2)
           if not self.opponent_nick and sender_nick != self.nick:
               self.opponent_nick = sender_nick
           self.root.after(0, self.display_chat, sender_nick, msg)


   def display_chat(self, sender_nick, msg):
       self.chat_box.config(state='normal')
       self.chat_box.insert(tk.END, f"[{sender_nick}]: {msg}\n")
       self.chat_box.see(tk.END)
       self.chat_box.config(state='disabled')


   def start_game_ui(self):
       self.status_label.config(text=f"Ваш символ: {self.symbol}")
       self.buttons = []
       for i in range(9):
           btn = tk.Button(self.game_frame, text="", font=("Helvetica", 20, 'bold'), width=4, height=2,
           command=lambda i=i: self.make_move(i), relief=tk.RAISED, bg="#FFFFFF", fg="black",
           activebackground="#EEE", disabledforeground="black")
           btn.grid(row=i//3, column=i%3, padx=5, pady=5)
           self.buttons.append(btn)
       self.default_bg = self.buttons[0].cget("bg")


   def make_move(self, idx):
       if self.my_turn and self.buttons[idx]["text"] == "":
           self.network.send(f"MOVE:{idx}")
           self.my_turn = False
           self.status_label.config(text="Хід супротивника..")


   def request_restart(self):
       self.network.send("RESTART")


   def reset_board(self):
       for btn in self.buttons:
           btn.config(text="", state="normal", bg=self.default_bg, fg="black", disabledforeground="black")
       self.my_turn = False
       self.restart_count = 0
       self.restart_label.config(text="Перезапуск: 0/2")
       self.status_label.config(text=f"Ваш символ: {self.symbol}")


   def run(self):
       self.root.mainloop()


if __name__ == '__main__':
   ConnectionWindow(lambda ip, port, nick: TicTacToeUI(ip, port, nick).run()).run()
