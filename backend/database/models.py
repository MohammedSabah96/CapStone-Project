import os

from sqlalchemy import Column, String, Integer, DateTime
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

database_filename = "database.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(
    os.path.join(project_dir, database_filename))
# database_name = "capstone"
# database_path = "postgres://{}:{}@{}/{}".format(
#     'postgres', 'gkmgkm123A', 'localhost:5432', database_name)
db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class User(db.Model):
    id = Column(Integer(), primary_key=True)
    name = Column(String(20), unique=True, nullable=False)
    products = db.relationship('Product', backref='user')

    def __init__(self, name):
        self.name = name

    def insert(self):
        db.session.add(self)
        db.session.commit()


class Product(db.Model):
    id = Column(Integer(), primary_key=True)
    title = Column(String(80), unique=True)
    description = Column(String(180), nullable=True)
    price = Column(String(20), nullable=False)
    imageUrl = Column(String(250))
    created = Column(DateTime())
    user_id = Column(Integer(), db.ForeignKey('user.id'))

    def __init__(self, title, description, price, imageUrl, user):
        self.title = title
        self.description = description
        self.price = price
        self.imageUrl = imageUrl
        self.created = datetime.today()
        self.user_id = user.id

    def format_data_short(self):
        return {
            'id': self.id,
            'title': self.title,
            'price': self.price,
            'imageUrl': self.imageUrl,
            'user_id': self.user_id
        }

    def format_data_long(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'imageUrl': self.imageUrl,
            'created': self.created,
            'user_id': self.user_id
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def update():
        db.session.commit()

    def __repr__(self):
        return self.format_data()
