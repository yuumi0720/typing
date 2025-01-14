import socket
import sys
import asyncio
import typing_game_func as tgf
import team_func as team
import league_func as lg

class TypingServer:
    def __init__(self, mode, host='0.0.0.0', port=65432):
        self.mode = mode
        self.server_address = (host, port)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(self.server_address)
        self.server_socket.listen()
        self.client_sockets = []
        self.player_names = []
        self.num_players = 0
        print(f"サーバーが起動しました... Game Mode: {self.mode}")

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

    
    def handle_connection(self, client_socket):
        try:
            initial_message = self.recv_message(client_socket)
            if initial_message == "SERVER_TEST":
                self.send_message(client_socket, "SERVER_OK")
                client_socket.close()
                return False
            elif initial_message == "CLIENT_CONNECT":
                self.client_sockets.append(client_socket)
                return True
            else:
                print(f"不明なメッセージ：{initial_message}")
                client_socket.close()
                return False
        except Exception as e:
            print(f"接続待機中にエラー: {e}")
            client_socket.close()
            return False

    def start(self):
        try:
            first_client_socket, _ = self.server_socket.accept()
            if self.handle_connection(first_client_socket):
                print(f"最初のクライアントが接続しました")
                self.send_message(self.client_sockets[0], "num_players")
                self.num_players = int(self.recv_message(self.client_sockets[0]))
                print(f"あと{self.num_players - 1}人待っています...")

            while len(self.client_sockets) < self.num_players:
                client_socket, _ = self.server_socket.accept()
                if self.handle_connection(client_socket):
                    print(f"クライアント{len(self.client_sockets)}が接続しました")

            
            
            if self.mode == "vs":
                game = tgf.TypingGame(self.server_socket, self.client_sockets, "end_game2")
                game.start_game()
            elif self.mode == "team":
                game = team.TeamTypingGame(self.server_socket, self.client_sockets)
                game.start_game()
            elif self.mode == "league":
                game = lg.LeagueGame(self.server_socket, self.client_sockets)
                asyncio.run(game.start_league())
            

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
    if len(sys.argv) != 2:
        print("実行方法: python3 typing_server.py <mode>")
        sys.exit(1)

    mode = sys.argv[1]
    if mode not in ["vs", "team", "league"]:
        print("mode: vs or team or league")
        sys.exit(1)

    server = TypingServer(mode)
    server.start()
