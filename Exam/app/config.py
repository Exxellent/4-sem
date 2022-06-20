import os

SECRET_KEY = 'Renat12345'

SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://std_1682_exam:Renat12345@std-mysql.ist.mospolytech.ru/std_1682_exam'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media', 'images')