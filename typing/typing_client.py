import socket
import time

class TypingClient:
    def __init__(self, host='127.0.0.1', port=65432):
        self.server_address = (host, port)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(self.server_address)
        print("サーバーに接続しました。")

        self.send_message(self.client_socket, "CLIENT_CONNECT")

    def send_message(self, socket, message):
        socket.sendall(message.encode('utf-8'))

    def recv_message(self, socket):
        try:
            message = socket.recv(1024).decode('utf-8').strip()
            return message
        except Exception as e:
            print(f"受信中にエラー: {e}")
            return ""


    def start(self):
        try:
            while True:
                message = self.recv_message(self.client_socket)

                if message == "num_players":
                    num_plyaers = input("プレイヤー人数の入力>> ")
                    self.send_message(self.client_socket, num_plyaers)
                
                elif message == "name":
                    name = input("名前を入力>> ")
                    self.send_message(self.client_socket, name)
                    
                
                elif "ゲーム開始" in message:
                    print(message)
                
                elif message== "wait":
                    print("\nwait...")
                    result = self.recv_message(self.client_socket)
                    print(result)
                    continue

                elif message == "end_game1":
                    time.sleep(0.2)
                    print("\nゲーム終了")
                    winner_result = self.recv_message(self.client_socket)
                    print(winner_result)
                    continue  # ゲーム終了時

                elif message == "end_game2":
                    time.sleep(0.2)
                    winner_result = self.recv_message(self.client_socket)
                    print(winner_result)
                    break
                
                elif "単語" in message:
                    time.sleep(0.2)
                    print(f"\n{message}")
                    start_time = time.time()
                    player_input = input("入力: ")
                    player_time = time.time() - start_time

                    # 入力結果とタイムをサーバーに送信
                    self.send_message(self.client_socket, f"{player_input}, {player_time:.2f}")
                    score_result = self.recv_message(self.client_socket)
                    print(score_result)

                else:
                    print("\n" + message)
                        
        except Exception as e:
            print(f"エラー: {e}")
        finally:
            self.client_socket.close()
