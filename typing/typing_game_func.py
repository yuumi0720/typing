import random
import time
import typing_functions as tf

class TypingGame:
    def __init__(self, server_socket, client_sockets, player_names=None):
        self.server_socket = server_socket
        self.client_sockets = client_sockets
        self.score_limit = 2
        self.words = []
        self.player_scores = [0] * (len(client_sockets)) 
        self.player_names = player_names if player_names else []

    def send_message(self, socket, message):
        socket.sendall(message.encode('utf-8'))

    def recv_message(self, socket):
        return socket.recv(1024).decode('utf-8').strip()

    def broadcast(self, message):
        #全プレイヤーにメッセージを送信
        for client_socket in self.client_sockets:
            self.send_message(client_socket, message)
            
    

    def collect_inputs(self):
        #全プレイヤーの入力を集めて、結果を返す
        player_times = []
        player_inputs = []

        # クライアントの入力を受信
        for client_socket in self.client_sockets:
            try:
                client_input, client_time = self.recv_message(client_socket).split(',')
                player_inputs.append(client_input)
                player_times.append(float(client_time))
            except Exception as e:
                print(f"入力待機中にエラー: {e}")
                player_inputs.append("")  # 空の入力として処理
                player_times.append(float('inf'))  # タイムアウト扱い
        
        return player_inputs, player_times

    def send_results_to_clients(self, player_times, player_scores, player_names):
        results = "\ntime :"
        for i in range(len(player_times)):
            if i != 0:
                results += "  -  "
            results += f"[{player_names[i]}] {player_times[i]:.2f}sec"

        results += "\nscore:"
        for i in range(len(player_scores)):
            if i != 0:
                results += "  -  "
            results += f"[{player_names[i]}] {player_scores[i]}"
    
        self.broadcast(results)
        #print(results)
       
       
    def start_game(self):
        #ニックネーム設定
        if not self.player_names:
            self.broadcast("name")
            for client_socket in self.client_sockets:
                client_name = self.recv_message(client_socket)
                self.player_names.append(client_name)

    # サーバーがモードを選択し、全員に通知する

        # モードを選択し、全員に通知する
        # self.send_message(self.client_sockets[0], "mode_select")
        # mode = self.recv_message(self.client_sockets[0])
        # while True:
        #     if mode == "easy":
        self.words = tf.load_words('words.txt')
            #     break
            # elif mode == "hard":
            #     self.words = tf.load_words('difficult_words.txt')
            #     break
            
        self.broadcast("ゲーム開始まで2秒...")
        time.sleep(2)

        # ゲーム進行
        while max(self.player_scores) < self.score_limit:
            word = random.choice(self.words)
            self.words.remove(word)
            self.broadcast(f"\n単語: {word}")

            # 全プレイヤーの入力を集める
            player_inputs, player_times = self.collect_inputs()


            # 正誤判定
            correct_inputs = []
            for i in player_inputs:
                if i == word:
                    correct_inputs.append(True)
                else:
                    correct_inputs.append(False)
            
            #タイム判定
            correct_times = []
            for i, t in zip(correct_inputs, player_times):
                if i:
                    correct_times.append(t)
            if correct_times:
                min_time = min(correct_times)
            else:
                min_time = None

            # スコアを更新
            for i, correct in enumerate(correct_inputs):
                if min_time != None and correct and player_times[i] == min_time:
                    self.player_scores[i] += 1

            #結果を表示
            self.send_results_to_clients(player_times, self.player_scores, self.player_names)

        self.broadcast("end_game")
        # 勝敗の決定
        winner = self.player_scores.index(max(self.player_scores))
        time.sleep(0.1)
        self.broadcast(f"{self.player_names[winner]}が勝利しました！")
        time.sleep(0.4)
       