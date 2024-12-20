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
        self.player_names = []
        self.num_players = 0
        print("サーバーが起動しました...")

    def send_message(self, socket, message):
        socket.sendall(message.encode('utf-8'))

    def recv_message(self, socket):
        return socket.recv(1024).decode('utf-8').strip()
       

    def start(self):
        first_client_socket, _ = self.server_socket.accept()
        self.client_sockets.append(first_client_socket)
        print("最初のクライアントが接続しました")

        # self.num_players = int(input("プレイヤーは人数を入力してください>> ")) - 1
        self.send_message(self.client_sockets[0], "num_players")
        self.num_players = int(self.recv_message(self.client_sockets[0]))
        print(f"あと{self.num_players - 1}人待っています...")

        for i in range(self.num_players - 1):
            client_socket, _ = self.server_socket.accept()
            self.client_sockets.append(client_socket)
            print(f"クライアント{i+2}が接続しました")

        # for client_socket in self.client_sockets:
        #     self.send_message(client_socket, "name")
        #     player_name = self.recv_message(client_socket)
        #     self.player_names.append(player_name)

        # self.send_message(self.client_sockets[0], "game_mode")
        # game_mode = self.recv_message(self.client_sockets[0])

        # if game_mode == "vs":
        game = tgf.TypingGame(self.server_socket, self.client_sockets)
        game.start_game()
        # elif game_mode == "team":
        #     game = taem.TeamTypingGame(self.server_socket, self.client_sockets)
        #     game.start_game()

        
        for client_socket in self.client_sockets:
            client_socket.close()

        self.server_socket.close()

if __name__ == "__main__":
    server = TypingServer()
    server.start()
