from flask_login import UserMixin
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.types import Integer, Boolean, String, Date, Time
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt
import datetime

db = SQLAlchemy()

user_training = Table('user_training', db.metadata,
                      Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
                      Column('training_id', Integer, ForeignKey('training.id'), primary_key=True)
                      )


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, autoincrement=True, primary_key=True)
    active = Column(Boolean, default=True)
    name = Column(String(20), nullable=False)
    email = Column(String(200), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    trainings = relationship("Training", secondary=user_training, back_populates='users')
    valid_up_to = Column(Date, default=datetime.date.today())
    trainings_left = Column(Integer, default=-1)  # -1 is infinity number of trainings to left

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = sha256_crypt.hash(password)

    def is_active(self):
        return self.active

    def can_subscribe(self):
        if self.trainings_left != 0 and self.valid_up_to > datetime.date.today():
            return True
        else:
            return False


class Training(db.Model):
    __tablename__ = 'training'
    id = Column(Integer, autoincrement=True, primary_key=True)
    max_participants = Column(Integer, nullable=False)
    start_time_of_training = Column(Time, nullable=False)
    finish_time_of_training = Column(Time, nullable=False)
    date_of_training = Column(Date, nullable=False)
    description = Column(String)
    name_of_training = Column(String, default='Trening dnia')
    users = relationship("User", secondary=user_training, back_populates='trainings')

    def __init__(self, max_participants, start_time_of_training,
                 finish_time_of_training, date_of_training, description):
        self.max_participants = max_participants
        self.start_time_of_training = start_time_of_training
        self.finish_time_of_training = finish_time_of_training
        self.date_of_training = date_of_training
        self.description = description

    def number_of_signed_users(self):
        return len(self.users)

    def datetime_of_training(self):
        return datetime.datetime.combine(self.date_of_training, self.start_time_of_training)



