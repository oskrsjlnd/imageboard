from flask import Flask
from repositories.database import db
import os

def create_app():
    app = Flask(__name__, static_url_path="//home/g3xskgz/Repositories/sajinboard/app/static", template_folder="//home/g3xskgz/Repositories/sajinboard/app/templates")
    app.config["SECRET_KEY"] = os.urandom(24).hex()
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///keijo"
    return app

app = create_app()