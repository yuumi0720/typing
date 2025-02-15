
import itertools
import asyncio
import time
import vs_func as vs
import log_handler as log


class LeagueGame:
    def __init__(self, server_socket, client_sockets):
        self.server_socket = server_socket
        self.client_sockets = client_sockets
        self.players = [{"name": "", "win": 0}for _ in client_sockets]
        self.rounds = [] #ラウンドごとの試合スケジュール

    def send_message(self, socket, message):
        try:
            socket.sendall(message.encode('utf-8'))
        except BrokenPipeError:
            print("クライアントが切断されました。")

    def recv_message(self, socket):

        try:
            return socket.recv(1024).decode('utf-8').strip()
        except Exception as e:
            print(f"受信中にエラー: {e}")
            return ""
    
    def broadcast(self, message):
        for client_socket in self.client_sockets:
            self.send_message(client_socket, message)


    def show_results(self):
        results = "\n現在の成績"
        for plyaer in self.players:
            results += f"\n{plyaer['name']} : {plyaer['win']}勝"

        self.broadcast(results)
    
    def generate_rounds(self):
        """試合スケジュールをラウンドごとに生成"""
        all_matches = list(itertools.combinations(range(len(self.players)), 2))
        rounds = []

        while all_matches:
            current_round = []
            used_plyaers = set()

            for match in all_matches[:]:
                if match[0] not in used_plyaers and match[1] not in used_plyaers:
                    current_round.append(match)
                    used_plyaers.update(match)
                    all_matches.remove(match)

            rounds.append(current_round)

        self.rounds = rounds



    async def play_match(self, player1, player2):
        player_names = [player1["name"], player2["name"]]
        
        game = vs.TypingGame(self.server_socket, [player1["socket"], player2["socket"]], "end_game1", player_names)
        try:
            await asyncio.to_thread(game.start_game)
        except Exception as e:
            print(f"試合中にエラー: {e}")

        scores = game.player_scores
        if scores[0] > scores[1]:
            player1["win"] += 1
        else:
            player2["win"] += 1


    async def sudden_death(self, tied_players):
        self.broadcast("サドンデス突入!!!")

        tied_sockets = [player["socket"] for player in tied_players]
        tied_names = [player["name"] for player in tied_players]

        name_message = " vs ".join(tied_names)
       
        self.broadcast(name_message)
        time.sleep(0.2)
        input("準備ができたらEnter>>")
        game = vs.TypingGame(self.server_socket, tied_sockets, "end_game1", tied_names)

        try:
            await asyncio.to_thread(game.start_game)
        except Exception as e:
            print(f"試合中にエラー: {e}")

        scores = game.player_scores
        winner_idx = scores.index(max(scores))
        return tied_players[winner_idx]
    

    async def start_league(self):
        #名前の設定
        self.broadcast("name")
        for i, client_socket in enumerate(self.client_sockets):
            self.players[i]["name"] = self.recv_message(client_socket)
            self.players[i]["socket"] = client_socket


        #試合の組み合わせ
        self.generate_rounds()

        #試合開始
        for round_idx, current_round in enumerate(self.rounds):
            current_matches = []
            #対戦相手を表示
            for player1_idx, player2_idx in current_round:
                player1 = self.players[player1_idx]
                player2 = self.players[player2_idx]
                
                self.send_message(player1["socket"], f"\n対戦: {player1['name']} vs {player2['name']}")
                self.send_message(player2["socket"], f"\n対戦: {player1['name']} vs {player2['name']}")
                
            time.sleep(0.2)
            input("準備ができたらEnter>>")
            #試合を非同期で開始
            for player1_idx, player2_idx in current_round:
                player1 = self.players[player1_idx]
                player2 = self.players[player2_idx]
                current_matches.append(self.play_match(player1, player2))
            
            try:
                results = await asyncio.gather(*current_matches, return_exceptions=True)
                for result in results:
                    if isinstance(result, Exception):
                        print(f"試合中にエラー: {result}")
            except Exception as e:
                print(f"ラウンド{round_idx+1}にエラー: {e}")

            self.show_results()

        #優勝者の判定
        max_wins = max(player["win"] for player in self.players)
        potential_winners = []
        for player in self.players:
            if player["win"] == max_wins:
                potential_winners.append(player)

        if len(potential_winners) == 1:
            self.broadcast("end_game2")
            winner = potential_winners[0]
            time.sleep(0.3)
            self.broadcast(f"優勝者{winner['name']}({winner['win']}勝)")
        else:
            time.sleep(0.3)
            sudden_death_winner = await self.sudden_death(potential_winners)
            self.broadcast("end_game2")
            time.sleep(0.3)
            self.broadcast(f"優勝者{sudden_death_winner['name']}({sudden_death_winner['win']}勝)")
        

        player_names = [player["name"] for player in self.players]
        player_results = {player["name"]: player["win"] for player in self.players}
        winner = potential_winners[0]["name"] if len(potential_winners) == 1 else f"サドンデスで{sudden_death_winner['name']}"
        log.save_log("league", player_names, player_results, winner)