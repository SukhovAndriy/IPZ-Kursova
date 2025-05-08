import tkinter as tk

class TicTacToeUI:
    def __init__(self, protocol):
        self.protocol = protocol
        self.symbol = ''
        self.my_turn=False
        self.restart_count=0
        self.build()

    def build(self):
        self.root = tk.Tk()
        self.status = tk.Label(self.root,text='Очікування...')
        self.status.pack()
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack()
        self.buttons=[tk.Button(self.board_frame,font=('Arial',24),width=4,height=2,
                         command=lambda i=i:self.on_cell(i)) for i in range(9)]
        for i,btn in enumerate(self.buttons): btn.grid(row=i//3,column=i%3,padx=2,pady=2)
        ctrl = tk.Frame(self.root); ctrl.pack(pady=5)
        tk.Button(ctrl,text='Перезапустити',command=self.on_restart).grid(row=0,column=0)
        tk.Button(ctrl,text='Вийти',command=self.root.destroy).grid(row=0,column=1)
        self.restart_label=tk.Label(ctrl,text='0/2');self.restart_label.grid(row=0,column=2)

    def on_cell(self,i):
        if self.my_turn and self.buttons[i]['text']=='':
            self.protocol.send(f'MOVE:{i}')
            self.my_turn=False

    def on_restart(self):
        self.protocol.send('RESTART')

    def start(self):
        self.root.mainloop()