from flask import Flask
from celery import Celery
import json


class Response:
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    NO_CONTENT = 204

    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404


def json2dict(data):
    return json.loads(data, strict=False) if data else dict()


def make_celery(app):
    celery = Celery(app.import_name)
    celery.conf.update(app.config.get('CELERY_CONFIG'))

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
