import socket
import threading

class TicTacToeServer:
    def __init__(self, host="0.0.0.0", port=5555):
        self.board = [""] * 9
        self.players = {}
        self.turn = "X"
        self.lock = threading.Lock()
        self.host = host
        self.port = port

    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen(2)
        print("Сервер запущено. Очікування гравців...")

        while len(self.players) < 2:
            conn, addr = server.accept()
            symbol = "X" if len(self.players) == 0 else "O"
            self.players[conn] = symbol
            conn.sendall(f"SYMBOL:{symbol}".encode())
            print(f"Підключено гравця {symbol} з адреси {addr}")
            threading.Thread(target=self.handle_client, args=(conn,), daemon=True).start()

    def handle_client(self, conn):
        symbol = self.players[conn]
        try:
            while True:
                data = conn.recv(1024).decode()
                if data.startswith("MOVE:"):
                    index = int(data.split(":")[1])
                    with self.lock:
                        if self.board[index] == "" and self.turn == symbol:
                            self.board[index] = symbol
                            self.broadcast(f"UPDATE:{index},{symbol}")

                            winner = self.check_winner()
                            if winner:
                                self.broadcast(f"END:{winner}")
                                self.reset()
                            else:
                                self.turn = "O" if self.turn == "X" else "X"
                                self.broadcast(f"TURN:{self.turn}")
        except:
            print(f"Гравець {symbol} відключився")
            conn.close()
            del self.players[conn]

    def broadcast(self, message):
        for conn in self.players:
            try:
                conn.sendall(message.encode())
            except:
                pass

    def check_winner(self):
        combos = [
            (0,1,2), (3,4,5), (6,7,8),
            (0,3,6), (1,4,7), (2,5,8),
            (0,4,8), (2,4,6)
        ]
        for i, j, k in combos:
            if self.board[i] == self.board[j] == self.board[k] != "":
                return self.board[i]
        if "" not in self.board:
            return "Нічия"
        return None

    def reset(self):
        self.board = [""] * 9
        self.turn = "X"

if __name__ == "__main__":
    TicTacToeServer().start()
