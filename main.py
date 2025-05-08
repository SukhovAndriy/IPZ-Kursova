from client_logic import ClientProtocol
from client_ui import TicTacToeUI

if __name__ == '__main__':
    app = TicTacToeUI(None)
    proto = ClientProtocol(
        '26.125.50.236',
        12345,
        on_message=lambda msg: app.process(msg)
    )
    app.protocol = proto
    app.start()