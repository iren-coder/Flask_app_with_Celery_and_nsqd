import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_APP="app.py"
    FLASK_DEBUG=1
    FLASK_ENV='development'
    SECRET_KEY='secret_key'
