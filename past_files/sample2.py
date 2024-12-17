import random
import time


# 単語リスト
def load_words(file):
    with open(file, 'r') as f:
        return [line.strip() for line in f]
    
words = load_words('words.txt')

#得点の定義
count = 1
score_clear = 10

print("=== タイピングゲームへようこそ！ ===")
print(f"{score_clear}個の単語をできるだけ早く入力してください。")
input("準備ができたらEnterキーを押してください...")


#ゲーム開始時間
start_time = time.time()

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
