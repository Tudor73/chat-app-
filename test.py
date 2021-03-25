from client import Client
import time
import threading

msgs = []

c1 = Client("Tudor")
c2 = Client("Gigi")
c3 = Client("ANdi")

time.sleep(1)

c1.send_message("hello")
time.sleep(0.1)
c2.send_message("hi")
time.sleep(0.1)
c3.send_message("salut")
time.sleep(0.1)
c1.send_message("quit")
time.sleep(0.1)
c2.send_message("quit")


def update_messages():
    while True:
        try:       
            time.sleep(0.1)
            messages_to_show = c1.get_messages()
            msgs.extend(messages_to_show)
            for msg in messages_to_show:
                print(msg)
        except Exception as e:
            print("[EXCEPTION] ", e)
            break

threading.Thread(target=update_messages).start()
