from flask import Flask, request
from firebase_admin import credentials
from firebase_admin import firestore
from tools import Response
from unit import User
from unit import Seat
import firebase_admin as fb
import json
import os
import tools


cred = credentials.Certificate(os.path.abspath('credentials/seat-booking-db-firebase-adminsdk-4e0g2-518adfa3cc.json'))
app_fb = fb.initialize_app(cred)
app = Flask(__name__)
db = firestore.client()

@app.route('/users', methods=['GET'])
async def get_users():
    users_collection_stream = db.collection('users').stream()
    users = {user.id: user.to_dict() async for user in users_collection_stream}
    if users:
        return users, Response.OK
    return {}, Response.NO_CONTENT

@app.route('/users/<user>', methods=['GET'])
async def get_user(user):
    user_doc_ref = db.collection('users').document(user)
    user_doc = await user_doc_ref.get()
    if user_doc.exist:
        return user_doc.to_dict(), Response.OK
    return {}, Response.NO_CONTENT

@app.route('/users/<user>', methods=['POST'])
async def set_user(user):
    return {}, Response.OK

@app.route('/seats/<seat>', methods=['GET'])
async def get_seat(seat):
    seat_doc_ref = db.collection('seats').document(seat)
    seat_doc = await seat_doc_ref.get()
    if seat_doc.exist:
        return seat_doc.to_dict(), Response.OK
    return {}, Response.NO_CONTENT


if __name__ == '__main__':
    app.run(debug=True)
