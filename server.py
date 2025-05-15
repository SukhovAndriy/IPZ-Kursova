import socket
import threading
from game_logic import Game, symbols

HOST = '26.125.50.236'
PORT = 12345
lock = threading.Lock()

def send_msg(conn, msg):
    conn.sendall((msg + "\n").encode())

def handle_client(conn, player_id, clients, game, restart_requests):
    try:
        buffer = ''
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            buffer += data
            while '\n' in buffer:
                line, buffer = buffer.split('\n', 1)
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
                            game.reset()
                            restart_requests[:] = [False, False]
                        for c in clients:
                            send_msg(c, "RESET")
                        send_msg(clients[0], "YOUR_TURN")
                elif line.startswith("CHAT:"):
                    msg = line.split(":", 1)[1]
                    for c in clients:
                        send_msg(c, f"CHAT:{player_id}:{msg}")
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
            game = Game()
            restart_requests = [False, False]

            while len(clients) < 2:
                conn, addr = server.accept()
                print(f"[ПІДКЛЮЧЕНО] {addr}")
                clients.append(conn)

            for idx, conn in enumerate(clients):
                send_msg(conn, f"START:{symbols[idx]}")
            send_msg(clients[0], "YOUR_TURN")

            threads = []
            for idx, conn in enumerate(clients):
                t = threading.Thread(target=handle_client, args=(conn, idx, clients, game, restart_requests), daemon=True)
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
