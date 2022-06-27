import hashlib
import uuid
import os

from werkzeug.utils import secure_filename
from sqlalchemy.sql import or_

from models import Covers, Book, Genrys_books
from app import db, app


class BookFilter:
    def __init__(self):
        self.query = Book.query
        self.qwerty = Genrys_books.query

    def perform(self, name_book='', genrys='', years='', amount_from='', amount_to='', author=''):
        if name_book != '':
            self.query = self.query.filter(Book.name_book.ilike(f'%{name_book}%'))
        if genrys != []:
            self.qwerty =  self.qwerty.filter(Genrys_books.id_genry.in_(genrys))
            self.query = self.query.join(self.qwerty)
        if years != []:
            self.query = self.query.filter(or_(Book.year.like(f'%{v}%') for v in years))
        if amount_from != '':
            self.query = self.query.filter(Book.volume >= int(amount_from))
        if amount_to != '':
            self.query = self.query.filter(Book.volume <= int(amount_to))
        if author != '':
            self.query = self.query.filter(Book.author.ilike(f'%{author}%'))
        return self.query.order_by(Book.year.desc())


            
class ImageSaver:
    def __init__(self, file):
        self.file = file

    def save(self, book_id):
        self.img = self.__find_by_md5_hash()
        if self.img:
            return self.img
        file_name = secure_filename(self.file.filename)
        self.img = Covers(id = str(uuid.uuid4()), file_name=file_name, mime_type=self.file.mimetype, md5_hash=self.md5_hash, id_book = book_id)
        db.session.add(self.img)
        db.session.commit()
        self.file.save(os.path.join(app.config['UPLOAD_FOLDER'], self.img.storage_filename))
        return self.img
    def __find_by_md5_hash(self):
        self.md5_hash = hashlib.md5(self.file.read()).hexdigest()
        self.file.seek(0)
        return Covers.query.filter(Covers.md5_hash == self.md5_hash).first()
