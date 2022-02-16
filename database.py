from app import app
from flask import session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

class Repository:
    def __init__(self, app=app):
        self.db = SQLAlchemy(app)
    
    def new_user(self, username, password, email):
        try:
            pw_hash_value = generate_password_hash(password)
            sql = """INSERT INTO users (username, password, email, admin)
                    VALUES (:username, :password, :email, :admin)"""
            self.db.session.execute(sql, {"username":username, "password":pw_hash_value, "email":email, "admin":'f'})
            self.db.session.commit()
        except:
            return False
        return self.login(username, password)
    
    def login(self, username, password):
        sql = """SELECT id, username, admin, password 
                FROM users WHERE username=:username"""
        result = self.db.session.execute(sql, {"username":username})
        user = result.fetchone()
        if not user:
            return False
        if check_password_hash(user[3], password):
            session["user_id"] = user[0]
            session["username"] = user[1]
            session["admin"] = user[2]
            return True
        return False
    
    def logout(self):
        del session["user_id"]
        del session["username"]
        del session["admin"]

db = Repository()
