from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)

@app.route('/')
def main():
    return redirect(url_for("login"))

@app.route('/login', methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        return redirect(url_for("home"))
    else:
        return render_template("login.html")

@app.route("/home")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug = True)
