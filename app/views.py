from flask import Flask, render_template, request, url_for, redirect, session, jsonify
from flask import Blueprint
from .database import Database

view = Blueprint("views", __name__, static_folder="static", template_folder="template")

NAME_KEY = "user"


@view.route('/login', methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        name = request.form["name"]  
        session[NAME_KEY] = name
        return redirect(url_for("views.home"))
    else:
        if NAME_KEY in session:
            return redirect(url_for("views.home"))
    return render_template("login.html")


@view.route("/")
@view.route("/home")
def home():
    if NAME_KEY not in session:
        return redirect(url_for("views.login"))
    return render_template("home.html")

@view.route("/logout")
def logout():
    session.pop(NAME_KEY, None)
    return redirect(url_for("views.login"))


@view.route("/get_messages")
def get_messages():
    db = Database()
    results = db.get_all_messages()
    results = trim_seconds_from_messages(results)
    return jsonify({"messages": results})

@view.route("/get_name")
def get_name():
    data = {"name": ""}
    if NAME_KEY in session:
        data = {"name": session[NAME_KEY]}
    return jsonify(data)    



def trim_seconds_from_messages(msgs):
    messages = []
    for msg in msgs: 
        msg_copy = msg 
        msg_copy["time"] = msg["time"][:16] 
        messages.append(msg_copy)
    return messages

