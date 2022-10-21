from flask import Flask, request
import json

app = Flask(__name__)


@app.route('/')
def home():  # put application's code here
    return 'Hello World!'


@app.route('/test')
def test_page():
    q = request.args.get('q')
    print(q)
    return {'message': "Hello!"}, 201


if __name__ == '__main__':
    app.run()
