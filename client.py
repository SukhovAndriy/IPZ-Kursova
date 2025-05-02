import socket
import threading
import tkinter as tk
from tkinter import messagebox


class TicTacToeClient:
   def __init__(self):
       self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       self.root = tk.Tk()
       self.root.title("Очікування підключення...")
       self.symbol = None
       self.my_turn = False
       self.game_over = False


       self.buttons = []
       self.create_ui()


       threading.Thread(target=self.connect_to_server, daemon=True).start()
       self.root.mainloop()


   def create_ui(self):
       for i in range(9):
           btn = tk.Button(self.root, text="", font=("Arial", 24), width=5, height=2,
                           command=lambda i=i: self.make_move(i))
           btn.grid(row=i // 3, column=i % 3)
           self.buttons.append(btn)


   def connect_to_server(self):
       try:
           self.client.connect(("26.125.50.236", 5555))
           threading.Thread(target=self.receive_data, daemon=True).start()
       except Exception as e:
           messagebox.showerror("Помилка", f"Не вдалося підключитися до сервера: {e}")
           self.root.destroy()


   def receive_data(self):
       try:
           while True:
               data = self.client.recv(1024).decode()
               if not data:
                   break
               print("[DEBUG] Отримано", data)


               if data.startswith("SYMBOL:"):
                   self.symbol = data.split(":")[1]
                   self.root.title(f"Гравець {self.symbol}")
               elif data == "START":
                   print("[DEBUG] Гра почалася")
               elif data.startswith("TURN:"):
                   turn = data.split(":")[1]
                   self.my_turn = (turn == self.symbol)
                   self.root.title(f"Гравець {self.symbol} {'(Ваш хід)' if self.my_turn else '(Хід суперника)'}")
               elif data.startswith("UPDATE:"):
                   _, idx, sym = data.split(":")
                   idx = int(idx)
                   self.buttons[idx].config(text=sym, state="disabled")
               elif data.startswith("WIN:"):
                   winner = data.split(":")[1]
                   self.game_over = True
                   messagebox.showinfo("Гра закінчена", f"Гравець {winner} переміг")
               elif data == "DRAW":
                   self.game_over = True
                   messagebox.showinfo("Гра закінчена", "Нічия")
               elif data == "FINISH":
                   self.client.close()
                   break
       except Exception as e:
           messagebox.showerror("Помилка", f"Втрачено з’єднання з сервером: {e}")
           self.root.quit()


   def make_move(self, index):
       if self.my_turn and not self.game_over and self.buttons[index]["text"] == "":
           try:
               self.client.sendall(f"MOVE:{index}".encode())
               self.my_turn = False
               print(f"[DEBUG] Відправка ходу: {index}")
           except:
               messagebox.showerror("Помилка", "З'єднання з сервером втрачено")
               self.root.quit()


if __name__ == "__main__":
   TicTacToeClient()


