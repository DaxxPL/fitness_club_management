from flask_login import UserMixin
from main import db
from sqlalchemy import Column
from sqlalchemy.types import Integer, Boolean, String


class User(db.Model, UserMixin):
    id = Column(Integer, autoincrement=True, primary_key=True)
    active = Column(Boolean, default=True)
    name = Column(String(20), nullable=False)
    email = Column(String(200), unique=True, nullable=False)
    password = Column(String(200), nullable=False)

    def is_active(self):
        return self.active
