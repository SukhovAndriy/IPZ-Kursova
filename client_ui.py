import tkinter as tk
from tkinter import messagebox

class TicTacToeUI:
    def __init__(self, protocol):
        self.protocol = protocol
        self.symbol = ''
        self.my_turn = False
        self.restart_count = 0
        self.build()

    def build(self):
        self.root = tk.Tk()
        self.status = tk.Label(self.root, text='Очікування...')
        self.status.pack()
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack()
        self.buttons = []
        for i in range(9):
            btn = tk.Button(
                self.board_frame,
                font=('Arial', 24),
                width=4,
                height=2,
                command=lambda i=i: self.on_cell(i)
            )
            btn.grid(row=i//3, column=i%3, padx=2, pady=2)
            self.buttons.append(btn)
        ctrl = tk.Frame(self.root)
        ctrl.pack(pady=5)
        tk.Button(ctrl, text='Перезапустити', command=self.on_restart).grid(row=0, column=0)
        tk.Button(ctrl, text='Вийти', command=self.root.destroy).grid(row=0, column=1)
        self.restart_label = tk.Label(ctrl, text='0/2')
        self.restart_label.grid(row=0, column=2)

    def on_cell(self, i):
        if self.my_turn and self.buttons[i]['text'] == '':
            self.protocol.send(f'MOVE:{i}')
            self.my_turn = False

    def on_restart(self):
        self.protocol.send('RESTART')

    def process(self, msg):
        if msg.startswith('START:'):
            self.symbol = msg.split(':')[1]
            self.status.config(text=f'Ваша фігура: {self.symbol}')
        elif msg == 'YOUR_TURN':
            self.my_turn = True
        elif msg.startswith('UPDATE:'):
            _, idx, sym = msg.split(':')
            self.buttons[int(idx)].config(text=sym, state='disabled')
        elif msg.startswith('WIN:'):
            winner = msg.split(':')[1]
            messagebox.showinfo('Гра завершена', f'Переміг гравець {winner}!')
        elif msg == 'TIE':
            messagebox.showinfo('Гра завершена', 'Нічия!')
        elif msg.startswith('RESTART_COUNT:'):
            count = int(msg.split(':')[1])
            if count < 2:
                self.restart_count = count
                self.restart_label.config(text=f'{count}/2')
        elif msg == 'RESET':
            for btn in self.buttons:
                btn.config(text='', state='normal')
            self.my_turn = False
            self.restart_count = 0
            self.restart_label.config(text='0/2')
        elif msg == 'OPPONENT_LEFT':
            messagebox.showinfo('Увага', 'Ваш суперник покинув гру.')
            self.root.destroy()

    def start(self):
        self.root.mainloop()