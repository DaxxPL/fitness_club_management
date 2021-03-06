import os
from flask import Flask
from fitness_club_manager.views import login_blueprint, user_training
from fitness_club_manager.models import db
import fitness_club_manager


app = Flask(__name__)
app.config.from_object('fitness_club_manager.config')
db.init_app(app)
db.create_all(app=app)


app.register_blueprint(login_blueprint)
app.register_blueprint(user_training)
app.debug = True

if __name__ == '__main__':
    app.run()
