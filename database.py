from flask import session
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
import secrets

def new_user(username, password, email):
    try:
        pw_hash_value = generate_password_hash(password)
        sql = """INSERT INTO "users" (username, password, email, admin)
                VALUES (:username, :password, :email, :admin)"""
        db.session.execute(sql, {"username":username, "password":pw_hash_value, "email":email, "admin":'f'})
        db.session.commit()
    except:
        return False
    return login(username, password)

def login(username, password):
    sql = """SELECT user_id, username, admin, password 
            FROM "users" WHERE username=:username"""
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    if check_password_hash(user[3], password):
        session["user_id"] = user[0]
        session["username"] = user[1]
        session["admin"] = user[2]
        session["csrf_token"] = secrets.token_hex(16)
        return True
    return False

def get_all_users():
    sql = """SELECT user_id, username, admin, email FROM users
            ORDER BY user_id"""
    result = db.session.execute(sql)
    if result is not None:
        data = result.fetchall()
    return data

def is_admin(user_id):
    sql = """SELECT admin FROM users
            WHERE user_id=:user_id"""
    result = db.session.execute(sql, {"user_id": user_id})
    admin_status = result.fetchone()
    return admin_status[0]

def change_admin_status(user_id):
    if is_admin(user_id):
        sql = f"""UPDATE users
                SET admin='f'
                WHERE user_id={user_id}"""
    else:
        sql = f"""UPDATE users 
                SET admin='t' 
                WHERE user_id={user_id}"""
    db.session.execute(sql, {"user_id":user_id})
    db.session.commit()

# todo admin can add and delete subjects
def create_subject(subject):
    try:
        sql = """INSERT INTO "subject" (name) VALUES (:name)"""
        db.session.execute(sql, {"name":subject})
        db.session.commit()
    except:
        return False
    return True

def subject_exists(subject):
    sql = """SELECT subject_id FROM subject WHERE name=:subject"""
    result = db.session.execute(sql, {"subject":subject}).fetchone()
    if result is not None:
        return True
    return False


def upload_image(user_id, subject_name, name, data):
    if not subject_exists(subject_name):
        create_subject(subject_name)
    try:
        sql = """INSERT INTO "image" (user_id, subject_name, name, data, timezone) 
                VALUES (:user_id, :subject_name, :name, :data, NOW())"""
        db.session.execute(sql, {"user_id":user_id, "subject_name":subject_name, "name":name, "data":data})
        db.session.commit()
    except:
        return False
    return True

def delete_image(image_id):
    try:
        sql = """DELETE FROM "image" WHERE image_id=:image_id"""
        db.session.execute(sql, {"image_id":image_id})
        db.session.commit()
    except:
        return False
    return True

def edit_image_title(image_id, new_title):
    try:
        sql = """UPDATE "image"
                SET name=:new_title
                WHERE image_id=:image_id"""
        db.session.execute(sql, {"new_title":new_title, "image_id":image_id})
        db.session.commit()
    except:
        return False
    return True


def get_user_uploads(user_id):
    sql = """SELECT image_id, subject_name, name, timezone FROM "image" 
            WHERE user_id=:user_id 
            ORDER BY timezone"""
    result = db.session.execute(sql, {"user_id":user_id})
    data = result.fetchall()
    result.close()

    if data is not None:
        return data
    else:
        return None


def get_random_image():
    sql = """SELECT subject_name, name, timezone, encode(data, 'base64'), user_id, image_id
                    FROM "image" ORDER BY RANDOM() LIMIT 1"""
    result = db.session.execute(sql)
    data = result.fetchone()

    if data is not None:
        details = {}
        details["subject_name"] = data[0]
        details["title"] = data[1]
        details["time"] = data[2]
        details["image"] = data[3]
        details["user_id"] = data[4]
        details["image_id"] = data[5]
        return details
    else:
        return None

def get_images_by_subject(subject):
    sql = """SELECT image.image_id, encode(data, 'base64'), timezone, COUNT(imglike_id)
            FROM "image"
            LEFT OUTER JOIN "imglike"
            USING (image_id)
            WHERE subject_name=:subject
            GROUP BY image.image_id
            ORDER BY timezone DESC"""
    result = db.session.execute(sql, {"subject":subject})
    data = result.fetchall()
    return data

def get_image(image_id):
    sql = """SELECT subject_name, name, timezone, encode(data, 'base64'), user_id, image_id
            FROM "image" WHERE image_id=:image_id"""
    result = db.session.execute(sql, {"image_id":image_id})
    data = result.fetchone()

    if data is not None:
        details = {}
        details["subject_name"] = data[0]
        details["title"] = data[1]
        details["time"] = data[2]
        details["image"] = data[3]
        details["user_id"] = data[4]
        details["image_id"] = data[5]
        return details
    else:
        return None


def post_like(user_id, image_id):
    if liked(user_id, image_id):
        return False
    sql = """INSERT INTO "imglike" (user_id, image_id)
            VALUES (:user_id, :image_id)"""
    try:
        db.session.execute(sql, {"user_id":user_id, "image_id":image_id})
        db.session.commit()
    except:
        return False
    return True

def get_likes(image_id):
    sql = """SELECT COUNT(*) FROM "imglike"
            WHERE image_id=:image_id"""
    result = db.session.execute(sql, {"image_id":image_id})
    data = result.fetchone()
    if data is not None:
        return data[0]
    return 0

def liked(user_id, image_id):
    sql = """SELECT * FROM "imglike"
            WHERE image_id=:image_id
            AND user_id=:user_id"""
    result = db.session.execute(sql, {"image_id":image_id, "user_id":user_id})
    data = result.fetchone()
    if data is None:
        return False
    return True

def post_comment(user_id, image_id, content):
    try:
        sql = """INSERT INTO "comment" (user_id, image_id, content, time)
                VALUES (:user_id, :image_id, :content, NOW())"""
        db.session.execute(sql, {"user_id":user_id, "image_id":image_id, "content":content})
        db.session.commit()
    except:
        return False
    return True

def get_comments(image_id):
    sql = """SELECT comment_id, username, content, time, users.user_id
            FROM "comment" 
            LEFT OUTER JOIN "users"
            ON comment.user_id=users.user_id
            WHERE image_id=:image_id
            ORDER BY time DESC"""
    result = db.session.execute(sql, {"image_id":image_id})
    data = result.fetchall()
    return data

def delete_comment(comment_id):
    try:
        sql = """DELETE FROM comment WHERE comment_id=:comment_id"""
        db.session.execute(sql, {"comment_id":comment_id})
        db.session.commit()
    except:
        return False
    return True

