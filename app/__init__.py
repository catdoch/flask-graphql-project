from flask import Flask
from flask_assets import Environment, Bundle
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template
from flask_login import LoginManager
import os

basedir = os.path.abspath(os.path.dirname(__file__))

# App initialisation
app = Flask(__name__)
app.debug = True

login = LoginManager(app)
login.login_view = 'login'

# Configs
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
# app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Modules
db = SQLAlchemy(app)
