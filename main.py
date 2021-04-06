from flask import session  
from flask_socketio import SocketIO  
from app import create_app
from app.database import Database

app = create_app() # initialize the app with the settings from __init__
socketio = SocketIO(app, pingInterval = 3, pingTimeout = 3) # socketIO initialization 

NAME_KEY = "user" # the key used to store the session 
   
@socketio.on('event') 
    # handles the messages received from clients and sends them back as json 

def handle_event(json, methods = ["GET", "POST"]):
    if len(json["name"]) >= 2 :
        db = Database() 
        db.insert_message(json["name"], json["message"])
        result = db.get_messages_by_name(1,json["name"]) # getting the last message from the database( the one that was just inserted above)
        result = trim_seconds_from_message(result)
        socketio.emit("message response", result) # sending it back to the clients

@socketio.on('disconnect')
def handle_disconnection():

    # handles disconnection from the server 
    print("DISCONNECT")
    db = Database()
    msg = {"name": session[NAME_KEY], "message": " has left the chat"}
    db.insert_message(session[NAME_KEY], " has left the chat") 
    result = db.get_messages_by_name(1,session[NAME_KEY])
    result = trim_seconds_from_message(result)
    socketio.emit("message response", result)


# utiliy function 
def trim_seconds_from_message(msg):
    # function used to trim the seconds from date 
    msg_copy = msg
    msg_copy["time"] = msg["time"][:16]
    return msg_copy

if __name__ == "__main__":
    socketio.run(app, host='192.168.1.106', port=5000)
    # socketio.run(app)
