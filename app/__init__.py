# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import json

app = Flask(__name__)
app.secret_key = '11A1GEg7ez1fzae7gzgeah'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

with open('sshconfig.json', 'r') as config_file:
    ssh_config = json.load(config_file)

from app import routes
