from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    #datos de usuarios
    id = db.Column(db.Integer, primary_key=True) #las claves primarias son requeridas por SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
