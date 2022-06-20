import os
import sqlalchemy as sa
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from flask import url_for
from app import db

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(25), unique=True, nullable=False)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    middle_name = db.Column(db.String(25))
    role_id = db.Column(db.Integer, unique=True)
    password_hash = db.Column(db.String(256), nullable=False)
    

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def full_name(self):
        return ' '.join([self.last_name, self.first_name, self.middle_name or ''])

    def __repr__(self):
        return '<User %r>' % self.login

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    name_book = db.Column(db.String(255), nullable=False)
    short_description = db.Column(db.String(25), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    publishing_house = db.Column(db.String(25), nullable=False)
    author = db.Column(db.String, nullable=False)
    volume = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Book %r>' % self.name_book
    

