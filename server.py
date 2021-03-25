import socket 
import threading 

# constant values 
PORT = 5050
SERVER = "192.168.1.103"
ADDR = (SERVER, PORT)
HEADER = 32
DISCONNECT_MESSAGE = "quit"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} CONNECTED")

    try:
        while True:
            msg = conn.recv(HEADER).decode()
            if msg:
                if msg == DISCONNECT_MESSAGE:
                    break
                print(f"Client from {addr} said: ", msg)
                conn.send("message received".encode())
    except Exception as e:
        print("[EXCEPTION] ", e)

    conn.close()

def start():
    server.listen(5)
    print(f"[LISTENING] Server listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target = handle_client, args=(conn,addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


if __name__ == "__main__":
    print("[STARTING] server is starting...")
    start()

