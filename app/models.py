import enum
from sqlalchemy import Enum

from app import db

class Results(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(300), unique=False, nullable=True)
    words_count = db.Column(db.Integer, unique=False, nullable=True)
    http_status_code = db.Column(db.Integer)


class TaskStatus (enum.Enum):
    NOT_STARTED = 1
    PENDING = 2
    FINISHED = 3

class Tasks(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(300), unique=False, nullable=True)
    timestamp = db.Column(db.DateTime())
    task_status = db.Column(Enum(TaskStatus))
    http_status = db.Column(db.Integer)

class NSQD:
    def __init__(self, server):
        self.server = "http://{server}/pub".format(server=server)

    def send(self, topic, message):
        res = requests.post(self.server, params={'topic': topic}, data=message)
        if res.ok:
            return res


nsqd = NSQD('nsqd:4151')