from flask import Flask, request
from firebase_admin import credentials
from firebase_admin import firestore
from unit import User
from unit import Seat
import firebase_admin as fb
import json
import os
import tools


cred = credentials.Certificate('credentials/seat-booking-db-firebase-adminsdk-4e0g2-518adfa3cc.json')
app_fb = fb.initialize_app(cred)
app = Flask(__name__)
db = firestore.client()

@app.route('/users', methods=['GET'])
async def users():
    return {}, 200

@app.route('/users/<user>', methods=['GET'])
async def i_users(user):
    return {}, 200


if __name__ == '__main__':
    app.run(debug=True)
