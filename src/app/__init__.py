from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import sys

current_path = os.getcwd()


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///epl.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy()
db.init_app(app)
from app.models import *
with app.app_context():
	db.create_all()

from app import main
