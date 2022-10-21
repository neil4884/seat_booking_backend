from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():  # put application's code here
    return 'Hello World!'


@app.route('/test')
def test_page():
    return 'This is test page.'


if __name__ == '__main__':
    app.run()
