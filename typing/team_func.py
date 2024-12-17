import random
import time
import typing_functions as tf

class TeamTypingGame:
    def __init__(self, server_socket, client_sockets, score_limit=10):
        self.server_socket = server_socket
        self.client_sockets = client_sockets
        self.score_limit = score_limit
        self.words = []
        self.team_scores = [0, 0] #チーム1とチーム2のスコア 
        self.teams = {}

    def send_message(self, socket, message):
        socket.sendall(message.encode('utf-8'))

    def recv_message(self, socket):
        return socket.recv(1024).decode('utf-8').strip()

    def broadcast(self, message):
        #全プレイヤーにメッセージを送信
        for client_socket in self.client_sockets:
            self.send_message(client_socket, message)

    def assign_name(self, player_names):
        # ランダムのチームを割り当て
        num_players = len(player_names)
        team_assignments = [1] * (num_players // 2) + [2] * (num_players - num_players // 2)
        random.shuffle(team_assignments)
        
        for name, team in zip(player_names, team_assignments):
            self.teams[name] = team


        grouped_teams = {'team1': [], 'team2': []}
        for name, team in self.teams.items():
            if team == 1:
                grouped_teams['team1'].append(name)
            elif team == 2:
                grouped_teams['team2'].append(name)

        print(f"\nチーム割り当て: {grouped_teams}")
        self.broadcast(f"\nチーム割り当て: {grouped_teams}")

    def send_turn_message(self, active_players, message, all_players):
        # 対戦中のプレイヤーには単語、それ以外は待機
        for i, player_socket in enumerate(all_players):
            if i in active_players:
                if player_socket == self.server_socket:
                    print(f"\n単語: {message}")
                else:
                    self.send_message(player_socket, f"単語: {message}")
            else:
                if player_socket == self.server_socket:
                    print("\nwait...")
                else:
                    self.send_message(player_socket, "wait")

               
    def collect_inputs(self, player_sockets):
        player_times = []
        player_inputs = []

        start_time = time.time()

        for player_socket in player_sockets:
            if player_socket == self.server_socket:
                player_input = input("入力: ").strip()
                player_time = time.time() - start_time

            else:
                response = self.recv_message(player_socket)
                player_input, player_time = response.split(',')
                player_time = float(player_time)

            player_inputs.append(player_input)
            player_times.append(float(f"{player_time:.2f}"))
            
        return player_inputs, player_times
    
    
    def send_results_to_clients(self, player_times, team_scores, player_names):
        results = "\ntime :"

        for name, time in zip(player_names, player_times):
            results += f" [{name}] {time:.2f} sec"

        results += "\nscore:"
        for i, score in enumerate(team_scores):
            results += f" team{i+1}: {score}"
    
        self.broadcast(results)
        print(results)
       
       
    def start_game(self):
        player_names = []
        player_name = input("名前を入力>> ")
        player_names.append(player_name)

        for client_socket in self.client_sockets:
            client_name = self.recv_message(client_socket)
            player_names.append(client_name)


        self.assign_name(player_names)
        

        # サーバーがモードを選択し、全員に通知する
        while True:
            mode = input("モードを選択してね easy or hard>> ")
            if mode == "easy":
                self.words = tf.load_words('words.txt')
                break
            elif mode == "hard":
                self.words = tf.load_words('difficult_words.txt')
                break
            
        self.broadcast(mode)
        time.sleep(1)


        self.broadcast("ゲーム開始まで2秒...")
        print("ゲーム開始まで2秒...")
        time.sleep(2)

        current_round = 0
        team1_players = []
        team2_players = []

        for name, team in self.teams.items():
            if team == 1:
                team1_players.append(name)
            elif team == 2:
                team2_players.append(name) 

        
        # ゲーム進行
        while max(self.team_scores) < self.score_limit:
            team1_index = current_round % len(team1_players)
            taem1_player = team1_players[team1_index]

            team2_index = current_round % len(team2_players)
            taem2_player = team2_players[team2_index]

            team1_socket = (
                self.server_socket
                if taem1_player == player_names[0]
                else self.client_sockets[player_names.index(taem1_player) - 1]
            )
            team2_socket = (
                self.server_socket
                if taem2_player == player_names[0]
                else self.client_sockets[player_names.index(taem2_player) - 1]
            )

            
            word = random.choice(self.words)
            self.words.remove(word)

            server_id = 0
            if team1_socket == self.server_socket:
                team1_id = server_id
            else:
                team1_id = player_names.index(taem1_player)

            if team2_socket == self.server_socket:
                team2_id = server_id
            else:
                team2_id = player_names.index(taem2_player)

            all_players = [self.server_socket] + self.client_sockets

            self.send_turn_message(
                [team1_id, team2_id],
                word,
                all_players
            )

            player_inputs, player_times = self.collect_inputs([team1_socket, team2_socket])
            

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
                    self.team_scores[i] += 1

            #結果を表示
            self.send_results_to_clients(player_times, self.team_scores, [taem1_player, taem2_player])

            current_round += 1


        self.broadcast("end")
        # 勝敗の決定
        winner = self.team_scores.index(max(self.team_scores))
       
        print(f"team{winner+1}が勝利しました！")
        self.broadcast(f"team{winner+1}が勝利しました！")
        