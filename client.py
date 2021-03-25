import socket 

DISCONNECT_MESSAGE = "quit"
HEADER = 32
PORT = 5050
SERVER = "192.168.1.103"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    client.send(message)

while True:
    send_msg = input("S: ")
    send(send_msg)
    if send_msg == DISCONNECT_MESSAGE:
        break
    recv_msg = client.recv(HEADER).decode()
    print(recv_msg)

client.close() 

