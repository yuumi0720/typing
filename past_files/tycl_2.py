import socket
import typing_game_func as tgf

class TypingClinet:
    def __init__(self, host='127.0.0.1', port=65432):
        
        self.server_address = (host, port)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(self.server_address)
        print("サーバーに接続しました。")

    def start(self):
        game = tgf.TypingGame(self.client_socket, self.client_socket)
        game.start_game(player_number=2)

        self.client_socket.close()

# if __name__ == "__main__":
#     client = TypingClinet()
#     client.start()