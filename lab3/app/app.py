from flask import Flask, render_template, request, make_response, session, redirect,url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message = 'Для доступка к данной странице пройдите аутентификацю'
login_manager.login_message_category = 'warning' 

app = Flask(__name__)
application = app

login_manager.init_app(app)


class User(UserMixin):
    def __init__(self, user_id,login,password):
        # super().__init__()
        self.id = user_id
        self.login = login
        self.password = password


@login_manager.user_loader
def load_user(user_id):
    for user in get_users():
        if user['user_id'] == int(user_id):
            return User(**user)
    return None


def get_users():
    return [{'user_id': 1,'login':'admin','password':'admin'}]


app.config.from_pyfile('config.py')
@app.route('/')
def index():
    return render_template('/index.html')


@app.route('/visits')
def visits():
    if session.get('visits_count') is None:
        session['visits_count'] = 1
    else:
        session['visits_count'] +=1
    return render_template('visits.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('pass')
        rememberme = request.form.get('rememberme') == 'on'

        for user in get_users():
            if user['login'] == login and user['password'] == password:
                login_user(User(**user), remember = rememberme)
                flash('Вы молодец', 'success')
                return redirect(url_for('index'))
        flash('Ошиб0чка', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/secret_page')
@login_required
def secret_page():
    return render_template('secret_page.html')
