from flask import render_template, request, redirect, session
import re
from app import app
import database

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

        if database.login(username, password):
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
            if database.new_user(username, password, email):
                return redirect("/")
            else:
                return render_template("create_acc.html", msg="Username or email already exists")
        else:
            return render_template("create_acc.html", msg="Invalid username, password or email address")
    else:
        return render_template("create_acc.html", msg="")

@app.route("/log_out")
def log_out():
    session.clear()
    return redirect("/")

@app.route("/upload")
def upload():
    return render_template("upload.html")

@app.route("/random_image")
def random_image():
    img = database.get_random_image()
    if img is not None:
        return render_template("random_image.html", image=img["image"])
    else:
        return render_template("random_image.html", msg="Image database empty")
@app.route("/send_image", methods=["POST"])
def send_image():
    image = request.files["file"]
    title = request.form["name"]
    subject_name = request.form["subject"]
    user_id = session["user_id"]
    image_data = image.read()
    image_file_name = image.filename

    if image_upload_validation(image_file_name, title, subject_name, image_data):
        if database.upload_image(user_id, subject_name, title, image_data):
            return render_template("upload.html", msg="Image uploaded successfully")
        else:
            return render_template("upload.html", msg="Error while uploading image to database")
    else:
        return render_template("upload.html", msg="Check image requirements")


def image_upload_validation(file_name, title, subject, image_data):
    if (not file_name.endswith(".jpg")
        or len(title) > 15
        or len(subject) > 15
        or len(image_data) > 2000*1024):
        return False
    return True

def create_acc_validation(username, email, password, repeat_pw):
    if (password != repeat_pw
        or len(username) < 6 
        or len(username) > 20
        or len(password) < 8 
        or len(password) > 20
        or not re.match("[^@]+@[^@]+\.[^@]+", email)):
        return False
    return True
