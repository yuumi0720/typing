import argparse
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
    

def main():
    #コマンドラインから指定
    parser = argparse.ArgumentParser(description="タイピングゲームを選択してね")
    parser.add_argument('mode', choices=['one', 'two', 'd1','vs', 'team', 'league', 'log'], help="実行するゲームを選択してね")
    args = parser.parse_args()

    if args.mode == 'log':
        log.show_log()
        return
    
    elif args.mode in ['one', 'two', 'd1']:
        if args.mode == 'one':
            tf.time_limit('words.txt')
        elif args.mode == 'two':
            tf.clear_time('words.txt')
        elif args.mode == 'd1':
            tf.practice('d1.txt')

    elif args.mode in ['vs', 'team', 'league']:
        if not is_server_running():
            try:
                subprocess.Popen(["python3", "typing_server.py", args.mode])
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



