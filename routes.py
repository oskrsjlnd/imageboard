from flask import render_template, request, redirect, session, abort
from app import app
import database

@app.route("/")
def index():
    return render_template("index.html", msg="")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        pwd = request.form["pwd"]

        if database.login(username, pwd):
            return redirect("/")
        else:
            return render_template("index.html", msg="Invalid username or password")
    else:
        return render_template("index.html")

@app.route("/create_acc", methods=["GET", "POST"])
def create_acc():
    msg = ""
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["pwd"]

        if database.new_user(username, password, email):
            return redirect("/")
        else:
            msg="Username or email already taken"
    
    return render_template("create_acc.html", msg=msg)

@app.route("/delete_user/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    if "user_id" in session:
        if user_id == session["user_id"] or session["admin"]:
            database.delete_user_by_id(user_id)
            log_out()
            return redirect("/")
    else:
        return render_template("login_error.html")

@app.route("/edit_admin_status/<int:user_id>", methods=["POST"])
def edit_admin_status(user_id):
    if session["admin"]:
        if session["csrf_token"] != request.form["csrf_token"]:
            return abort(403)
        database.change_admin_status(user_id)
        return redirect("/user_list")
    else:
        return render_template("notification.html", msg="You are not authorized")

@app.route("/user_list")
def user_list():
    if session["admin"]:
        user_list = database.get_all_users()
        return render_template("user_list.html", users=user_list)
    else:
        return render_template("notification.html", msg="You don't have authorization to view this page")

@app.route("/log_out")
def log_out():
    session.clear()
    return redirect("/")

@app.route("/my_profile/<int:user_id>")
def my_profile(user_id):
    if "user_id" in session:
        if session["user_id"] == user_id or session["admin"]:
            user = database.get_user_by_id(user_id)
            return render_template("my_profile.html", user=user)
        else:
            return render_template("notification.html", msg="You can only view your own user page")

    else:
        return render_template("login_error.html")            




@app.route("/upload")
def upload():
    return render_template("upload.html")

@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/category/<string:subject>/")
def category(subject):
    subj_images = database.get_images_by_subject(subject)
    return render_template("category.html", data=subj_images, subject=subject)

@app.route("/my_uploads")
def my_uploads():
    if "user_id" in session:
        user_id = session["user_id"]
        upload_list = database.get_user_uploads(user_id)
        return render_template("my_uploads.html", uploads=upload_list)
    else:
        return render_template("login_error.html")

@app.route("/random_image")
def random_image():
    image_data = database.get_random_image()
    comment_data = database.get_comments(image_data["image_id"])
    likes = database.get_likes(image_data["image_id"])
    msg = ""
    if image_data is None:
        msg = "Whoops, 0 images on site!"
    return render_template("random_image.html", image_data=image_data, comment_data=comment_data, likes=likes, msg=msg)

@app.route("/show_image/<int:image_id>")
def show_image(image_id):
    image_data = database.get_image(image_id)
    comment_data = database.get_comments(image_id)
    likes = database.get_likes(image_id)
    msg = ""
    if image_data is None:
        msg = "No image found"
    return render_template("show_image.html", image_data=image_data, comment_data=comment_data, likes=likes, msg=msg)

@app.route("/send_image", methods=["POST"])
def send_image():
    if session["csrf_token"] != request.form["csrf_token"]:
            return abort(403)
    image = request.files["fileInput"]
    title = request.form["title"]
    subject_name = request.form["subject"]
    user_id = session["user_id"]
    image_data = image.read()

    if len(image_data) > 2000*1024:
        msg = "Maximum file size is 2MB"
    elif database.upload_image(user_id, subject_name, title, image_data):
        msg = "Image uploaded successfully"
    else:
        msg = "Error while uploading image to database"
    return render_template("upload.html", msg=msg)

@app.route("/delete_image/<int:user_id>/<int:image_id>", methods=["POST"])
def delete_image(image_id, user_id):
    if "user_id" in session:
        if session["csrf_token"] != request.form["csrf_token"]:
            return abort(403)

        if session["user_id"] == user_id:
            database.delete_image(image_id)
            msg = "Image successfully deleted"
        else:
            msg = "You can only delete your own images"
        return render_template("notification.html", msg=msg)
    else:
        return render_template("login_error.html")

@app.route("/edit_image_title/<int:user_id>/<int:image_id>", methods=["POST"])
def edit_image_title(image_id, user_id):
    if "user_id" in session:
        if session["csrf_token"] != request.form["csrf_token"]:
            return abort(403)
        if session["user_id"] == user_id or session["admin"]:
            new_title = request.form["new_title"]
            database.edit_image_title(image_id, new_title)
            return redirect(f"/show_image/{image_id}")
        else:
            return render_template("notification.html", msg="You can only edit titles of your images")
    else:
        return render_template("login_error.html")
            

@app.route("/like_image/<int:image_id>", methods=["POST"])
def like_image(image_id):
    if "user_id" in session:
        if session["csrf_token"] != request.form["csrf_token"]:
            return abort(403)
        user_id = session["user_id"]
        database.post_like(user_id, image_id)
        return redirect(f"/show_image/{image_id}")
    else:
        return render_template("login_error.html")


@app.route("/post_comment/<int:image_id>", methods=["POST"])
def post_comment(image_id):
    if "user_id" in session:
        if session["csrf_token"] != request.form["csrf_token"]:
            return abort(403)
        user_id = session["user_id"]
        content = request.form["comment"]
        database.post_comment(user_id, image_id, content)
        return redirect(f"/show_image/{image_id}")
    else:
        return render_template("login_error.html")

@app.route("/delete_comment/<int:image_id>/<int:user_id>/<int:comment_id>", methods=["POST"])
def delete_comment(comment_id, image_id, user_id):
    if "user_id" in session:
        if session["csrf_token"] != request.form["csrf_token"]:
            return abort(403)

        if user_id == session["user_id"] or session["admin"]:
            database.delete_comment(comment_id)
            return redirect(f"/show_image/{image_id}")

        else:
            return render_template("notification.html", msg="You can only delete your own posts")
