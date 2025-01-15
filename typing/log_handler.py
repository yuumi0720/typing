from datetime import datetime

LOG_FILE = "typing_log.txt"

def save_log(mode, players, results, winner):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write("=========================================\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Mode: {mode}\n")
        f.write(f"Players: {', '.join(players)}\n")
        f.write("Results:\n")
        for player, score in results.items():
            f.write(f"  - {player}: {score} \n")
        f.write(f"Winner: {winner}\n")
        f.write("=========================================\n\n")


def show_log():
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            print(f.read())
    except FileNotFoundError:
        print("ログファイルが見つかりません。")