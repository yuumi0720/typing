import random
import time
import threading
import queue

# 単語リスト
def load_words(file):
    with open(file, 'r') as f:
        return [line.strip() for line in f]
    
# 制限時間の関数の定義
def timer_function(time_limit, stop_event):
    time.sleep(time_limit)
    stop_event.set()

# 入力の定義
def input_with_timeout(prompt, timeout, input_queue):
    def get_input():
        user_input = input(prompt)
        input_queue.put(user_input)

    input_thread = threading.Thread(target=get_input)
    input_thread.daemon = True
    input_thread.start()
    input_thread.join(timeout)
    


#制限時間制の関数
def time_limit(file_txt):
    # 初期設定
    score = 0
    time_limit = 15  # 制限時間（秒）

    print("=== タイピングゲームへようこそ！ ===")
    print(f"制限時間: {time_limit}秒")
    print("単語が表示されたら、できるだけ早く入力してください。")
    input("準備ができたらEnterキーを押してください...")

    # ゲーム開始時間
    start_time = time.time()


    #タイマーの設定
    stop_event = threading.Event()
    timer_thread = threading.Thread(target=timer_function, args=(time_limit, stop_event))
    timer_thread.start()


    words = load_words(file_txt)
    input_queue = queue.Queue()

    while not stop_event.is_set():
        current_time = time.time()
        elapsed_time = current_time - start_time
        
        if elapsed_time > time_limit:
            break
        
        # ランダムな単語を選択
        word = random.choice(words)
        words.remove(word)
        
        # 入力が正しいか確認
        while True:
            print(f"単語: {word}")
            input_with_timeout("入力: ", time_limit - elapsed_time, input_queue)
            
            if stop_event.is_set():
                break
            
            if not input_queue.empty():
                user_input = input_queue.get()
                if user_input == word:
                    score += 1
                    print("正解！")
                    break
                else:
                    print("間違い！\n")
            else:
                print("\nタイムアウト")
                break
            
        print(f"現在のスコア: {score}")
        print(f"残り時間: {int(time_limit - (time.time()-start_time))}秒\n")

    # 結果の表示
    print("=== ゲーム終了！ ===")
    print(f"あなたの最終スコアは: {score} 点です。")


#クリアタイム制の関数
def clear_time(file_txt):
     #得点の定義
    count = 1
    score_clear = 20

    print("=== タイピングゲームへようこそ！ ===")
    print(f"{score_clear}個の単語をできるだけ早く入力してください。")
    input("準備ができたらEnterキーを押してください...")


    #ゲーム開始時間
    start_time = time.time()

    words = load_words(file_txt)

    while count <= score_clear:
        word = random.choice(words)
        words.remove(word)
        print(count)
        while True:
            print(f"単語: {word}")
            user_input = input("入力: ")

            #入力判定
            if user_input == word:
                count += 1
                print("正解！\n")
                break
            else:
                print("間違い！\n")

    #時間測定
    end_time = time.time()
    elapsed_time = format(end_time-start_time, '.3f')

    #結果表示
    print("=== ゲーム終了！ ===")
    print(f"{elapsed_time} 秒です。")



def practice(file_txt):
    score = 0
    time_limit = 10

    print("=== タイピングゲームへようこそ！ ===")
    print(f"制限時間: {time_limit}秒")
    print("単語が表示されたら、できるだけ早く入力してください。")
    input("準備ができたらEnterキーを押してください...")

    # ゲーム開始時間
    start_time = time.time()

    #タイマーの設定
    stop_event = threading.Event()
    timer_thread = threading.Thread(target=timer_function, args=(time_limit, stop_event))
    timer_thread.start()

    words = load_words(file_txt)
    input_queue = queue.Queue()

    while not stop_event.is_set():
        current_time = time.time()
        elapsed_time = current_time - start_time
        
        if elapsed_time > time_limit:
            break
        
        # ランダムな単語を選択
        word = random.choice(words)

        # 一行に含まれる単語の数
        word_count = len(word.split())

        
        # 入力が正しいか確認
        
        print(f"単語: {word}")
        input_with_timeout("入力: ", time_limit - elapsed_time, input_queue)

        if stop_event.is_set():
            break

        if not input_queue.empty():
            user_input = input_queue.get()
            if user_input == word:
                score += word_count
                print("正解！")
            else:
                print("間違い！")
        else:
            print("\nタイムアウト")
            
        print(f"現在のスコア: {score}")
        print(f"残り時間: {int(time_limit - (time.time()-start_time))}秒\n")

    # 結果の表示
    print("\n=== ゲーム終了！ ===")
    print(f"あなたの最終スコアは: {score} 点です。")


