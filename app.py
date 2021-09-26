import asyncio
from aiosmtplib import send
import more_itertools

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from celery import Celery

import datetime

app_name = 'app'
app = Flask(__name__)
celery = Celery(
    app_name,
    backend='redis://127.0.0.1:6379/1',
    broker='redis://127.0.0.1:6379/2'
)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.config.from_mapping(SQLALCHEMY_DATABASE_URI='postgresql://admin:admin@127.0.0.1:5432/advertising_site')


class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)


celery.Task = ContextTask


@celery.task()
def send_email():
    asyncio.run(EmailSender.extract_and_send(
        hostname='smtp.gmail.com',
        port=587,
        sender='sender',
        username='user@example.org',
        password='password'
    ))
    return


class Advertising(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String, index=True, unique=True)
    create_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    creator_id = db.Column(db.Integer, db.ForeignKey('creator.id'))


class Creator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String, index=True, unique=True)
    advertising = db.relationship('Advertising', backref='creator', lazy='dynamic')


class EmailSender:

    @staticmethod
    async def extract_and_send(
            hostname,
            port,
            sender,
            username,
            password
    ):

        cor_list = []
        cur = Creator.query.all()

        for row in cur:
            recipients = row.email
            message = f'Уважаемый {row.name}! Спасибо, что пользуетесь нашим сервисом объявлений.'.encode('utf-8')
            cor_list.append(
                send(
                    message,
                    recipients=recipients,
                    sender=sender,
                    hostname=hostname,
                    port=port,
                    username=username,
                    password=password,
                    start_tls=True
                )
            )

        for chunk in more_itertools.chunked(cor_list, 10):
            await asyncio.gather(*chunk)
