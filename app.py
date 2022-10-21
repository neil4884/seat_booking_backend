from flask import Flask, request
from unit import User, Seat
import json

app = Flask(__name__)


@app.route('/')
def home():  # put application's code here
    return 'Hello World!'


@app.route('/test', methods=['POST', 'GET', 'PUT', 'DELETE'])
def test_page():
    """
    This is an example of REST API usage, with addition of linkage to our database and linkage classes.

    POST: Backend gets Data from Frontend
    GET: Frontend requests and gets Data from Backend
    PUT:
    DELETE:
    :return:
    """
    if request.method == 'POST':
        body = request.data
        data = json.loads(body, strict=False) if body else dict()
        print(data)
        return data, 201

    elif request.method == 'GET':
        q = request.args.get('q')
        print(q)
        return {'message': 'Hello!', 'loop_back': q}, 200

    elif request.method == 'PUT':



if __name__ == '__main__':
    app.run(debug=True)
