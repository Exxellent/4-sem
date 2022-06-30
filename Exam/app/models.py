import os
import sqlalchemy as sa

from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from flask import url_for
from markdown import markdown

from app import db, app
from users_policy import UsersPolicy


class Genrys_books(db.Model):
    __tablename__ = 'genrys_books'
    id = db.Column(db.Integer, primary_key=True),
    id_book = db.Column(db.Integer,db.ForeignKey('books.id'),primary_key=True)
    id_genry = db.Column(db.Integer,db.ForeignKey('genrys.id'),primary_key=True)
    book = db.relationship('Book')
    genry = db.relationship('Genry')

# genrys_books = db.Table('genrys_books',
#                         db.Column('id', db.Integer, primary_key=True),
#                         db.Column('id_book',db.Integer,db.ForeignKey('books.id'),primary_key=True),
#                         db.Column('id_genry',db.Integer,db.ForeignKey('genrys.id'),primary_key=True))

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(25), unique=True, nullable=False)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    middle_name = db.Column(db.String(25))
    role_id = db.Column(db.Integer,  db.ForeignKey('roles.id'), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)


    def check_password(self, password: str):
        return check_password_hash(self.password_hash, password)


    @property
    def full_name(self):
        return ' '.join([self.last_name, self.first_name, self.middle_name or ''])
    @property
    def is_admin(self):
        return app.config.get('ADMIN_ROLE_ID') == self.role_id

    @property
    def is_moderator(self):
        return app.config.get('MODERATOR_ROLE_ID') == self.role_id

    @property
    def is_user(self):
        return app.config.get('USER_ROLE_ID') == self.role_id
    
    def can(self, action, id_book = None):
        user_policy = UsersPolicy(id_book)
        method = getattr(user_policy, action)
        if method is not None: return method()
        else: return False

    def __repr__(self):
        return '<User %r>' % self.login

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    name_book = db.Column(db.String(255), nullable=False)
    short_description = db.Column(db.Text, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    publishing_house = db.Column(db.String(25), nullable=False)
    author = db.Column(db.String, nullable=False)
    volume = db.Column(db.Integer, nullable=False)


    # genrys = db.relationship('Genry', secondary=genrys_books, backref=db.backref('books'), cascade="all, delete")
    genrys_books = db.relationship('Genrys_books', cascade="all, delete")
    recives = db.relationship('Recives', cascade="all, delete")
    covers = db.relationship('Covers', uselist=False, cascade="all, delete")


    @property
    def score(self):
        sum = 0
        recives = Recives.query.filter(self.id == Recives.id_book).all()
        for recive in recives:
            sum += recive.mark
        try:
            return sum / len(self.recives)
        except ZeroDivisionError:
            return 0.0
    
    @property
    def recives_count(self):
        recives = Recives.query.filter(self.id == Recives.id_book).all()
        return len(recives)
    
    @property
    def formatted_description(self):
        return markdown(self.short_description)

    def __repr__(self):
        return '<Book %r>' % self.name_book


class Genry(db.Model):
    __tablename__ = 'genrys'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(25), nullable=False)


class Recives(db.Model):
    __tablename__ = 'book_recives'
    id = db.Column( db.Integer, primary_key=True)
    mark = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text, nullable=False)

    date_added = db.Column(db.DateTime, nullable=False, server_default=sa.sql.func.now())

    id_book = db.Column(db.Integer,db.ForeignKey('books.id'))
    id_users = db.Column(db.Integer,db.ForeignKey('users.id'))


    book = db.relationship('Book')
    user = db.relationship('User')

    @property
    def formatted_text(self):
        return markdown(self.text)



class Covers(db.Model):
    __tablename__ = 'covers_books'

    id = db.Column(db.String(100), primary_key=True)

    file_name = db.Column(db.String(100), nullable=False)
    mime_type = db.Column(db.String(100), nullable=False)

    md5_hash = db.Column(db.String(100), nullable=False, unique=True)

    id_book = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    book = db.relationship('Book')

    @property
    def storage_filename(self):
        _, ext = os.path.splitext(self.file_name)
        return self.id + ext

    @property
    def url(self):
        return url_for('image', image_id=self.id)


