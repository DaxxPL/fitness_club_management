from main import app
from main import db
from flask import request, session, flash, render_template, redirect
from models import User
from passlib.hash import sha256_crypt
from functools import wraps


def login_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if 'logged_in'not in session:
            flash('Musisz być zalogowany.')
            return redirect('/')
        else:
            return func(*args, **kwargs)
    return wrap


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['action'] == 'Zaloguj':
            db_user = User.query.filter_by(email=request.form['email']).first()
            if db_user:
                db_password = db_user.password
                if sha256_crypt.verify(request.form['password'], db_password):
                    session['logged_in'] = True
                    session['username'] = request.form['email']
                    db_user.active = 1
                    db.session.commit()
                    flash('Zalogowano!')
                else:
                    flash('Niepoprawne hasło')
            else:
                flash('Użytkownika o podanym adresie e-mail nie ma w bazie!')
        elif request.form['action'] == 'Wyloguj':
            try:
                User.query.filter_by(email=session['username']).first().active=0
                db.session.commit()
                session.clear()
            except KeyError:
                flash('Nie można wylogować niezalogowaneo użytkownika.')
    return render_template('login.html')


@app.route('/czy_logowanie_dziala')
@login_required
def check():
    return render_template('zalogowano.html')


app.secret_key = 'sekretny klucz'
