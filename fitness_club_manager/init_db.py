from fitness_club_manager.models import User, Training
from fitness_club_manager.main import db, app
import datetime
import os

if __name__ == '__main__':
    if os.path.exists('production.db'):
        os.remove('production.db')

    user1 = User(name='Mikołaj', email='mik89123@o2.pl', password='haslo')
    user1.valid_up_to = datetime.date.today() + datetime.timedelta(days=10)
    user1.trainings_left = 5

    user2 = User('Dominika', 'dz@wo.pl', 'haslo2')
    user2.valid_up_to = datetime.date(2018, 10, 3)

    user3 = User('Hubert', 'hh@o2.pl', 'haslo3')
    user3.valid_up_to = datetime.date.today() + datetime.timedelta(days=9)
    user3.trainings_left = 1

    training1 = Training(25,
                         datetime.time(20, 45),
                         datetime.time(21, 45),
                         datetime.date(datetime.date.today().year,
                                       datetime.date.today().month,
                                       datetime.date.today().day),
                         'Bla bla bla')

    training2 = Training(25,
                         datetime.time(9, 45),
                         datetime.time(10, 45),
                         datetime.date(datetime.date.today().year,
                                       datetime.date.today().month,
                                       datetime.date.today().day),
                         'Bla bla bla2'
                         )
    user1.trainings = [training2]
    user2.trainings = [training2]
    user2.trainings.append(training1)
    db.app = app
    db.init_app(app)
    db.create_all()
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.add(training1)
    db.session.add(training2)
    db.create_all()
    db.session.commit()
    print('initalized!')
