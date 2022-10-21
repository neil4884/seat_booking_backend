from flask import Flask, request
from unit import User, Seat
import json
import tools

app = Flask(__name__)
user = User()


@app.route('/')
def home():  # put application's code here
    return 'Hello World!'


@app.route('/test', methods=['POST', 'GET', 'PUT', 'DELETE'])
def test_page():
    """
    This is an example of REST API usage, with addition of linkage to our database and linkage classes.

    POST: Frontend requests and gives Data to Backend to do something (200)

    GET: Frontend requests and gets Data from Backend (200)

    PUT: Frontend requests to replace Data in Backend (can check to replace/create: 200/201)

    DELETE: Frontend requests to delete Data in Backend (200)

    :return:
    """
    if request.method == 'POST':
        data = tools.json2dict(request.data)
        print(data)
        return {'message': 'POST CALLED', 'loop_back': data}, 201

    elif request.method == 'GET':
        q = request.args.get('q')
        print(q)
        return {'message': 'GET CALLED', 'loop_back': q}, 200

    elif request.method == 'PUT':
        data = tools.json2dict(request.data)
        print(data)
        return {'message': 'PUT CALLED', 'loop_back': data}, 200

    elif request.method == 'DELETE':
        data = tools.json2dict(request.data)
        print(data)
        return {'message': 'PUT CALLED', 'loop_back': data}, 200


if __name__ == '__main__':
    app.run(debug=True)
