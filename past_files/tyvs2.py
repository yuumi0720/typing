import threading
import random
import time
import socket
import typing_functions as tf

class TypingGame:
    def __init__(self, words_file):
        self.words = tf.load_words(words_file)
        self.score1 = 0
        self.score2 = 0
        self.current_word = ""
        self.lock = threading.Lock()

    def start_game(self, player, conn):
        score_limit = 10
        while self.score1 < score_limit and self.score2 < score_limit:
            with self.lock:
                if self.current_word == "":
                    self.current_word = random.choice(self.words)
                print(f"送信する単語: {self.current_word}")  # デバッグメッセージ
                try:
                    conn.sendall(f"単語: {self.current_word}\n".encode('utf-8'))
                except BrokenPipeError:
                    print("クライアントが切断されました。")
                    return
                except Exception as e:
                    print(f"エラー（単語送信中）: {e}")
                    return

            start_time = time.time()
            try:
                print(f"プレイヤー{player}のデータを待機中...")  # デバッグメッセージ
                data = conn.recv(1024).decode('utf-8').strip()
                if not data:
                    print("クライアントからデータが受信されませんでした。接続を閉じます。")
                    return
                print(f"受信データ (プレイヤー{player}): {data}")
            except Exception as e:
                print(f"エラー (データ受信中): {e}")
                return
            end_time = time.time()
            elapsed_time = end_time - start_time

            with self.lock:
                if data == self.current_word:
                    if player == 1:
                        self.score1 += 1
                    else:
                        self.score2 += 1
                    print(f"Player {player} 正解！ ({elapsed_time:.2f}秒)")
                else:
                    print(f"Player {player} 間違い！ ({elapsed_time:.2f}秒)")

                self.current_word = ""

            try:
                conn.sendall(f"スコア: Player 1: {self.score1} - Player 2: {self.score2}\n".encode('utf-8'))
            except Exception as e:
                print(f"エラー (スコア送信中): {e}")
                return

        with self.lock:
            try:
                if self.score1 >= 10:
                    conn.sendall("ゲーム終了! Player 1 勝ち!\n".encode('utf-8'))
                elif self.score2 >= 10:
                    conn.sendall("ゲーム終了! Player 2 勝ち!\n".encode('utf-8'))
                else:
                    conn.sendall("ゲーム終了!\n".encode('utf-8'))
            except Exception as e:
                print(f"エラー (ゲーム終了メッセージ送信中): {e}")

def handle_client(conn, addr, game, player, is_server_client=False):
    print(f"接続: {addr}")
    try:
        message = "ゲームが数秒後に開始します...\n"
        conn.sendall(message.encode('utf-8'))
        if is_server_client:
            print(message)
        print(f"プレイヤー{player}に開始メッセージを送信しました")
        time.sleep(3)
        game.start_game(player, conn)
    except BrokenPipeError:
        print("クライアントが切断されました。")
    except Exception as e:
        print(f"エラー: {e}")
    finally:
        conn.close()
        print(f"接続を閉じました: {addr}")

def start_server(port=65432):
    host = '0.0.0.0'
    game = TypingGame('words.txt')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"サーバーが起動しました。ポート {port} で接続を待っています...")

        # クライアント2の接続を待つ
        conn2, addr2 = s.accept()
        print(f"プレイヤー2が接続しました: {addr2}")

        # クライアント2の処理をするスレッドを作成
        thread2 = threading.Thread(target=handle_client, args=(conn2, addr2, game, 2))
        thread2.start()

        # サーバーがプレイヤー1として接続
        time.sleep(1)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s1:
            s1.connect(('127.0.0.1', port))
            print("サーバーがプレイヤー1として接続しました。")
            handle_client(s1, ('127.0.0.1', port), game, 1, is_server_client=True)

        thread2.join()

def start_client():
    host = '127.0.0.1'
    port = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        print("サーバーに接続しました。")

        while True:
            print("ループの先頭")  # デバッグメッセージ
            try:
                print("データを受信中...")  # デバッグメッセージ
                data = s.recv(1024).decode('utf-8')
                if not data:
                    print("データが受信されませんでした。接続を閉じます。")
                    break

                print(f"受信データ: {data}")

                if "ゲーム終了" in data:
                    break

                user_input = input("入力: ")
                s.sendall(user_input.encode('utf-8'))
            except BrokenPipeError:
                print("サーバーが切断されました。")
                break
            except Exception as e:
                print(f"error: {e}")
                break
