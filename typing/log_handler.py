from datetime import datetime, timedelta

LOG_FILE = "typing_log.txt"

def save_log(mode, players, results, winner, teams=None):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write("=" * 40 + "\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Mode: {mode}\n")
        f.write(f"Players: {', '.join(players)}\n")
        if mode == "team" and teams:
            f.write("Teams:\n")
            for team, players in teams.items():
                f.write(f"  {team}: {', '.join(players)}\n")

        f.write("Results:\n")
        for player, score in results.items():
            if mode == "league":
                f.write(f"  - {player}: {score} win \n")
            else:
                f.write(f"  - {player}: {score} point \n")
        f.write(f"Winner: {winner}\n")
        f.write("=" * 40 + "\n")


def show_log():
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            logs = f.readlines()
    except FileNotFoundError:
        print("ログファイルが見つかりません。")
        return
    
    modes = ["vs", "team", "league"]
    print("表示したいモードを選択してください:")
    for i, mode in enumerate(modes, start=1):
        print(f"{i}: {mode}")

    try:
        selected_mode = int(input("番号を入力してください: ")) - 1
        if selected_mode < 0 or selected_mode >= len(modes):
            print("無効な番号が選択されました。")
            return
        mode_to_display = modes[selected_mode]
    except ValueError:
        print("無効な入力です。")
        return
    
    display_logs = []
    current_log = []
    include_log = False
    count = 0
    for line in reversed(logs):
        if "========================" in line:
            if current_log and include_log:
                current_log.append(line)
                display_logs.append("".join(reversed(current_log)))
                count += 1
                if count >= 10:
                    break
            current_log = []
            include_log = False
        
        # if line.startswith("Date:"):
        #     log_date = datetime.strptime(line.split(": ", 1)[1].strip(), '%Y-%m-%d %H:%M:%S')
        #     if log_date >= three_days_ago:
        #         include_log = True
        
        if line.startswith("Mode:"):
            log_mode = line.split(": ", 1)[1].strip()
            if log_mode == mode_to_display:
                include_log = True
            else:
                include_log = False

        current_log.append(line)
    
    if current_log and include_log:
        display_logs.append("".join(current_log))
    
    if display_logs:
        print("\n".join(reversed(display_logs)))
    else:
        print("指定されたモードのログが見つかりません。")

        