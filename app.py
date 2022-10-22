from flask import Flask, request
# from celery import Celery
from firebase_admin import credentials
from firebase_admin import firestore
from tools import Response
from tools import json2dict
# from tools import make_celery
# from unit import User
# from unit import Seat
import firebase_admin as fb
# import json
import os

USERS_COLLECTION = 'users'
SEATS_COLLECTION = 'seats'

cred = credentials.Certificate(os.path.abspath('credentials/seat-booking-db-firebase-adminsdk-4e0g2-518adfa3cc.json'))
app_fb = fb.initialize_app(cred)
db = firestore.client()
app = Flask(__name__)


# celery = make_celery(app)


@app.route('/users', methods=['GET'])
async def get_users():
    """
    Get all users' data if request body is empty, users' data in request body's key "users". If there are no users
    in the database, and empty dictionary and NO_CONTENT is returned, otherwise list of users with id as key and OK
    is returned.

    :return:
    """
    data = json2dict(request.data)
    if not data or data.get('users') is None:
        users_collection_stream = db.collection(USERS_COLLECTION).stream()
        users = {user.id: user.to_dict() for user in users_collection_stream}
        if not users:
            return {}, Response.NO_CONTENT
        return users, Response.OK

    return_dict = {}
    for user_id in data.get('users'):
        user_doc_ref = db.collection(USERS_COLLECTION).document(user_id)
        user_doc = user_doc_ref.get()
        if user_doc.exists:
            return_dict[user_id] = user_doc.to_dict()

    return return_dict, (Response.OK if return_dict else Response.NO_CONTENT)


@app.route('/users/<user>', methods=['GET'])
async def get_user(user):
    """
    Get one user's data. Return dictionary of user data and OK if exists, else NO_CONTENT

    :param user:
    :return:
    """
    user_doc_ref = db.collection(USERS_COLLECTION).document(user)
    user_doc = user_doc_ref.get()
    if not user_doc.exists:
        return {}, Response.NO_CONTENT
    return user_doc.to_dict(), Response.OK


@app.route('/users/<user>', methods=['POST', 'PUT'])
async def set_user(user):
    """
    Set user's value in request body's key: value accordingly, merge if exists.

    **!!!Additional keys are added!!!**

    :param user:
    :return:
    """
    user_doc_ref = db.collection(USERS_COLLECTION).document(user)
    user_doc = user_doc_ref.get()
    data = json2dict(request.data)
    if not user_doc.exists:
        user_doc_ref.set(data, merge=True)
        user_doc = user_doc_ref.get()
        return user_doc.to_dict(), Response.CREATED
    user_doc_ref.set(data, merge=True)
    user_doc = user_doc_ref.get()
    return user_doc.to_dict(), Response.OK


@app.route('/users/<user>', methods=['PATCH'])
async def update_user(user):
    """
    Update user's value in request body's key: value accordingly, merge if exists.

    :param user:
    :return:
    """
    user_doc_ref = db.collection(USERS_COLLECTION).document(user)
    user_doc = user_doc_ref.get()
    data = {k: v for k, v in json2dict(request.data).items() if
            k in user_doc.to_dict()} if user_doc.exists else json2dict(request.data)
    if not user_doc.exists:
        user_doc_ref.set(data, merge=True)
        user_doc = user_doc_ref.get()
        return user_doc.to_dict(), Response.CREATED
    user_doc_ref.set(data, merge=True)
    user_doc = user_doc_ref.get()
    return user_doc.to_dict(), Response.OK


@app.route('/users', methods=['DELETE'])
async def delete_users():
    data = json2dict(request.data)
    return_dict = {}
    if not data or data.get('users') is None:
        return {}, Response.BAD_REQUEST
    for user_id in data.get('users'):
        user_doc_ref = db.collection(USERS_COLLECTION).document(user_id)
        user_doc = user_doc_ref.get()
        if user_doc.exists:
            user_doc_ref.delete()
            return_dict[user_id] = (user_doc.to_dict())
    return return_dict, Response.OK


@app.route('/users/<user>', methods=['DELETE'])
async def delete_user(user):
    user_doc_ref = db.collection(USERS_COLLECTION).document(user)
    user_doc = user_doc_ref.get()
    if not user_doc.exists:
        return {}, Response.NO_CONTENT
    user_doc_ref.delete()
    return user_doc.to_dict(), Response.OK


