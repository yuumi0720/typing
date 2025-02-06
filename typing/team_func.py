import random
import time
import typing_functions as tf
import log_handler as log

class TeamGame:
    def __init__(self, server_socket, client_sockets, score_limit=5):
        self.server_socket = server_socket
        self.client_sockets = client_sockets
        self.score_limit = score_limit
        self.words = []
        self.player_names = []
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


        formatted_teams = ", ".join(
        f"{team}: [{', '.join(members)}]" for team, members in grouped_teams.items()
        )
        self.broadcast(f"\nチーム割り当て: {formatted_teams}")

        input("準備ができたらEnter>>")


    def send_turn_message(self, active_players, message):
        # 対戦中のプレイヤーには単語、それ以外は待機
        for i, player_socket in enumerate(self.client_sockets):
            if i in active_players:
                self.send_message(player_socket, f"単語: {message}")
           
            else:
                self.send_message(player_socket, "wait")

               
    def collect_inputs(self, player_sockets):
        player_times = []
        player_inputs = []

        for player_socket in player_sockets:
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
       
       
    def start_game(self):
        self.broadcast("name")
        for client_socket in self.client_sockets:
            client_name = self.recv_message(client_socket)
            self.player_names.append(client_name)

        self.assign_name(self.player_names)
        

        
        self.words = tf.load_words('text/words.txt')
        

        self.broadcast("ゲーム開始まで2秒...")
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

            team1_socket = self.client_sockets[self.player_names.index(taem1_player)]
            
            team2_socket = self.client_sockets[self.player_names.index(taem2_player)]
            

            
            word = random.choice(self.words)
            self.words.remove(word)

            
            team1_id = self.player_names.index(taem1_player)
            team2_id = self.player_names.index(taem2_player)


            self.send_turn_message(
                [team1_id, team2_id],
                word,
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


        self.broadcast("end_game2")
        # 勝敗の決定
        winner = self.team_scores.index(max(self.team_scores))
        time.sleep(0.5)
        self.broadcast(f"team{winner+1}が勝利しました！")

        
        teams = {
        "team1": [name for name, team in self.teams.items() if team == 1],
        "team2": [name for name, team in self.teams.items() if team == 2]
        }
        team_results = {f"Team {i+1}": score for i, score in enumerate(self.team_scores)}
        winner = f"Team {self.team_scores.index(max(self.team_scores)) + 1}"
        log.save_log("team", self.player_names, team_results, winner, teams)
