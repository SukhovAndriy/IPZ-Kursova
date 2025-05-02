import socket
import threading

class TicTacToeServer:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('26.125.50.236', 5555))
        self.server.listen(2)
        print("[SERVER] Очікування гравців...")

        self.players = {}
        self.board = [""] * 9
        self.turn = "X"

        threading.Thread(target=self.accept_connections, daemon=True).start()

    def accept_connections(self):
        while len(self.players) < 2:
            conn, addr = self.server.accept()
            symbol = "X" if "X" not in self.players.values() else "O"
            self.players[conn] = symbol
            print(f"[SERVER] Гравець {symbol} підключився з {addr}")
            conn.sendall(f"SYMBOL:{symbol}".encode())
            threading.Thread(target=self.handle_client, args=(conn,), daemon=True).start()

        self.broadcast("START")
        self.broadcast(f"TURN:{self.turn}")

    def handle_client(self, conn):
        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                msg = data.decode()

                if msg.startswith("MOVE:"):
                    index = int(msg.split(":")[1])
                    symbol = self.players.get(conn)

                    if self.board[index] == "" and self.turn == symbol:
                        self.board[index] = symbol
                        self.broadcast(f"UPDATE:{index}:{symbol}")

                        if self.check_win(symbol):
                            self.broadcast(f"WIN:{symbol}")
                            self.broadcast("FINISH")
                            break
                        elif "" not in self.board:
                            self.broadcast("DRAW")
                            self.broadcast("FINISH")
                            break
                        else:
                            self.turn = "O" if self.turn == "X" else "X"
                            self.broadcast(f"TURN:{self.turn}")
        except Exception as e:
            print(f"[ERROR] {e}")
        finally:
            print("[SERVER] Клієнт відключився.")
            conn.close()
            if conn in self.players:
                del self.players[conn]

    def broadcast(self, msg):
        for conn in list(self.players):
            try:
                conn.sendall(msg.encode())
            except:
                conn.close()
                if conn in self.players:
                    del self.players[conn]

    def check_win(self, sym):
        combos = [
            [0,1,2],[3,4,5],[6,7,8],
            [0,3,6],[1,4,7],[2,5,8],
            [0,4,8],[2,4,6]
        ]
        return any(all(self.board[i] == sym for i in combo) for combo in combos)

if __name__ == "__main__":
    TicTacToeServer()
    while True:
        pass
