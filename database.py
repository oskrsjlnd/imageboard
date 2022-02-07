from app import app
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

class Repository:
    def __init__(self, app=app):
        self.db = SQLAlchemy(app)
    
    def new_user(self, username, password, email):
        if self.username_is_duplicate(username):
            return False
        pw_hash_value = generate_password_hash(password)
        sql = "INSERT INTO users VALUES(DEFAULT, :admin, :password, :username, :email )"
        self.db.session.execute(sql, {"username":username, "password":pw_hash_value, "email":email, "admin":FALSE})
        self.db.session.commit()
        return True
    
    def username_is_duplicate(self, username):
        sql = "SELECT username FROM users WHERE username=:username"
        result = self.db.session.execute(sql, {"username":username})
        if result is None:
            return False
        else:
            return True
    
    def login_validation(self, username, password):
        sql = "SELECT admin, username, password FROM users WHERE username=:username"
        result = self.db.session.execute(sql, {"username":username})
        user = result.fetchone()

        if user is not None:
            if check_password_hash(user[2], password):
                return True
        return False

db = Repository()
