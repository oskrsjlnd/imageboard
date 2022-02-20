from flask import Flask
from os import urandom

app = Flask(__name__)
app.config['SECRET_KEY'] = urandom(24).hex()
app.config['DEBUG'] = True

import routes
