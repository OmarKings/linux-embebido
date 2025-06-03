import socket
from time import sleep

HOST = '127.0.0.1' #Localhost
PORT = 3333

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s. bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    while conn:
        data =conn.recv(1024)
        print(f"{data.decode}")
        sleep(5)
        if not data:
            break
        conn.sendall(data)


