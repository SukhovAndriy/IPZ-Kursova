import socket
import threading

class ClientNetwork:
    def __init__(self, ip, port, on_message):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip, port))
        self.on_message = on_message
        threading.Thread(target=self._receive, daemon=True).start()

    def _receive(self):
        buf = ''
        while True:
            data = self.sock.recv(1024).decode()
            if not data:
                break
            buf += data
            while '\n' in buf:
                line, buf = buf.split('\n', 1)
                self.on_message(line)

    def send(self, msg):
        try:
            self.sock.sendall((msg + '\n').encode())
        except Exception:
            pass