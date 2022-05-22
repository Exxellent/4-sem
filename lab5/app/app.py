from flask import Flask, render_template, session, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from mysql_db import MySQL
import mysql.connector as connector

app = Flask(__name__)
application = app

app.config.from_pyfile('config.py')

mysql = MySQL(app)

CREATE_PARAMS = ['login', 'password', 'first_name', 'last_name', 'middle_name', 'role_id']

UPDATE_PARAMS = [ 'first_name', 'last_name', 'middle_name', 'role_id']

from auth import init_login_manager, bp as auth_bp, check_rights
from visits import bp as visits_bp

init_login_manager(app)
app.register_blueprint(auth_bp)
app.register_blueprint(visits_bp)

@app.before_request
def log_visit_info():
    if request.endpoint == 'static' or request.args.get('download_csv'):
        return None

    user_id = getattr(current_user, 'id', None)
    query = 'INSERT INTO visit_logs (user_id, path) VALUES (%s, %s);'
    with mysql.connection.cursor(named_tuple=True) as cursor:
        try:
            cursor.execute(query,(user_id, request.path))
            mysql.connection.commit()
        except:
            pass


def request_params(params_list):
    params = {}

    for param_name in params_list:
        params[param_name] = request.form.get(param_name) or None

    return params


def load_roles():
    with mysql.connection.cursor(named_tuple=True) as cursor:
        cursor.execute('SELECT id, name FROM roles;')
        roles = cursor.fetchall()
    return roles


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/users')
def users():

    with mysql.connection.cursor(named_tuple=True) as cursor:
        cursor.execute(
            'SELECT users.*, roles.name AS role_name FROM users LEFT JOIN roles ON users.role_id = roles.id;'
            )
        users = cursor.fetchall()
        
    return render_template('users/index.html', users=users)


@app.route('/users/new')
@login_required
@check_rights('create')
def new():
    dict = {'login': None, 'password': None, 'first_name': None, 'middle_name': None, 'last_name': None}
    return render_template('users/new.html', user = {}, error = dict, roles=load_roles())

@app.route('/users/create', methods=['POST'])
@login_required
@check_rights('create')
def create():
    params = request_params(CREATE_PARAMS)
    params['role_id'] = int(params['role_id']) if params['role_id'] else None
    error = check(params)
    if error['login'] is not None or error['password'] is not None or error['first_name'] is not None or error['last_name'] is not None:
        return render_template('users/new.html', error=error, user=params, roles=load_roles())
    with mysql.connection.cursor(named_tuple=True) as cursor:
        try:
            cursor.execute(
                ('INSERT INTO users (login, password_hash, last_name, first_name, middle_name, role_id)'
                 'VALUES (%(login)s, SHA2(%(password)s, 256), %(last_name)s, %(first_name)s, %(middle_name)s, %(role_id)s);'),
                params
            )
            mysql.connection.commit()
        except connector.Error:
            flash('Введены некорректные данные. Ошибка сохранения', 'danger')
            return render_template('users/new.html', user=params, error=error ,roles=load_roles())
    flash(f"Пользователь {params.get('login')} был успешно создан!", 'success')
    return redirect(url_for('users'))


@app.route('/users/<int:user_id>')
@login_required
@check_rights('show')
def show(user_id):
    with mysql.connection.cursor(named_tuple=True) as cursor:
        cursor.execute('SELECT * FROM users WHERE id=%s;', (user_id,))
        user = cursor.fetchone()
    return render_template('users/show.html', user=user, )


@app.route('/users/<int:user_id>/edit')
@login_required
@check_rights('update')
def edit(user_id):
    with mysql.connection.cursor(named_tuple=True) as cursor:
        cursor.execute('SELECT * FROM users WHERE id=%s;', (user_id,))
        user = cursor.fetchone()
    return render_template('users/edit.html', user=user, roles=load_roles())


@app.route('/users/<int:user_id>/update', methods=['POST'])
@login_required
@check_rights('update')
def update(user_id):
    params = request_params(UPDATE_PARAMS)
    params['role_id'] = int(params['role_id']) if params['role_id'] else None
    params['id'] = user_id
    with mysql.connection.cursor(named_tuple=True) as cursor:
        try:
            cursor.execute(
                ('UPDATE users SET last_name=%(last_name)s, first_name=%(first_name)s, middle_name=%(middle_name)s, role_id=%(role_id)s,'
                 'middle_name=%(middle_name)s, role_id=%(role_id)s WHERE id=%(id)s;'), params)
            mysql.connection.commit()
        except connector.Error:
            flash('Введены некорректные данные. Ошибка сохранения', 'danger')
            return render_template('users/edit.html', user=params, roles=load_roles())
    flash("Пользователь был успешно обновлен!", 'success')
    return redirect(url_for('show', user_id=user_id))


