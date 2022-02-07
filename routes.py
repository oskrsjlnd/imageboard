from flask import render_template, request, redirect, session
import re
from app import app
from database import db

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if (request.method == "POST"
        and "username" in request.form
        and "password" in request.form):
        username = request.form["username"]
        password = request.form["password"]
        if db.login(username, password):
            return redirect("/")

    msg = "Wrong username or password"
    return render_template("index.html", msg = msg)

@app.route("/create_acc", methods=["GET", "POST"])
def create_acc():
    if (request.method == "POST"
        and "username" in request.form
        and "email" in request.form
        and "password" in request.form
        and "repeat_pw" in request.form):
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        repeat_pw = request.form["repeat_pw"]
        msg = create_acc_validation(username, email, password, repeat_pw)
        if (msg == "User successfully created"):
            db.new_user(username, password, email)
            return redirect("/")
        else:
            return render_template("create_acc.html", msg = msg)
    else:
        msg = "Fill in all the required fields"
        return render_template("create_acc.html", msg = msg)

@app.route("/log_out")
def log_out():
    session.clear()
    return redirect("/")

def create_acc_validation(username, email, password, repeat_pw):
    msg = "Password must be between 8 and 20 characters\n\
        Passwords must match\n\
        Username must be between 6 and 20 characters\n\
        Email address must be valid"
    if (password != repeat_pw
        or len(username) < 6 or len(username) > 20
        or len(password) < 8 or len(password) > 20
        or not re.match("[^@]+@[^@]+\.[^@]+", email)):
        return msg
    msg = "User succesfully created"
    return msg
