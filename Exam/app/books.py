from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
import os
from app import db, app
from models import Book, Recives, Genry, Covers
from tools import ImageSaver

book_bp = Blueprint('books', __name__, url_prefix='/books')


@book_bp.route('/<int:book_id>')
def show(book_id):
    book = Book.query.get(book_id)
    image = Covers.query.filter(Covers.id_book == book_id).first()
    return render_template('book/show.html', book=book, image=image)

@book_bp.route('/<int:book_id>/edit', methods=['GET', 'POST'])
def edit(book_id):
    genrys = Genry.query.all()
    genrys_count = len(genrys)
    book = Book.query.get(book_id)
    return render_template('book/edit.html',genrys=genrys, genrys_count=genrys_count, book=book, year=book.year.strftime('%Y-%m-%d'))


@book_bp.route('/create', methods=['GET', 'POST'])
def create():
    genrys = Genry.query.all()
    genrys_count = len(genrys)
    if request.method == 'POST':
        try:
            book = Book()
            book.name_book = request.form.get('book_name')
            book.short_description = request.form.get('book_short_description')
            book.author = request.form.get('book_author')
            book.publishing_house = request.form.get('book_publishing_house')
            book.year = request.form.get('book_year')
            book.volume = request.form.get('book_volume')

            for id in request.form.getlist('book_genrys'):
                genry = Genry.query.get(id)
                book.genrys.append(genry)

            db.session.add(book)
            db.session.commit()

            f = request.files.get('book_img')
            if f and f.filename:
                ImageSaver(f).save(book.id)

            db.session.commit()

            flash('Книга успешно добавлена.', 'success')
            return redirect(url_for('books.show', book_id=book.id))
        except:
            db.session.rollback()
            flash('При сохранении данных возникла ошибка. Проверьте корректность введённых данных.', 'warning')
    return render_template('book/create.html',genrys=genrys, genrys_count=genrys_count)

@book_bp.route('/<int:book_id>/delete', methods=['GET', 'POST'])
def delete(book_id):
    try:
        book = Book.query.get(book_id)
        image = Covers.query.filter(Covers.id_book == book_id).first()

        if image:
            path_to_img = os.path.join(
                app.config['UPLOAD_FOLDER'], image.storage_filename)

        book.genrys.clear()
        db.session.delete(book)
        db.session.commit()
        if image:
            os.remove(path_to_img)

    except:
        flash('Ошибка при удалении книги.', 'warning')
        return redirect(url_for('index'))

    flash('Книга успешно удалена.', 'success')
    return redirect(url_for('index'))



