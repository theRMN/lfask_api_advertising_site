from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import datetime

app = Flask(__name__)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.config.from_mapping(SQLALCHEMY_DATABASE_URI='postgresql://admin:admin@127.0.0.1:5432/advertising_site')


class Advertising(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String, index=True, unique=True)
    create_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    creator_id = db.Column(db.Integer, db.ForeignKey('creator.id'))


class Creator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    advertising = db.relationship('Advertising', backref='creator', lazy='dynamic')
