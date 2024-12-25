import socket
import time

class TypingClient:
    def __init__(self, host='127.0.0.1', port=65432):
        
        self.server_address = (host, port)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(self.server_address)
        print("サーバーに接続しました。")

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
                    
                # elif message == "game_mode":
                #     game_mode = input("vs or team >>")
                #     self.send_message(self.client_socket, game_mode)
                
                # elif message == "mode_select":
                #     mode_select = input("モードを選択 easy or hard >> ")
                #     self.send_message(self.client_socket, mode_select)

                elif "ゲーム開始" in message:
                    print(message)
                    break
                
            while True:               
                # サーバーから単語を受け取る
                word = self.recv_message(self.client_socket)
                # if word == "wait":
                #     print("\nwait...")
                #     result = self.recv_message(self.client_socket)
                #     print(result)
                #     continue
                if word == "end_game" or not word:
                    print("\nゲーム終了")
                    winner_result = self.recv_message(self.client_socket)
                    print(winner_result)
                    continue  # ゲーム終了時
                
                elif "単語" in word:
                    print(f"\n{word}")
                    start_time = time.time()
                    player_input = input("入力: ")
                    player_time = time.time() - start_time

                    # 入力結果とタイムをサーバーに送信
                    self.send_message(self.client_socket, f"{player_input}, {player_time:.2f}")
                    
                    score_result = self.recv_message(self.client_socket)
                    print(score_result)
                        
        except Exception as e:
            print(f"エラー: {e}")
        finally:
            self.client_socket.close()

    # def start(self):
    #     game = tgf.TypingGame(None, [self.client_socket])
    #     game.start_game()

    #     self.client_socket.close()

# if __name__ == "__main__":
#     client = TypingClinet()
#     client.start()
