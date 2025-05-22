# server.py
import socket
import threading
import random
from game_logic import Game, symbols

HOST = '26.125.50.236'
PORT = 12345
lock = threading.Lock()

def send_msg(conn, msg):
    conn.sendall((msg + "\n").encode())

def handle_client(conn, player_id, clients, game, restart_requests, nicks):
    try:
        data = conn.recv(1024).decode().strip()
        if data.startswith("NICK:"):
            nick = data.split(":", 1)[1]
            nicks[player_id] = nick

        buffer = ''
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            buffer += data
            while '\n' in buffer:
                line, buffer = buffer.split('\n', 1)

                if all(n is not None for n in nicks):
                    opponent = nicks[1-player_id]
                    send_msg(conn, f"OPPONENT_NICK:{opponent}")
                    nicks[player_id] = nicks[player_id]

                if line.startswith("MOVE:"):
                    idx = int(line.split(":")[1])
                    with lock:
                        if game.current_turn == player_id:
                            symbol = game.make_move(idx)
                            if symbol:
                                for c in clients:
                                    send_msg(c, f"UPDATE:{idx}:{symbol}")
                                if game.check_winner(symbol):
                                    for c in clients:
                                        send_msg(c, f"WIN:{symbol}")
                                elif game.is_full():
                                    for c in clients:
                                        send_msg(c, "TIE")
                                else:
                                    game.next_turn()
                                    send_msg(clients[game.current_turn], "YOUR_TURN")

                elif line == "RESTART":
                    with lock:
                        restart_requests[player_id] = True
                        count = sum(restart_requests)
                    for c in clients:
                        send_msg(c, f"RESTART_COUNT:{count}")

                    if count == 2:
                        with lock:
                            symbol_list = random.sample(symbols, k=2)
                            game.reset()
                            restart_requests[:] = [False, False]
                            game.symbols = symbol_list
                            game.current_turn = symbol_list.index('X')
                        for idx, c in enumerate(clients):
                            send_msg(c, f"START:{symbol_list[idx]}")
                            send_msg(c, "RESET")
                        send_msg(clients[game.current_turn], "YOUR_TURN")

                elif line.startswith("CHAT:"):
                    msg = line.split(":", 1)[1]
                    sender_nick = nicks[player_id] or f"Гравець{player_id}"
                    for c in clients:
                        send_msg(c, f"CHAT:{sender_nick}:{msg}")

    except Exception:
        pass

    for c in clients:
        if c is not conn:
            try:
                send_msg(c, "OPPONENT_LEFT")
            except:
                pass
    conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[СЕРВЕР] Запущено на {HOST}:{PORT}")

    try:
        while True:
            print("[СЕРВЕР] Очікування двох гравців..")
            clients = []
            nicks = [None, None]
            restart_requests = [False, False]
            game = Game()

            while len(clients) < 2:
                conn, addr = server.accept()
                print(f"[ПІДКЛЮЧЕНО] {addr}")
                clients.append(conn)

            symbol_list = random.sample(symbols, k=2)
            game.symbols = symbol_list
            game.current_turn = symbol_list.index('X')
            for idx, conn in enumerate(clients):
                send_msg(conn, f"START:{symbol_list[idx]}")
            send_msg(clients[game.current_turn], "YOUR_TURN")

            threads = []
            for idx, conn in enumerate(clients):
                t = threading.Thread(
                    target=handle_client,
                    args=(conn, idx, clients, game, restart_requests, nicks),
                    daemon=True
                )
                t.start()
                threads.append(t)

            for t in threads:
                t.join()
            print("[СЕРВЕР] Сесія завершена.")

    except KeyboardInterrupt:
        print("\n[СЕРВЕР] Зупинка.")
    finally:
        server.close()

if __name__ == "__main__":
    start_server()
