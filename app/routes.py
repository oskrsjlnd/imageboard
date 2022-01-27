from flask import render_template, request, redirect, session
import re
from app.__init__ import app
from repositories.database import db

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
        if db.user_validation(username, password):
            return redirect("/")

    msg = "Wrong username or password"
    return render_template("index.html", msg = msg)

@app.route("/register", methods=["GET", "POST"])
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
        error_msg = create_acc_validation(username, email, password, repeat_pw)
        if ( error_msg != None):
            db.new_user()
        else:
            return render_template("register.html", msg = error_msg)
    else:
        error_msg = "Fill in all the required fields"
        return render_template("register.html", msg = error_msg)

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

    return None
