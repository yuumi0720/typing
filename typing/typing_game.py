import argparse
import time
import typing_functions as tf
import typing_server as server
import typing_client as client
import subprocess


#コマンドラインから指定
parser = argparse.ArgumentParser(description="タイピングゲームを選択してね")
parser.add_argument('mode', choices=['one', 'two', 'd1','server', 'client'], help="実行するゲームを選択してね")
args = parser.parse_args()

if args.mode in ['one', 'two', 'd1']:
    if args.mode == 'one':
        tf.time_limit('words.txt')
    elif args.mode == 'two':
        tf.clear_time('words.txt')
    elif args.mode == 'd1':
        tf.practice('d1.txt')
elif args.mode in ['server', 'client']:
    if args.mode == 'server':
        subprocess.Popen(["python3", "typing_server.py"])
        print("サーバーをバックグラウンドで起動しました。")
        time.sleep(0.1)
        client.TypingClient().start()
    else:
        time.sleep(0.1)
        client.TypingClient().start()



