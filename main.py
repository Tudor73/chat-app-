from flask import Flask, render_template, request, url_for, redirect, session, jsonify
from client.client import Client
from threading import Thread
import time

app = Flask(__name__)
app.secret_key = "hello"


messages = []
NAME_KEY = "user"

client = None
@app.route('/')
def main():
    return redirect(url_for("login"))

@app.route('/login', methods = ["POST", "GET"])
def login():
    global client
    if request.method == "POST":
        name = request.form["name"]
        session[NAME_KEY] = name
        client = Client(session[NAME_KEY])
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
    global client 
    if client:
        client.disconnect()

    return redirect(url_for("login"))

@app.route("/run", methods = ["GET"])
def send():
    global client

    msg = request.args.get("message")
    if client:
        client.send_message(msg)
    return "none"

@app.route("/get_messages")
def get_messages():
    return jsonify({"messages": messages})

def update_messages():
    global messages
    global client 
    while True:    
        time.sleep(0.1)
        if not client: continue
        new_messages = client.get_messages()
        messages.extend(new_messages)
        for msg in new_messages:
            print(msg)
            if msg == "quit":
                break

if __name__ == "__main__":
    Thread(target=update_messages).start()
    app.run(debug = True)
