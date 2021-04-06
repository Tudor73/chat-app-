from flask import Flask, render_template, request, url_for, redirect, session, jsonify, flash
from flask import Blueprint
from .database import Database

view = Blueprint("views", __name__, static_folder="static", template_folder="template")

NAME_KEY = "user" # the key used to store the session 

@view.route('/login', methods = ["POST", "GET"])
def login():
    #handles login page 
    if request.method == "POST":
        name = request.form["name"]
        if len(name) >= 2:  
            session[NAME_KEY] = name # on POST we add the user to the session and redirect them to home 
            flash("Login Succesful!")
            return redirect(url_for("views.home"))
        else:
            flash("2Name must be longer than one character")
    else:
        if NAME_KEY in session: # if the user already is logged in we redirect them to the home page
            flash("Already Logged In")
            return redirect(url_for("views.home"))
    return render_template("login.html")


@view.route("/")
@view.route("/home")
def home():
    if NAME_KEY not in session: # if the user is not logged in we redirect them to the login page
        return redirect(url_for("views.login"))
    return render_template("home.html")

@view.route("/logout")
def logout():
    if NAME_KEY in session: # we pop the user from the session and redirect him to the login page
        flash("1You have been logged out","info")
    session.pop(NAME_KEY, None)
    return redirect(url_for("views.login"))


@view.route("/get_messages")
def get_messages():
    # function used to query the database for all the previous messages 
    # and returning them as json 
    db = Database()
    results = db.get_all_messages()
    results = trim_seconds_from_messages(results)
    return jsonify({"messages": results})

@view.route("/get_name")
def get_name():
    # function used to get the name of the user from the session 
    # and returning it as json
    data = {"name": ""}
    if NAME_KEY in session:
        data = {"name": session[NAME_KEY]}
    return jsonify(data)    

def trim_seconds_from_messages(msgs):
    # utility function used to trim the seconds from the message
    messages = []
    for msg in msgs: 
        msg_copy = msg 
        msg_copy["time"] = msg["time"][:16] 
        messages.append(msg_copy)
    return messages

