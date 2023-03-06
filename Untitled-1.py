import socket

HOST = '192.168.2.150'
PORT = 10014

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print("WAITING")
    s.connect((HOST, PORT))
    while True:
        data = s.recv(1024)
        if not data:
            break
        print(data.decode())
