
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import sys
sys.path.append("../")
from app import app
import os


file_path = os.path.abspath(os.getcwd())+"\data/site.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), nullable = False)
    last_name = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(50), nullable = False)
    phone_number = db.Column(db.String(11), nullable = False)
    age = db.Column(db.Integer)

    def __repr__(self):
        return f"User('{self.name}','{self.last_name}')"

    def add(self):
        db.session.add(self)
        db.session.commit()