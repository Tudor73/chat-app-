from flask import Flask, render_template, request, url_for, redirect, session, jsonify
from flask import Blueprint


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
