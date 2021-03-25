import socket 
import threading 
from person import Person

# constant values 
PORT = 5050
SERVER = "192.168.1.103"
ADDR = (SERVER, PORT)
HEADER = 32
DISCONNECT_MESSAGE = "quit"

# global variables
Persons = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(person):
    client = person.client
    addr = person.addr
    print(f"[NEW CONNECTION] {addr} CONNECTED")
    person.name = client.recv(HEADER).decode() # first message is always the name

    try:
        while True:
            msg = client.recv(HEADER).decode()
            if msg:
                if msg == DISCONNECT_MESSAGE:
                    print(f"{person.name} has left the chat" )
                    break
                print(f"{person.name}, {addr} said: ", msg)
                client.send("message received".encode())
                
    except ConnectionResetError:
        print(f"{person.name} has left the chat" )

    except Exception as e:
        print("[EXCEPTION] ", e)
    client.close()

def start():
    server.listen(5)
    print(f"[LISTENING] Server listening on {SERVER}")
    while True:
        client, addr = server.accept()
        person = Person(addr, client)
        Persons.append(person)
        thread = threading.Thread(target = handle_client, args=(person, ))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


if __name__ == "__main__":
    print("[STARTING] server is starting...")
    start()

