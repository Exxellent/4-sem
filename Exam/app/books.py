from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db, app
from models import Book, Recives, Genry, Covers
from tools import ImageSaver

book_bp = Blueprint('books', __name__, url_prefix='/books')


@book_bp.route('/<int:book_id>')
def show(book_id):
    book = Book.query.get(book_id)
    image = Covers.query.filter(Covers.id_book == book_id).first()
    return render_template('book/show.html', book=book, image=image)