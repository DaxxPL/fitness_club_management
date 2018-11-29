from flask_login import UserMixin
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.types import Integer, Boolean, String, Date, Time
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

association_table = Table('association', db.metadata,
                          Column('user_id', Integer, ForeignKey('user.user_id')),
                          Column('training_id', Integer, ForeignKey('training.training_id'))
                          )


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    user_id = Column(Integer, autoincrement=True, primary_key=True)
    active = Column(Boolean, default=True)
    name = Column(String(20), nullable=False)
    email = Column(String(200), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    trainings = relationship("Training", secondary=association_table, backref=db.backref('trainees', lazy='dynamic'))

    def is_active(self):
        return self.active


class Training(db.Model):
    __tablename__ = 'training'
    training_id = Column(Integer, autoincrement=True, primary_key=True)
    max_participants = Column(Integer, nullable=False)
    time_of_training = Column(Time, nullable=False)
    date_of_training = Column(Date, nullable=False)
    subscribers = Column(Integer, default=0)
    description = Column(String, nullable=False)

