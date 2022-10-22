from flask import Flask, request
from unit import User, Seat
import json
import tools

app = Flask(__name__)
user = User()


@app.route('/')
def home():  # put application's code here
    return 'Hello World!'


@app.route('/test', methods=['POST', 'GET', 'PUT', 'PATCH', 'DELETE'])
def test_page():
    """
    This is an example of REST API usage, with addition of linkage to our database and linkage classes.

    Use cases: there will be endpoints for some HTTP method, i.e., GET /users will get a list of all users
    and GET /users/user_643xxxxx21 will get a single user.

    POST: Frontend requests and gives Data to Backend to do something (200)

    GET: Frontend requests and gets Data from Backend (200)

    PUT: Frontend requests to replace Data in Backend (can check to replace/create: 200/201)

    PATCH: Frontend requests to partially update Data in Backend

    DELETE: Frontend requests to delete Data in Backend (200)

    :return: Dictionary of something (JSON package) and HTTP status response code for success/failure
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

    elif request.method == 'PATCH':
        return

    elif request.method == 'DELETE':
        data = tools.json2dict(request.data)
        print(data)
        return {'message': 'PUT CALLED', 'loop_back': data}, 200


if __name__ == '__main__':
    app.run(debug=True)
