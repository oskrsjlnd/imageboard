from app.__init__ import app as app
from flask_sqlalchemy import SQLAlchemy

class Repository:
    def __init__(self, app=app):
        self.db = SQLAlchemy(app)
        self.db.session.execute
    
    def new_user(self, username, password, email):
        if not self.username_duplicate_check(username):
            return
        query = f"""
        INSERT INTO users(username, password, email)
        VALUES ({username}, {password}, {email})
        """
        self.db.session.execute(query)
    
    def username_duplicate_check(self, username):
        query = f"""
        SELECT EXISTS(
            SELECT *
            FROM users
            WHERE username = {username}
        )
        """
        return self.db.session.execute(query)
    
    def user_validation(self, username, password):
        query = f"""
        SELECT EXISTS(
            SELECT 1
            FROM users
            WHERE username = {username} 
            AND password = {password}
        )
        """
        return self.db.session.execute(query)

db = Repository()
