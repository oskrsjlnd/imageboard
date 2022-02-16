from flask import render_template, request, redirect, session
import re
from app import app
from database import db

@app.route("/")
def index():
    return render_template("index.html", msg="")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == "" or password == "":
            return render_template("index.html", msg="Please give username and password")

        if db.login(username, password):
            session["username"] = username
            return redirect("/")
        else:
            return render_template("index.html", msg="Invalid username or password")
    else:
        return render_template("index.html", msg="")

@app.route("/create_acc", methods=["GET", "POST"])
def create_acc():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        repeat_pw = request.form["repeat_pw"]
        if username == "" or email == "" or password == "" or repeat_pw == "":
            return render_template("create_acc.html", msg="Fill in all the required fields")

        if create_acc_validation(username, email, password, repeat_pw):
            if db.new_user(username, password, email):
                return redirect("/")
            else:
                return render_template("create_acc.html", msg="Username already exists")
        else:
            return render_template("create_acc.html", msg="Invalid username, password or email address")
    else:
        return render_template("create_acc.html", msg="")

@app.route("/log_out")
def log_out():
    session.clear()
    return redirect("/")

# @app.route("/my_uploads")
# def my_uploads():
#     return render_template("my_uploads.html")

def create_acc_validation(username, email, password, repeat_pw):
    if (password != repeat_pw
        or len(username) < 6 
        or len(username) > 20
        or len(password) < 8 
        or len(password) > 20
        or not re.match("[^@]+@[^@]+\.[^@]+", email)):
        return False
    return True
