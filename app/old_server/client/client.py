from socket import AF_INET, socket , SOCK_STREAM
from threading import Lock, Thread


# the client interface 
class Client:
    DISCONNECT_MESSAGE = "quit"
    HEADER = 256
    PORT = 5050
    SERVER = "192.168.1.106"
    ADDR = (SERVER, PORT)
    FORMAT = "utf-8"

    def __init__(self, name):
        self.name = name 
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(self.ADDR)
        self.messages = []
        receive_thread = Thread(target=self.receive_messages)
        receive_thread.start()
        self.send_message(name)
        self.lock = Lock()
    
    def receive_messages(self):
        while True:
            try:
                new_message = self.client_socket.recv(self.HEADER).decode()
                self.lock.acquire()
                self.messages.append(new_message)
                self.lock.release()
            except Exception as e:
                print("[EXCEPION] ",e)
                break

    def send_message(self, msg):
        try:
            self.client_socket.send(bytes(msg, "utf8"))
            if msg == self.DISCONNECT_MESSAGE:
                self.client_socket.close()
        except Exception as e:
            self.client_socket = socket(AF_INET, SOCK_STREAM)
            self.client_socket.connect(self.ADDR)
            print(e)

    def get_messages(self):
        messages_copy = self.messages[:]
        self.lock.acquire()
        self.messages  = []
        self.lock.release()
        return messages_copy

    def disconnect(self):
        self.send_message(self.DISCONNECT_MESSAGE)


