from google.api_core.datetime_helpers import DatetimeWithNanoseconds
import json
import datetime
import hashlib


RAND_MAP = {k: v for k, v in zip('0123456789', 'oithfspven')}


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


def generate_hash(passwd):
    passwd_t = 'k'.join([RAND_MAP.get(e) if e in RAND_MAP.keys() else e for e in passwd])
    return hashlib.sha1(passwd_t.encode()).hexdigest()[::2]
