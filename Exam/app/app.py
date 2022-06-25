
from flask import Flask, render_template, abort, send_from_directory, request, flash


from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from bleach import clean

app = Flask(__name__)
application = app

app.config.from_pyfile('config.py')
PER_PAGE = 3

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(app, metadata=metadata)

from models import Book, Covers, Genry, Genrys_books
from auth import bp as auth_bp, init_login_manager
from tools import BookFilter

init_login_manager(app)


from books import book_bp
app.register_blueprint(auth_bp)
app.register_blueprint(book_bp)


def search_params():
    return {
        'name_book': request.args.get('name_book'),
        'genrys': request.args.getlist('genrys'),
    }


@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    book_genry = Genrys_books.query.all()
    books = BookFilter().perform(**search_params())
    pagination = books.paginate(page, PER_PAGE)
    books = pagination.items
    genrys = Genry.query.all()
    return render_template('index.html', 
                            books=books, 
                            pagination=pagination,
                            genrys = genrys,
                            book_genry = book_genry,
                            search_params = search_params()
                            )


@app.route('/images/<image_id>')
def image(image_id):
    img = Covers.query.get(image_id)
    if img is None:
        abort(404)
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               img.storage_filename)


