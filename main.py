
from flask import Flask
from views import login_blueprint
from models import db


app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)
db.create_all(app=app)

app.register_blueprint(login_blueprint)

if __name__ == '__main__':
    app.run()
