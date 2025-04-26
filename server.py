import socket
import threading
import socket
import threading

class TicTacToeServer:
    def __init__(self, host="127.0.0.1", port=5555):
        self.board = [""] * 9
        self.current_player = "X"
        self.connections = []
        self.host = host
        self.port = port

    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen(2)
        print("Сервер запущено. Очікування гравців...")

        while len(self.connections) < 2:
            conn, addr = server.accept()
            self.connections.append(conn)
            print(f"Гравець {len(self.connections)} підключився: {addr}")
            conn.sendall(self.current_player.encode())
            threading.Thread(target=self.handle_client, args=(conn,)).start()

    def handle_client(self, conn):
        while True:
            try:
                data = conn.recv(1024).decode()
                if not data:
                    break
                index = int(data)

                if self.board[index] == "":
                    self.board[index] = self.current_player
                    winner = self.check_winner()

                    for c in self.connections:
                        c.sendall(f"{index},{self.current_player}".encode())

                    if winner:
                        for c in self.connections:
                            c.sendall(f"END:{winner}".encode())
                        self.board = [""] * 9
                        self.current_player = "X"
                    else:
                        self.current_player = "O" if self.current_player == "X" else "X"

            except:
                break
        conn.close()

    def check_winner(self):
        combos = [
            (0,1,2), (3,4,5), (6,7,8),
            (0,3,6), (1,4,7), (2,5,8),
            (0,4,8), (2,4,6)
        ]
        for i1, i2, i3 in combos:
            if self.board[i1] == self.board[i2] == self.board[i3] != "":
                return self.board[i1]
        if "" not in self.board:
            return "Нічия"
        return None

if __name__ == "__main__":
    server = TicTacToeServer()
    server.start()
