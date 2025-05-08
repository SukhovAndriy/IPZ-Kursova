import socket
from threading import Thread

class ClientProtocol:
    def __init__(self, ip, port, on_message):
        self.sock = socket.socket()
        self.sock.connect((ip, port))
        self.on_message = on_message
        Thread(target=self.listen, daemon=True).start()

    def send(self, msg):
        self.sock.sendall((msg+'\n').encode())

    def listen(self):
        buf = ''
        while True:
            data = self.sock.recv(1024).decode()
            if not data:
                break
            buf += data
            while '\n' in buf:
                line, buf = buf.split('\n', 1)
                self.on_message(line)
        self.sock.close()