# ####################### SEAT QUERY ########################

@app.route('/seats', methods=['GET'])
async def get_seats():
    """
    Get all seats' data if request body is empty, seats' data in request body's key "seats". If there are no seats
    in the database, and empty dictionary and NO_CONTENT is returned, otherwise list of seats with id as key and OK
    is returned.

    :return:
    """
    data = json2dict(request.data)
    if not data or data.get('seats') is None:
        SEATS_COLLECTION_stream = db.collection(SEATS_COLLECTION).stream()
        seats = {seat.id: seat.to_dict() for seat in SEATS_COLLECTION_stream}
        if not seats:
            return {}, Response.NO_CONTENT
        return seats, Response.OK

    return_dict = {}
    for seat_id in data.get('seats'):
        seat_doc_ref = db.collection(SEATS_COLLECTION).document(seat_id)
        seat_doc = seat_doc_ref.get()
        if seat_doc.exists:
            return_dict[seat_id] = seat_doc.to_dict()

    return return_dict, (Response.OK if return_dict else Response.NO_CONTENT)


@app.route('/seats/<seat>', methods=['GET'])
async def get_seat(seat):
    """
    Get one seat's data. Return dictionary of seat data and OK if exists, else NO_CONTENT

    :param seat:
    :return:
    """
    seat_doc_ref = db.collection(SEATS_COLLECTION).document(seat)
    seat_doc = seat_doc_ref.get()
    if not seat_doc.exists:
        return {}, Response.NO_CONTENT
    return seat_doc.to_dict(), Response.OK


@app.route('/seats/<seat>', methods=['POST', 'PUT'])
async def set_seat(seat):
    """
    Set seat's value in request body's key: value accordingly, merge if exists.

    **!!!Additional keys are added!!!**

    :param seat:
    :return:
    """
    seat_doc_ref = db.collection(SEATS_COLLECTION).document(seat)
    seat_doc = seat_doc_ref.get()
    data = json2dict(request.data)
    if not seat_doc.exists:
        seat_doc_ref.set(data, merge=True)
        seat_doc = seat_doc_ref.get()
        return seat_doc.to_dict(), Response.CREATED
    seat_doc_ref.set(data, merge=True)
    seat_doc = seat_doc_ref.get()
    return seat_doc.to_dict(), Response.OK


@app.route('/seats/<seat>', methods=['PATCH'])
async def update_seat(seat):
    """
    Update seat's value in request body's key: value accordingly, merge if exists.

    :param seat:
    :return:
    """
    seat_doc_ref = db.collection(SEATS_COLLECTION).document(seat)
    seat_doc = seat_doc_ref.get()
    data = {k: v for k, v in json2dict(request.data).items() if
            k in seat_doc.to_dict()} if seat_doc.exists else json2dict(request.data)
    if not seat_doc.exists:
        seat_doc_ref.set(data, merge=True)
        seat_doc = seat_doc_ref.get()
        return seat_doc.to_dict(), Response.CREATED
    seat_doc_ref.set(data, merge=True)
    seat_doc = seat_doc_ref.get()
    return seat_doc.to_dict(), Response.OK


@app.route('/seats', methods=['DELETE'])
async def delete_seats():
    data = json2dict(request.data)
    return_dict = {}
    if not data or data.get('seats') is None:
        return {}, Response.BAD_REQUEST
    for seat_id in data.get('seats'):
        seat_doc_ref = db.collection(SEATS_COLLECTION).document(seat_id)
        seat_doc = seat_doc_ref.get()
        if seat_doc.exists:
            seat_doc_ref.delete()
            return_dict[seat_id] = (seat_doc.to_dict())
    return return_dict, Response.OK


@app.route('/seats/<seat>', methods=['DELETE'])
async def delete_seat(seat):
    seat_doc_ref = db.collection(SEATS_COLLECTION).document(seat)
    seat_doc = seat_doc_ref.get()
    if not seat_doc.exists:
        return {}, Response.NO_CONTENT
    seat_doc_ref.delete()
    return seat_doc.to_dict(), Response.OK


# @celery.task()
# def background():
#     return


if __name__ == '__main__':
    app.run(debug=True)
