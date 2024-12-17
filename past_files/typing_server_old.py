import socket
import typing_game_func as tgf
import team_func as taem

class TypingServer:
    def __init__(self, host='0.0.0.0', port=65432):
        self.server_address = (host, port)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(self.server_address)
        self.server_socket.listen()
        self.client_sockets = []
        self.num_players = 0
        print("サーバーが起動しました...")
       

    def start(self):
        self.num_players = int(input("プレイヤーは人数を入力してください>> ")) - 1
        print(f"あと{self.num_players}人待っています...")

        for i in range(self.num_players):
            client_socket, client_address = self.server_socket.accept()
            self.client_sockets.append(client_socket)
            print(f"クライアント{i+1}が接続しました")

        mode = input("vs or team >> ")
        if mode == "vs":
            game = tgf.TypingGame(self.server_socket, self.client_sockets)
            game.start_game()
        elif mode == "team":
            game = taem.TeamTypingGame(self.server_socket, self.client_sockets)
            game.start_game()

        self.server_socket.close()
        for client_socket in self.client_sockets:
            client_socket.close()

# if __name__ == "__main__":
#     server = TypingServer()
#     server.start()