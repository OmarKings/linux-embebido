import socket

HOST = '127.0.0.1' #Localhost
PORT = 3333


with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.connect((HOST,PORT))
    s.sendall(b"Programa a recibir, recibido")
    data = s.recv(1024)

print(f"Recieved {data.decode()}")