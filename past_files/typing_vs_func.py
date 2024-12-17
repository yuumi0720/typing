import socket
import threading
import random
import time
import typing_functions as tf

# サーバークラス
class TypingServer:
    def __init__(self, host='0.0.0.0', port=65432):
        self.server_address = (host, port)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(self.server_address)
        self.server_socket.listen(1)
        self.words = tf.load_words('words.txt')
        self.buffer_size = 1024
        print(f"サーバーが起動しました。ポート {port} で接続を待っています...")

    def handle_client(self, client_socket):
        while True:
            try:
                word = random.choice(self.words)
                print(f"送信する単語: {word}")
                client_socket.sendall(word.encode('utf-8'))
                data = client_socket.recv(self.buffer_size).decode('utf-8').strip()
                print(f"!{data}!")
                if not data:
                    print("クライアントが接続を閉じました。")
                    break
                print(f"クライアントから受信: {data}")
            except ConnectionResetError:
                print("クライアントが接続をリセットしました。")
                break
            except Exception as e:
                print(f"エラー: {e}")
                break
        client_socket.close()

    def start(self):
        client_socket, client_address = self.server_socket.accept()
        print(f"クライアントが接続しました: {client_address}")
        self.handle_client(client_socket)

# クライアントクラス
class TypingClient:
    def __init__(self, host='127.0.0.1', port=65432):
        self.server_address = (host, port)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.buffer_size = 1024
        print("クライアントが接続を待っています...")
        time.sleep(2)
        self.client_socket.connect(self.server_address)

        print("サーバーに接続しました。")

    def start(self):
        while True:
            try:
                data = self.client_socket.recv(self.buffer_size).decode('utf-8').strip()
                if not data:
                    print("サーバーが接続を閉じました。")
                    break
                print(f"サーバーから受信: {data}")
                user_input = input("入力: ")
                self.client_socket.sendall(user_input.encode('utf-8'))
            except ConnectionResetError:
                print("サーバーが接続をリセットしました。")
                break
            except Exception as e:
                print(f"エラー: {e}")
                break
        self.client_socket.close()

# サーバーとクライアントを分岐する関数
def start_typing_game(mode):
    if mode == 'server':
        server = TypingServer()
        server.start()
    elif mode == 'client':
        client = TypingClient()
        client.start()

