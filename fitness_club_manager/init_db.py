from fitness_club_manager.models import User, Training
from passlib.hash import sha256_crypt
from fitness_club_manager.main import db, app
import datetime
import os

if __name__ == '__main__':
    if os.path.exists('production.db'):
        os.remove('production.db')
    user = User()
    user.name = 'Mikołaj'
    user.password = sha256_crypt.hash('haslo')
    user.email = 'mik89123@o2.pl'
    db.app = app
    db.init_app(app)
    db.create_all()
    db.session.add(user)
    db.session.commit()
    training = Training()
    training.max_participants = 25
    training.date_of_training = datetime.date(datetime.date.today().year, datetime.date.today().month,
                                              datetime.date.today().day)
    training.time_of_training = datetime.time(8, 45)
    db.create_all()
    db.session.add(training)
    db.session.commit()
    print('initalized!')
