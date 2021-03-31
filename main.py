from flask import Flask, render_template, request, url_for, redirect, session, jsonify
from flask_socketio import SocketIO
import time
from views import view

app = Flask(__name__)
app.register_blueprint(view, url_prefix= "/")
app.secret_key ="secret"
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


messages = []
NAME_KEY = "user"

@socketio.on('message')
def handle_message(msg):
    messages.append(msg)
    socketio.send(msg, broadcast = True)         

@socketio.on('event')
def handle_event(json):
    socketio.emit("message response", json)
    print(17)

@app.route("/get_messages")
def get_messages():
    return jsonify({"messages": messages})

@app.route("/get_name")
def get_name():
    data = {"name": ""}
    if NAME_KEY in session:
        data = {"name": session[NAME_KEY]}
    return jsonify(data)    

if __name__ == "__main__":
    # Thread(target=update_messages).start()
    socketio.run(app, host='192.168.1.106', port=5000)


    # handle disconnection when clien logs out or closes window
    # higlight the messages sent in client window
    #format message (name message data)
    #fix scrollling 
    # work on front end 
    #responsivenes