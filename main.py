from flask import session
from flask_socketio import SocketIO
from app import create_app
from app.database import Database

app = create_app()
socketio = SocketIO(app, pingInterval = 3, pingTimeout = 3)

NAME_KEY = "user"
   
@socketio.on('event')
def handle_event(json, methods = ["GET", "POST"]):
    db = Database() 
    db.insert_message(json["name"], json["message"])
    result = db.get_messages_by_name(1,json["name"])
    result = trim_seconds_from_message(result)
    socketio.emit("message response", result)

@socketio.on('disconnect')
def handle_disconnection():
    print("DISCONNECT")
    db = Database()
    msg = {"name": session[NAME_KEY], "message": " has left the chat"}
    db.insert_message(session[NAME_KEY], " has left the chat")
    result = db.get_messages_by_name(1,session[NAME_KEY])
    result = trim_seconds_from_message(result)
    socketio.emit("message response", result)


# utiliy function 
def trim_seconds_from_message(msg):
    msg_copy = msg
    msg_copy["time"] = msg["time"][:16]
    return msg_copy

if __name__ == "__main__":
    # socketio.run(app, host='192.168.1.106', port=5000)
    socketio.run(app)

    # format data on front-end
    # flash messages 
    # finish front-end