@app.route('/users/<int:user_id>/delete', methods=['GET','POST'])
@login_required
@check_rights('delete')
def delete(user_id):
    with mysql.connection.cursor(named_tuple=True) as cursor:
        try:
            cursor.execute(
                ('DELETE FROM users WHERE id=%s'), (user_id, ))
            mysql.connection.commit()
        except connector.Error:
            flash('Не удалось удалить пользователя', 'danger')
            return redirect(url_for('users'))
    flash(f'''Пользователь {user_id} был успешно удален!''', 'success')
    return redirect(url_for('users'))




@app.route('/change', methods=['GET','POST'])
def change():
    error = None
    if request.method == "POST":
        password = request.form.get('password')
        confpassword = request.form.get('confirmpassword')
        last_name = request.form.get('last_name')
        update_list = ['password', 'login', 'last_name']
        params = request_params(update_list)
        with mysql.connection.cursor(named_tuple=True) as cursor:
                cursor.execute(
                    ('SELECT * FROM users WHERE login=%(login)s AND last_name=%(last_name)s;'), params)
                db_user = cursor.fetchone()
        if db_user:
            if password != confpassword:
                error = "Пароль должны быть одинаковыми"
                return render_template('change.html', error = error)
            if checkpass(password) is not None:
                error = checkpass(password)
                return render_template('change.html', error = error)
            with mysql.connection.cursor(named_tuple=True) as cursor:
                    cursor.execute(
                        ('UPDATE users SET password_hash=SHA2(%(password)s, 256) WHERE login=%(login)s AND last_name=%(last_name)s;'), params)
                    mysql.connection.commit()
        else:
            flash('Не удалось сменить пароль, проверьте логин и фамилию', 'danger')
            return render_template('change.html', error = error)
        flash('Вы успешно сменили пароль', 'success')
        return redirect(url_for('auth.login'))
    return render_template('change.html', error = error)

@app.route('/change_auth', methods=['GET','POST'])
@login_required
def change_auth():
    error = None
    if request.method == "POST":
        old_password = request.form.get('oldpassword')
        password = request.form.get('password')
        confpassword = request.form.get('confirmpassword')
        with mysql.connection.cursor(named_tuple=True) as cursor:
                cursor.execute(
                    ('SELECT * FROM users WHERE id=%s AND password_hash=SHA2(%s, 256);'), (current_user.id, old_password ))
                db_user = cursor.fetchone()
        if db_user:
            if password != confpassword:
                error = "Пароль должны быть одинаковыми"
                return render_template('change.html', error = error)
            if checkpass(password) is not None:
                error = checkpass(password)
                return render_template('change.html', error = error)
            with mysql.connection.cursor(named_tuple=True) as cursor:
                    cursor.execute(
                        ('UPDATE users SET password_hash=SHA2(%s, 256) WHERE id=%s;'), (password, current_user.id))
                    mysql.connection.commit()
        else:
            flash("Неверный старый пароль", 'danger')
            return render_template('change.html', error = error)
        flash('Вы успешно сменили пароль', 'success')
        return redirect(url_for('index'))
    return render_template('change.html', error = error)

def check(params):
    dict = {'login': None, 'password': None, 'first_name': None, 'middle_name': None, 'last_name': None}
    dict['login'] = checklog(params['login'])
    dict['password'] = checkpass(params['password'])

    return dict
    
def checklog(login):
    alphlog = "abcdefghijklmnopqrstuvwxyz1234567890"
    if login is None:
        return "Поле не должно быть пустым"
    if len(login)<5:
        return "Длинна логина должна быть не менее 5 символов"
    for i in login:
        if (i.lower() in alphlog)==0:
            return "Логин должен состоять только из латинских букв и цифр"
    return None
    
def checkpass(password):
    alphpass = "abcdefghijklmnopqrstuvwxyz1234567890абвгдеёжзийклмнопрстуфхцчшщъыьэюя~!?@#$%^&*_-+()[]{>}</\|\"\'.,:;"
    if len(password) < 8 or len(password) > 128:
        return "Длинна пароля должна быть в пределах от 8 до 128"
    up, low = False, False
    for i in password:
        if i == " ":
            return "Пароль не может содержать пробелы"
        if (i.lower() in alphpass)==0:
            return "Пароль содержит недопустимые символы"
    for i in password:
        if i.isupper():
            up = True
        if i.islower():
            low = True
        if up and low:
            break
    if not up or not low:
        return "Пароль должен содержать как минимум одну заглавную и одну строчную букву"
    return None
