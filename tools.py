import json


def json2dict(data):
    return json.loads(data, strict=False) if data else dict()
