import os
from bleach import clean
from sqlalchemy.exc import SQLAlchemyError

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db, app
from models import Book, Recives, Genry, Covers
from tools import ImageSaver
from auth import check_rights

book_bp = Blueprint('books', __name__, url_prefix='/books')


@book_bp.route('/<int:book_id>')
def show(book_id):
    book = Book.query.get(book_id)
    image = Covers.query.filter(Covers.id_book == book_id).first()
    recives = Recives.query.filter(Recives.id_book == book_id).order_by(Recives.date_added.desc())
    curr_recive = None
    if current_user.is_authenticated:
        curr_recive = Recives.query.filter(Recives.id_book == book_id).filter(Recives.id_users == current_user.id).first()
    return render_template('book/show.html', book=book, image=image, curr_recive=curr_recive, recives=recives)


@book_bp.route('/<int:book_id>/recive')
@login_required
def recive(book_id):
    return render_template('book/recive.html', id_book=book_id)


@book_bp.route('/<int:book_id>/recive/create', methods=['POST'])
@login_required
def create_recive(book_id):
    new_recive = Recives()
    new_recive.id_book=book_id
    new_recive.id_users=current_user.id
    new_recive.mark=request.form.get('rating')
    new_recive.text=clean(request.form.get('text'))
    try:
        db.session.add(new_recive)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f'При добавлении данных произошла ошибка. \n{e}', category='danger')
        return redirect(url_for('books.recive', book_id=book_id))

    return redirect(url_for('books.show', book_id=book_id))


@book_bp.route('/<int:book_id>/edit', methods=['GET', 'POST'])
@login_required
@check_rights('update_book')
def edit(book_id):
    genrys = Genry.query.all()
    genrys_count = len(genrys)

    book = Book.query.get(book_id)

    if request.method == 'POST':
        try:
            book.name_book = clean(request.form.get('book_name'))
            book.short_description = clean(request.form.get('book_short_description')) 
            book.author = clean(request.form.get('book_author'))
            book.publishing_house = clean(request.form.get('book_publishing_house'))
            book.year = request.form.get('book_year')
            book.volume = request.form.get('book_volume')
            for genry_id in request.form.getlist('book_genrys'):
                genry = Genry.query.get(genry_id)
                book.genrys.append(genry)

            db.session.add(book)

            db.session.commit()

            flash('Книга успешно обновлена.', 'success')
            return redirect(url_for('index'))
        except:
            db.session.rollback()
            flash('При сохранении данных возникла ошибка. Проверьте корректность введённых данных.', 'warning')
    return render_template('book/edit.html',genrys=genrys, genrys_count=genrys_count, book=book, year=book.year.strftime('%Y-%m-%d'))


@book_bp.route('/create', methods=['GET', 'POST'])
@login_required
@check_rights('create_book')
def create():
    genrys = Genry.query.all()
    genrys_count = len(genrys)

    if request.method == 'POST':
        try:
            book = Book()
            book.name_book = clean(request.form.get('book_name'))
            book.short_description = clean(request.form.get('book_short_description')) 
            book.author = clean(request.form.get('book_author'))
            book.publishing_house = clean(request.form.get('book_publishing_house'))
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
@login_required
@check_rights('delete_book')
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



