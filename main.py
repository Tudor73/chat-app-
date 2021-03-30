from flask import Flask, render_template, request, url_for, redirect, session, jsonify
from client.client import Client
from flask_socketio import SocketIO
import time

app = Flask(__name__)
app.secret_key ="secret"
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


messages = []
NAME_KEY = "user"

@socketio.on('message')
def handle_message(msg):
    print(msg)
    socketio.send(msg, broadcast = True)
    

@app.route('/')
def main():
    return redirect(url_for("login"))

@app.route('/login', methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        name = request.form["name"]
        session[NAME_KEY] = name
        return redirect(url_for("home"))
    else:
        if NAME_KEY in session:
            return redirect(url_for("home"))
    return render_template("login.html")

@app.route("/home")
def home():
    if NAME_KEY not in session:
        return redirect(url_for("login"))
    return render_template("home.html")

@app.route("/logout")
def logout():
    session.pop(NAME_KEY, None)
    return redirect(url_for("login"))

@app.route("/run", methods = ["GET"])
def run():
    msg = request.args.get("message")
    print(msg)
    return "none"

@app.route("/get_messages")
def get_messages():
    return jsonify({"messages": messages})

@app.route("/get_name")
def get_name():
    data = {"name": ""}
    if NAME_KEY in session:
        print(session[NAME_KEY])
        data = {"name": session[NAME_KEY]}
    return jsonify(data)    

if __name__ == "__main__":
    # Thread(target=update_messages).start()
    socketio.run(app)