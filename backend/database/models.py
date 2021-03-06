import os
from sqlalchemy import Column, String, Integer, DateTime, BIGINT
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dotenv import load_dotenv

# this is going to let us using the variables that defined in .env file
load_dotenv()

# (1) uncomment the line below if you wanna do tests with test_app.py
# database_path = os.environ.get("DATABASE_URL_TEST")

# (2) commit line[11,12,13,14,15,16] if you want to do tests with test_app.py
# but if you want to do test with postman collection don't commit it
pgUser = os.environ['PGUSER']
pgPass = os.environ['PGPASSWORD']
pgHost = os.environ['PGHOST']
pgPort = os.environ['PGPORT']
pgDatabase = os.environ['PGDATABASE']
database_path = "postgres://{}:{}@{}:{}/{}" \
    .format(pgUser, pgPass, pgHost, pgPort, pgDatabase)

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    # (3) if you are doing some tests
    # you want to make sure uncomment the line below
    # db.drop_all()
    db.create_all()


"User Model"


class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer(), primary_key=True)
    name = Column(String(20), unique=True, nullable=False)
    products = db.relationship('Product', backref='users')

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

    # this method is for testing end point only
    def delete(self):
        db.session.delete(self)
        db.session.commit()


"Product Model"


class Product(db.Model):
    __tablename__ = 'products'
    id = Column(Integer(), primary_key=True)
    title = Column(String(80), unique=True)
    description = Column(String(180), nullable=True)
    price = Column(String(20), nullable=False)
    imageUrl = Column(String(250))
    public_id_image = Column(String(), nullable=False)
    imageName = Column(String())
    created = Column(DateTime(), nullable=False,
                     default=datetime.utcnow, onupdate=datetime.now)
    owner = Column(String())
    mobile = Column(BIGINT())
    user_id = Column(Integer(), db.ForeignKey('users.id'))

    def __init__(self, title, description, price, imageUrl,
                 public_id_image, imageName, owner, mobile, user):
        self.title = title
        self.description = description
        self.price = price
        self.imageUrl = imageUrl
        self.public_id_image = public_id_image
        self.imageName = imageName
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
            'imageName': self.imageName,
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


"Announcement Model"


class Announcement(db.Model):
    __tablename__ = 'Announcement'
    id = Column(Integer(), primary_key=True)
    announcement = Column(String())

    def __init__(self, announcement):
        self.announcement = announcement

    def format(self):
        return {
            'id': self.id,
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
