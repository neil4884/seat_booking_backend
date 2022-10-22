from enum import Enum
import json


class Response(Enum):
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
