import sys
import time
import socket
import typing_functions as tf
import typing_client as client
import log_handler as log
import subprocess


def is_server_running(host='127.0.0.1', port=65432):
    try:
        with socket.create_connection((host, port), timeout=0.5) as sock:
            sock.sendall(b"SERVER_TEST")
            response = sock.recv(1024).decode('utf-8').strip()
            return response == "SERVER_OK"
    except (socket.timeout, ConnectionRefusedError):
        return False
    

def custom_help():
    print("使用方法:")
    print("python3 typing_game.py [mode]\n")
    print("modeを選択:")
    print("vs    : 個人戦")
    print("team  : 団体戦")
    print("league: 総当たり戦")
    print("log   : ログを表示")
    print("skill : スキルチェック(15秒以内に単語を入力)")
    print("speed : スピードチェック(20個の単語を入力)")

    
def main():
    #コマンドラインから指定
   
    args_mode = sys.argv[1:]
    if len(args_mode) == 0:
        custom_help()
        return
   
    if args_mode[0] == 'log':
        log.show_log()
        return
    
    elif args_mode[0] in ['skill', 'speed']:
        if args_mode[0] == 'skill':
            tf.time_limit('text/words.txt')
        elif args_mode[0] == 'speed':
            tf.clear_time('text/words.txt')
    elif args_mode[0] in ['vs', 'team', 'league']:
        if not is_server_running():
            try:
                subprocess.Popen(["python3", "typing_server.py", args_mode[0]])
                time.sleep(1)
            except Exception as e:
                print(f"サーバーの起動に失敗しました: {e}")
                return
        
        try:
            time.sleep(0.5)
            client.TypingClient().start()
        except Exception as e:
            print(f"クライアントの起動に失敗しました: {e}")


if __name__=="__main__":
    main()



