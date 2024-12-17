import random
import time
import typing_functions as tf

class TypingGame:
    def __init__(self, server_socket, client_socket, score_limit=5):
        self.server_socket = server_socket
        self.client_socket = client_socket
        self.score_limit = score_limit
        self.words =""
        self.player_scores = [0, 0]

    def send_massage(self, socket, message):
        socket.sendall(message.encode('utf-8'))

    def recv_massage(self, socket):
        return socket.recv(1024).decode('utf-8').strip()
    
    def start_game(self, player_number=1):

        if player_number == 1:
            mode = input("モードを選択してね easy or hard>> ")
            if mode == "easy":
                self.words = tf.load_words('words.txt')
            elif mode == "hard":
                self.words = tf.load_words('difficult_words.txt')
            self.send_massage(self.client_socket, mode)
        else:
            mode = self.recv_massage(self.server_socket)
            print(f"{mode}が選択されました")
        
        print("ゲーム開始まで2秒...")
        time.sleep(2)
        




        while max(self.player_scores) < self.score_limit:
            
            if player_number == 1:
                word = random.choice(self.words)
                self.words.remove(word)
                self.send_massage(self.client_socket, word)
            else:
                word = self.recv_massage(self.server_socket)

            # time.sleep()
            print(f"単語: {word}")

            # if flag == False:
            #     print(f"単語: {word}")
            #     flag = True
            # else:
            #     print("次の単語まで..")
            #     for i in range(3, -1, -1):
            #         time.sleep(1)
            #         print(f"後{i}秒...")
                
            #     print(f"\n単語: {word}")


            start_time = time.time()
            player_input = input("入力: ").strip()
            player_time = time.time() - start_time
            
            
            if player_number == 1:
                self.send_massage(self.client_socket, f"{player_input},{player_time:.2f}")
                client_response = self.recv_massage(self.client_socket)
                client_input, client_time = client_response.split(",")
                client_time = float(client_time)
            else:
                self.send_massage(self.server_socket, f"{player_input},{player_time:.2f}")
                server_response = self.recv_massage(self.server_socket)
                server_input, server_time = server_response.split(",")
                server_time = float(server_time)



            if player_number == 1:
                server_time = player_time
                if player_input == word and (client_input != word or player_time < client_time):
                    print("nice!")
                    self.player_scores[0] += 1
                elif client_input == word and (player_input != word or client_time < player_time):
                    print("bad..")
                    self.player_scores[1] += 1
                else:
                    print("draw")
            else:
                client_time = player_time
                if player_input == word and (server_input != word or player_time < server_time):
                    print("nice!")
                    self.player_scores[1] += 1
                elif server_input == word and (player_input != word or server_time < player_time):
                    print("bad..")
                    self.player_scores[0] += 1
                else:
                    print("draw")
           

            
            print(f"Player1: {server_time:.2f}秒 - Player2: {client_time:.2f}秒")
            print(f"Player1: {self.player_scores[0]} - Player2: {self.player_scores[1]}\n")


        if self.player_scores[player_number - 1] >= self.score_limit:
            print("あなたの勝ち！")
            if player_number == 1:
                self.send_massage(self.client_socket, "win")
            else:
                oppnent_result = self.recv_massage(self.server_socket)
                if oppnent_result == "win":
                    print("あなたの負け...")
        else:
            print("あなたの負け...")
            if player_number == 1:
                self.send_massage(self.client_socket, "lose")
            else:
                oppnent_result = self.recv_massage(self.server_socket)
                if oppnent_result == "lose":
                    print("あなたの勝ち！")