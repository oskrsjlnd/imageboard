from flask import Flask
from flask import render_template, request, redirect
import re

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if (request.method == "POST"
    and "username" in request.form
    and "password" in request.form):
        pass
    msg = "Wrong username or password"
    return render_template("login.html", msg = msg)

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

        if password != repeat_pw:
            pass
        if len(username) < 6 or len(username) > 20:
            pass
        if len(password) < 8 or len(password) > 20:
            pass
        if username:
            pass
        if not re.match("[^@]+@[^@]+\.[^@]+", email):
            pass
        return redirect("/")
    else:
        msg = "Fill in all the required fields"
        return render_template("register.html", msg = msg)
