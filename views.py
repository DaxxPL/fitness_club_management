from models import db
from flask import request, session, flash, render_template, redirect, Blueprint
from models import User
from passlib.hash import sha256_crypt
from functools import wraps

login_blueprint = Blueprint('logins', __name__)


def login_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if 'logged_in'not in session:
            flash('Musisz być zalogowany.')
            return redirect('/')
        else:
            return func(*args, **kwargs)
    return wrap


@login_blueprint.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['action'] == 'Zaloguj':
            from_email_form = request.form['email']
            from_pass_form = request.form['password']
            if len(from_email_form) != 0 and len(from_pass_form) != 0:
                db_user = User.query.filter_by(email=from_email_form).first()
                if db_user:
                    db_password = db_user.password
                    if sha256_crypt.verify(from_pass_form, db_password):
                        session['logged_in'] = True
                        session['username'] = request.form['email']
                        db_user.active = 1
                        db.session.commit()
                        flash('Zalogowano!')
                    else:
                        flash('Niepoprawne hasło')
                else:
                    flash('Użytkownika o podanym adresie e-mail nie ma w bazie!')
            else:
                flash('nie wprowadziłeś hasła!')
        elif request.form['action'] == 'Wyloguj':
            try:
                User.query.filter_by(email=session['username']).first().active=0
                db.session.commit()
                session.clear()
            except KeyError:
                flash('Nie można wylogować niezalogowaneo użytkownika.')
    return render_template('login.html')


@login_blueprint.route('/czy_logowanie_dziala')
@login_required
def check():
    return render_template('zalogowano.html')


