import socket
import threading
from game_logic import TicTacToeGame

HOST, PORT = '26.125.50.236', 12345

class TicTacToeServer:
    def __init__(self):
        self.game = TicTacToeGame()
        self.clients = []
        self.symbols = ['X','O']
        self.sock = socket.socket()

    def send(self, conn, msg):
        conn.sendall((msg+'\n').encode())

    def broadcast(self, msg):
        for c in self.clients:
            self.send(c, msg)

    def handle_client(self, conn, pid):
        try:
            buffer = ''
            while True:
                data = conn.recv(1024).decode()
                if not data:
                    break
                buffer += data
                while '\n' in buffer:
                    line, buffer = buffer.split('\n',1)
                    self.process(line, pid)
        finally:
            self.clients.remove(conn)
            self.broadcast('OPPONENT_LEFT')
            conn.close()

    def process(self, msg, pid):
        if msg.startswith('MOVE:'):
            idx = int(msg.split(':')[1])
            if self.game.move(pid, idx):
                sym = self.symbols[pid]
                self.broadcast(f'UPDATE:{idx}:{sym}')
                if self.game.check_winner(sym):
                    self.broadcast(f'WIN:{sym}')
                elif self.game.is_full():
                    self.broadcast('TIE')
                else:
                    self.game.switch_player()
                    self.send(self.clients[self.game.current_player],'YOUR_TURN')
        elif msg == 'RESTART':
            votes = self.game.vote_restart(pid)
            self.broadcast(f'RESTART_COUNT:{votes}')
            if votes == 2:
                self.game.reset()
                self.broadcast('RESET')
                self.send(self.clients[0],'YOUR_TURN')

    def start(self):
        self.sock.bind((HOST, PORT))
        self.sock.listen(2)
        print(f'[SERVER] Listening on {HOST}:{PORT}')
        while True:
            if len(self.clients) < 2:
                conn, _ = self.sock.accept()
                pid = len(self.clients)
                self.clients.append(conn)
                self.send(conn, f'START:{self.symbols[pid]}')
                if pid == 1:
                    self.send(self.clients[0], 'YOUR_TURN')
                threading.Thread(target=self.handle_client, args=(conn, pid), daemon=True).start()

if __name__ == '__main__':
    TicTacToeServer().start()