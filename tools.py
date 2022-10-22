from google.api_core.datetime_helpers import DatetimeWithNanoseconds
from flask import Flask
from celery import Celery
import json
import datetime


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


def to_datetime(date_time_with_nanoseconds: DatetimeWithNanoseconds):
    return datetime.datetime.fromtimestamp(date_time_with_nanoseconds.timestamp())


def time_now():
    return datetime.datetime.now()
