from flask import session
from werkzeug.security import generate_password_hash, check_password_hash
from db import db

def new_user(username, password, email):
    try:
        pw_hash_value = generate_password_hash(password)
        sql = """INSERT INTO "user" (username, password, email, admin)
                VALUES (:username, :password, :email, :admin)"""
        db.session.execute(sql, {"username":username, "password":pw_hash_value, "email":email, "admin":'f'})
        db.session.commit()
    except:
        return False
    return login(username, password)

def login(username, password):
    sql = """SELECT id, username, admin, password 
            FROM "user" WHERE username=:username"""
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    if check_password_hash(user[3], password):
        session["user_id"] = user[0]
        session["username"] = user[1]
        session["admin"] = user[2]
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

def create_subject(subject):
    try:
        sql = """INSERT INTO "subject" (name) VALUES (:name)"""
        db.session.execute(sql, {"name":subject})
        db.session.commit()
    except:
        return False
    return True

def subject_exists(subject):
    sql = """SELECT id FROM subject WHERE name=:subject"""
    result = db.session.execute(sql, {"subject":subject}).fetchone()
    if result is not None:
        return True
    return False

def get_random_image():
    sql_details = """SELECT subject_name, name, timezone, encode(data, 'base64')
            FROM "image" ORDER BY RANDOM() LIMIT 1"""
    result = db.session.execute(sql_details)
    data = result.fetchone()

    if data is not None:
        details = {}
        details["subject_name"] = data[0]
        details["title"] = data[1]
        details["time"] = data[2]
        details["image"] = data[3]
        return details
    else:
        return None

def get_user_uploads(user_id):
    sql = """SELECT id, subject_name, name, timezone FROM "image" 
            WHERE user_id=:user_id ORDER BY timezone"""
    result = db.session.execute(sql, {"user_id":user_id})
    data = result.fetchall()
    result.close()

    if data is not None:
        return data
    else:
        return None

# def like_image(user_id, image_id):
#     sql = """INSERT INTO imglike (user_id, image_id)
#             VALUES (:user_id, :image_id)"""
#     try:
#         db.session.execute(sql, {"user_id":user_id, "image_id":image_id})
#         db.session.commit()
#     except:
#         return False
#     return True

# def post_comment(user_id, image_id, content):
#     sql = """INSERT INTO comment"""

# def get_image_stats(image_id):
#     sql = """SELECT"""
 