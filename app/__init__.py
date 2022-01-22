from celery import Celery
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CsrfProtect


from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.debug = True
    return app

app = create_app()
db = SQLAlchemy(app)
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

from app import routes, models, forms
db.create_all()
