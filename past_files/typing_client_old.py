import socket
import time
import typing_game_func as tgf

class TypingClinet:
    def __init__(self, host='127.0.0.1', port=65432):
        
        self.server_address = (host, port)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(self.server_address)
        print("サーバーに接続しました。")

    def start(self):
        try:
            name = input("名前を入力>> ")
            self.client_socket.sendall(name.encode('utf-8'))
            
            mode = self.client_socket.recv(1024).decode('utf-8').strip()
            print(f"サーバーが{mode}モードを選択しました")

            start = self.client_socket.recv(1024).decode('utf-8').strip()
            print(start)
            
            while True:
                # サーバーから単語を受け取る
                word = self.client_socket.recv(1024).decode('utf-8').strip()
                if word == "end":
                    break  # ゲーム終了時

                print(f"\n単語: {word}")
                start_time = time.time()
                player_input = input("入力: ").strip()
                player_time = time.time() - start_time

                # 入力結果とタイムをサーバーに送信
                self.client_socket.sendall(f"{player_input}, {player_time:.2f}".encode('utf-8'))
                
                # サーバーから結果を受け取る
                result = self.client_socket.recv(1024).decode('utf-8')
                print(result)

            result = self.client_socket.recv(1024).decode('utf-8').strip()
            print(result)

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