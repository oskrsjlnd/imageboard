from app import app
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

class Repository:
    def __init__(self, app=app):
        self.db = SQLAlchemy(app)
    
    def new_user(self, username, password, email):
        try:
            pw_hash_value = generate_password_hash(password)
            sql = "INSERT INTO users VALUES(DEFAULT, :admin, :password, :username, :email )"
            self.db.session.execute(sql, {"username":username, "password":pw_hash_value, "email":email, "admin":FALSE})
            self.db.session.commit()
        except:
            return False
        return self.login(username, password)
    
    def login(self, username, password):
        sql = "SELECT id, password, admin FROM users WHERE username=:username"
        result = self.db.session.execute(sql, {"username":username})
        user = result.fetchone()
        if not user:
            return False
        if check_password_hash(user.password, password):
            self.db.session["user_id"] = user.id
            return True
        return False
    
    def logout(self):
        del self.db.session["user_id"]

    # def user_id(self):
    #     return self.db.session.get("user_id", 0)


db = Repository()
