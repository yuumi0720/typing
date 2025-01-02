import socket
import asyncio
import typing_game_func as tgf
import team_func as taem
import league_func as lg

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
    
    def broadcast(self, message):
        for client_socket in self.client_sockets:
            self.send_message(client_socket, message)

    def close_all_client(self):
        self.broadcast("サーバーが閉じました")
        for client_socket in self.client_sockets:
            try:
                client_socket.close()
            except Exception as e:
                print(f"クライアントの切断中にエラー: {e}")
       

    def start(self):
        try:
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
            # game = tgf.TypingGame(self.server_socket, self.client_sockets, "end_game2")
            # game.start_game()

            game = lg.LeagueGame(self.server_socket, self.client_sockets)
            asyncio.run(game.start_league())
            # elif game_mode == "team":
            #     game = taem.TeamTypingGame(self.server_socket, self.client_sockets)
            #     game.start_game()

        except KeyboardInterrupt:
            print("サーバーが停止されました")
        except Exception as e:
            print(f"エラー: {e}")
        finally:
            self.close_all_client()
            try:
                self.server_socket.close()
            except Exception as e:
                print(f"サーバーの切断中にエラー: {e}")
            
        
if __name__ == "__main__":
    server = TypingServer()
    server.start()
