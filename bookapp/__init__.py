from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_login import LoginManager
import cloudinary
import os

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/bookdb?charset=utf8mb4" % quote('Admin@123')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.secret_key = os.urandom(24)
app.config["PAGE_SIZE"] = 8

login = LoginManager(app)

db = SQLAlchemy(app)

cloudinary.config(cloud_name='dbkmrrnge',
                  api_key='184527239617813',
                  api_secret='5zUrFEQ6ooHMaow-rKVNSQdxZhg')
