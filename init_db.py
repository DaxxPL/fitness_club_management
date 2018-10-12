from sqlalchemy import create_engine
from main import db
from models import User
import os
from passlib.hash import sha256_crypt


def db_start():
    if os.path.exists('test.db'):
        os.remove('test.db')
    engine = create_engine('sqlite:///tmp/test/db', convert_unicode=True, echo=True)
    db.create_all()
    db.session.commit()
    user = User()
    user.name = 'Mikołaj'
    user.password = sha256_crypt.hash('haslo')
    user.email = 'mik89123@o2.pl'
    db.session.add(user)
    db.session.commit()


if __name__ == '__main__':
    db_start()
