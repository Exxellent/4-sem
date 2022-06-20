from flask import Flask, render_template, session, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
application = app

app.config.from_pyfile('config.py')

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(app, metadata=metadata)

from models import Book 
from auth import bp as auth_bp, init_login_manager

init_login_manager(app)

app.register_blueprint(auth_bp)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/books')
def books():
    books = Book.query.all()
    return render_template('books.html', books=books)
