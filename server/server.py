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

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creates the server socket 
server.bind(ADDR)


def broadcast(msg, name):
    # sends the message to all the users

    # msg: the message to be sent
    # name: who sent the message 
    # 
    for person in Persons:
        client = person.client
        try:
            client.send((name +': '+ msg).encode())
        except Exception as e:
            print("[EXCEPTION] ", e)
            break

def handle_client(person):
    # """
    # The function that runs on a new thread for each client

    # person: the client that this thread is responsible for 

    # """
    client = person.client
    addr = person.addr
    person.name = client.recv(SIZE).decode(FORMAT) # first message is always the name
    name = person.name
    print(f"{person.name} has entered the chat ")

    while True:
        try:
            msg = client.recv(SIZE).decode()
            if msg == DISCONNECT_MESSAGE: # if the user quits we delete him from persons before broadcast 
                Persons.remove(person)
                broadcast(f"{name} has left the chat",'')
                print(f"{name} has left the chat" )
                break
            else:
                print(msg)
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
        client, addr = server.accept() # waiting for new connections 
        person = Person(addr, client) # creating new Person object for every new client 
        Persons.append(person)
        print(f"[CONNECTION] {addr} connected to the server at {time.time()}")
        thread = threading.Thread(target = handle_client, args=(person,)) # starts new thread for each client
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

    print("SERVER ERROR")

if __name__ == "__main__":
    print("[STARTING] server is starting...")
    start()

