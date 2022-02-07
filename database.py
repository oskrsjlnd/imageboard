from app import app
from flask import session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

class Repository:
    def __init__(self, app=app):
        self.db = SQLAlchemy(app)
    
    def new_user(self, username, password, email):
        pw_hash_value = generate_password_hash(password)
        try:
            sql = """INSERT INTO users (username, password, email, admin)
                    VALUES (:username, :password, :email, :admin)"""
            self.db.session.execute(sql, {"username":username, "password":pw_hash_value, "email":email, "admin":FALSE})
            self.db.session.commit()
        except:
            return False
        return self.login(username, password)
    
    def login(self, username, password):
        sql = """SELECT id, password, admin 
                FROM users WHERE username=:username"""
        result = self.db.session.execute(sql, {"username":username})
        user = result.fetchone()
        if not user:
            return False
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = user.username
            session["admin"] = user.admin #voi olla ettei toimi vielä
            return True
        return False
    
    def logout(self):
        del session["user_id"]
        del session["username"]
        del session["admin"] #voi olla ettei tämäkään toimi

    # def user_id(self):
    #     return self.db.session.get("user_id", 0)


db = Repository()
