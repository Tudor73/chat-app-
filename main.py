from flask import Flask, render_template, request, url_for, redirect
from client.client import Client

app = Flask(__name__)

@app.route('/')
def main():
    return redirect(url_for("login"))

@app.route('/login', methods = ["POST", "GET"])
def login():
    global client
    if request.method == "POST":
        name = request.form["name"]
        return redirect(url_for("home"))
    else:
        return render_template("login.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/run", methods = ["GET"])
def send():
    msg = request.args.get("message")
    print(msg)
    return "none"


if __name__ == "__main__":
    app.run(debug = True)
