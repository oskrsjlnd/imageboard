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
        return render_template("index.html")

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

@app.route("/my_uploads")
def my_uploads():
    if "user_id" in session:
        user_id = session["user_id"]
        upload_list = database.get_user_uploads(user_id)
        return render_template("my_uploads.html", uploads=upload_list)
    else:
        return render_template("login_error.html")


@app.route("/show_image/<int:id>")
def show_image(id):
    image_data = database.get_image(id)
    comment_data = database.get_comments(id)
    if image_data is not None:
        return render_template("show_image.html", image_data=image_data, comment_data=comment_data)
    else:
        return render_template("show_image.html", msg="No image found")

@app.route("/upload")
def upload():
    return render_template("upload.html")

@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/category/<string:subject>/")
def category(subject):
    subj_images = database.get_images_by_subject(subject)
    if len(subj_images) > 0:
        return render_template("category.html", data=subj_images, subj=subject)
    else:
        return render_template("category.html", subject=subject)

@app.route("/random_image")
def random_image():
    data = database.get_random_image()
    if data is not None:
        return render_template("random_image.html", data=data)
    else:
        return render_template("random_image.html", msg="Whoops, 0 images on site")

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

@app.route("/post_comment/<int:image_id>", methods=["POST"])
def post_comment(image_id):
    if "user_id" in session:
        user_id = session["user_id"]
        content = request.form["comment"]
        if database.post_comment(user_id, image_id, content):
            return redirect(f"/show_image/{image_id}")
    else:
        return render_template("login_error.html")

@app.route("/delete_image/<int:user_id>/<int:image_id>")
def delete_image(image_id, user_id):
    if "user_id" in session:
        if session["user_id"] == user_id:
            if database.delete_image(image_id):
                return render_template("notification.html", msg="Image successfully deleted")
        else:
                return render_template("notification.html", msg="You can only delete your own images")
    else:
        return render_template("login_error.html")


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
