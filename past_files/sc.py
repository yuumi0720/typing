import socket
import server
import client
import argparse


# def is_server_running(host='0.0.0.0', port=8080):
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         s.settimeout(1)
#         try:
#             s.connect((host, port))
#             s.close()
#             return True
#         except ConnectionRefusedError:
#             return False

parser = argparse.ArgumentParser(description='server or client')
parser.add_argument('mode', choices=['server', 'client'], help="server or client")
args = parser.parse_args()

if args.mode == 'client':
    client.InetClient().send()
elif args.mode == 'server':
    server.InetServer()






