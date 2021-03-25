import socket 
import threading 
from person import Person
import time

# constant values 
PORT = 5050
SERVER = "192.168.1.103"
ADDR = (SERVER, PORT)
SIZE = 256
FORMAT = "utf8"
DISCONNECT_MESSAGE = "quit"

# global variables
Persons = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def broadcast(msg, name):
    for person in Persons:
        client = person.client
        try:
            client.send((name +': '+ msg).encode())
        except Exception as e:
            print("[EXCEPTION] ", e)
            break

def handle_client(person):
    client = person.client
    addr = person.addr
    person.name = client.recv(SIZE).decode(FORMAT) # first message is always the name
    name = person.name
    print(f"{person.name} has entered the chat ")
    while True:
        try:
            msg = client.recv(SIZE).decode()
            if msg == DISCONNECT_MESSAGE:
                Persons.remove(person)
                broadcast(f"{name} has left the chat",'')
                print(f"{name} has left the chat" )
                break
            else:
                broadcast(msg, person.name)
            print(f"{person.name}, {addr} said: ", msg)
            
        except ConnectionResetError:
            Persons.remove(person)
            broadcast(f"{name} has left the chat",'')
            print(f"{name} has left the chat" )
            break

        except Exception as e:
            Persons.remove(person)
            print("[EXCEPTION] ", e)
            break
    
    client.close()

def start():
    server.listen(5)
    print(f"[LISTENING] Server listening on {SERVER}")
    while True:
        client, addr = server.accept()
        person = Person(addr, client)
        Persons.append(person)
        print(f"[CONNECTION] {addr} connected to the server at {time.time()}")
        thread = threading.Thread(target = handle_client, args=(person,))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

    print("SERVER ERROR")

if __name__ == "__main__":
    print("[STARTING] server is starting...")
    start()

