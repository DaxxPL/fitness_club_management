from fitness_club_manager.models import db, User, Training
from flask import request, session, flash, render_template, redirect, Blueprint, url_for
from passlib.hash import sha256_crypt
from functools import wraps
import datetime

login_blueprint = Blueprint('logins', __name__)
user_training = Blueprint('user_trainings', __name__)


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
    if 'logged_in' in session:
        return redirect('/trening')
    elif request.method == 'POST':
        if request.form['login'] == 'click':
            from_email_form = request.form['email']
            from_pass_form = request.form['password']
            db_user = User.query.filter_by(email=from_email_form).first()
            if db_user:
                db_password = db_user.password
                if sha256_crypt.verify(from_pass_form, db_password):
                    session['logged_in'] = True
                    session['username'] = from_email_form
                    db_user.active = 1
                    db.session.commit()
                    return redirect('/trening')
                else:
                    flash('Niepoprawne hasło')
            else:
                flash('Użytkownika o podanym adresie e-mail nie ma w bazie!')
    return render_template('login.html')


@login_blueprint.route('/czy_logowanie_dziala')
@login_required
def check():
    return render_template('zalogowano.html')


@login_blueprint.route('/trening')
@login_required
def forward():
    date = datetime.date.today()
    return redirect(url_for('logins.trainings', date=date))


@login_blueprint.route('/trening/<date>', methods=['GET', 'POST'])
@login_required
def trainings(date):
    date_object = datetime.date.fromisoformat(date)
    day_of_week = ['poniedziałek', 'wtorek', 'środa', 'czwartek', 'piątek', 'sobota', 'niedziela']
    user = User.query.filter_by(email=session['username']).first()
    this_day_trainings = Training.query.filter_by(date_of_training=date_object)\
        .order_by(Training.start_time_of_training).all()
    dis_training = None
    print(user.trainings_left)
    if len(this_day_trainings) > 0:
        dis_training = this_day_trainings[0]
    if request.method == 'POST':
        if 'button' in request.form.keys():
            if request.form['button'] == 'log_out':
                try:
                    user.active = 0
                    db.session.commit()
                    session.clear()
                    return redirect('/')
                except KeyError:
                    flash('Nie można wylogować niezalogowaneo użytkownika.')
            elif request.form['button'] == 'back':
                return redirect(url_for('logins.trainings', date=date_object + datetime.timedelta(days=-1)))
            elif request.form['button'] == 'forward':
                return redirect(url_for('logins.trainings', date=date_object + datetime.timedelta(days=+1)))
        elif 'sign_in' in request.form.keys():
            training = Training.query.filter_by(id=int(request.form['sign_in'])).first()
            user.trainings.append(training)
            dis_training = training
            if user.trainings_left >= 1:
                user.trainings_left -= 1
            db.create_all()
            db.session.commit()
        elif 'sign_out' in request.form.keys():
            training = Training.query.filter_by(id=int(request.form['sign_out'])).first()
            user.trainings.remove(training)
            if user.trainings_left >= 0:
                user.trainings_left += 1
            db.create_all()
            db.session.commit()
        elif 'display_training' in request.form.keys():
            dis_training = Training.query.filter_by(id=int(request.form['display_training'])).first()
    return render_template('plany.html',
                           date=date_object,
                           day=day_of_week[date_object.weekday()],
                           user=user,
                           trainings=this_day_trainings,
                           now=datetime.datetime.now() - datetime.timedelta(minutes=15),
                           dis_training=dis_training)


