import socket
import typing_game_func as tgf

class TypingServer:
    def __init__(self, host='0.0.0.0', port=65432):
        self.server_address = (host, port)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(self.server_address)
        self.server_socket.listen(1)
        print("サーバーが起動しました...")
       

    def start(self):
        client_socket, client_address = self.server_socket.accept()
        print(f"クライアントが接続しました: {client_address}")

        game = tgf.TypingGame(self.server_socket, client_socket)
        game.start_game(player_number=1)

        self.server_socket.close()
        client_socket.close()

# if __name__ == "__main__":
#     server = TypingServer()
#     server.start()