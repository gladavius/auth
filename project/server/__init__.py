# project/server/__init__.py

import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS

app = Flask(__name__)

bcrypt = Bcrypt(app)

from project.server.auth.views import auth_blueprint
app.register_blueprint(auth_blueprint)
