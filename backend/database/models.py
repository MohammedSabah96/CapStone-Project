import os
from sqlalchemy import Column, String, Integer, DateTime
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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

    def format_data(self):
        return {
            'id': self.id,
            'name': self.name
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()


class Product(db.Model):
    id = Column(Integer(), primary_key=True)
    title = Column(String(80), unique=True)
    description = Column(String(180), nullable=True)
    price = Column(String(20), nullable=False)
    imageUrl = Column(String(250))
    public_id_image = Column(String(), nullable=False)
    created = Column(DateTime(), nullable=False, default=datetime.utcnow, onupdate=datetime.now)
    owner = Column(String())
    mobile = Column(Integer())
    user_id = Column(Integer(), db.ForeignKey('user.id'))

    def __init__(self, title, description, price, imageUrl, public_id_image, owner, mobile, user):
        self.title = title
        self.description = description
        self.price = price
        self.imageUrl = imageUrl
        self.public_id_image = public_id_image
        self.mobile = mobile
        self.created = datetime.utcnow()
        self.owner = owner
        self.user_id = user.id

    def format_data_short(self):
        return {
            'id': self.id,
            'title': self.title,
            'price': self.price,
            'imageUrl': self.imageUrl,
            'created': self.created,
            'owner': self.owner,
            'user_id': self.user_id
        }

    def format_data_long(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'imageUrl': self.imageUrl,
            'public_id': self.public_id_image,
            'created': self.created,
            'mobile': self.mobile,
            'owner': self.owner,
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


class Announcement(db.Model):
    id = Column(Integer(), primary_key=True)
    announcement = Column(String())

    def __init__(self, announcement):
        self.announcement = announcement

    def format(self):
        return {
            'announcement': self.announcement
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
