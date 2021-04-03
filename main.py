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
    socketio.emit("message response", json)

@socketio.on('disconnect')
def handle_disconnection():
    print("DISCONNECT")
    db = Database()
    msg = {"name": session[NAME_KEY], "message": " has left the chat"}
    db.insert_message(session[NAME_KEY], " has left the chat")
    socketio.emit("message response", msg)

if __name__ == "__main__":
    # socketio.run(app, host='192.168.1.106', port=5000)
    socketio.run(app)


    # show message date on the screen 
    # flash messages 
    # finish front-end