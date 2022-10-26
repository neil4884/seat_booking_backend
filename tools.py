from google.api_core.datetime_helpers import DatetimeWithNanoseconds
import json
import datetime
import string
import random
import hashlib


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


def random_unique_id(length):
    # Getting password length
    characterList = ""

    # Getting character set for password
    characterList += string.ascii_letters
    characterList += string.digits
    characterList += string.punctuation
    password = ""

    for i in range(length):
        # Picking a random character from our
        # character list
        randomchar = random.choice(characterList)
        # appending a random character to password
        password += randomchar

    return password


def random_secret(passwd, length=6):
    salt = hashlib.
    hashlib.sha256(passwd.encode())
