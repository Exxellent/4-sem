from flask import Flask, render_template, abort, send_from_directory
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

from models import Book, Covers, Genry, Recives
from auth import bp as auth_bp, init_login_manager
from books import book_bp

init_login_manager(app)

app.register_blueprint(auth_bp)
app.register_blueprint(book_bp)

@app.route('/')
def index():
    books = Book.query.order_by(Book.year.desc())
    recives = Recives.query.all()
    return render_template('index.html', books=books, recives = recives)

@app.route('/images/<image_id>')
def image(image_id):
    img = Covers.query.get(image_id)
    if img is None:
        abort(404)
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               img.storage_filename)


