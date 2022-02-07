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
        if db.login_validation(username, password):
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
            return render_template("index.html")
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
    if password != repeat_pw:
        return "Passwords do not match"
    if len(username) < 6 or len(username) > 20:
        return "Username must be between 6 and 20 characters"
    if len(password) < 8 or len(password) > 20:
        return "Password must be between 8 and 20 characters"
    if not re.match("[^@]+@[^@]+\.[^@]+", email):
        return "Invalid email address"
    return "User succesfully created"
    #
