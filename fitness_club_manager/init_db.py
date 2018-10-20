from models import User
from passlib.hash import sha256_crypt
from main import db, app

if __name__ == '__main__':
    user = User()
    user.name = 'Mikołaj'
    user.password = sha256_crypt.hash('haslo')
    user.email = 'mik89123@o2.pl'
    db.app = app
    db.init_app(app)
    db.create_all()
    db.session.add(user)
    db.session.commit()
    print('initalized!')

