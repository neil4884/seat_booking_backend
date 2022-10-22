from flask import Flask, request
from celery import Celery
from firebase_admin import credentials
from firebase_admin import firestore
from tools import Response
from tools import json2dict
from tools import make_celery
from unit import User
from unit import Seat
import firebase_admin as fb
import json
import os
import asyncio

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
    if not data:
        users_collection_stream = db.collection(USERS_COLLECTION).stream()
        users = {user.id: user.to_dict() async for user in users_collection_stream}
        if not users:
            return {}, Response.NO_CONTENT
        return users, Response.OK

    return_dict = {}
    async for user_id in data.get('users'):
        user_doc_ref = db.collection(USERS_COLLECTION).document(user_id)
        user_doc = await user_doc_ref.get()
        if user_doc.exist:
            return_dict[user_id] = user_doc.to_dict

    return return_dict, (Response.OK if return_dict else Response.NO_CONTENT)


@app.route('/users/<user>', methods=['GET'])
async def get_user(user):
    """
    Get one user's data. Return dictionary of user data and OK if exists, else NO_CONTENT

    :param user:
    :return:
    """
    user_doc_ref = db.collection(USERS_COLLECTION).document(user)
    user_doc = await user_doc_ref.get()
    if not user_doc.exist:
        return {}, Response.NO_CONTENT
    return user_doc.to_dict(), Response.OK


@app.route('/users/<user>', methods=['POST', 'PUT', 'PATCH'])
async def set_user(user):
    """
    Set user's value in request body's key: value accordingly, merge if exists.

    :param user:
    :return:
    """
    user_doc_ref = db.collection(USERS_COLLECTION).document(user)
    user_doc = await user_doc_ref.get()
    data = {k: v for k, v in json2dict(request.data).items() if
            k in user_doc.to_dict()} if user_doc.exist else json2dict(request.data)
    if not user_doc.exist:
        await user_doc_ref.set(data, merge=True)
        user_doc = await user_doc_ref.get()
        return user_doc.to_dict(), Response.CREATED
    await user_doc_ref.set(data, merge=True)
    user_doc = await user_doc_ref.get()
    return user_doc.to_dict(), Response.OK


@app.route('/users', methods=['DELETE'])
async def delete_users():
    data = json2dict(request.data)
    return_dict = {}
    async for user_id in data.get('users'):
        user_doc_ref = db.collection(USERS_COLLECTION).document(user_id)
        user_doc = await user_doc_ref.get()
        if user_doc.exist:
            await user_doc_ref.delete()
            return_dict[user_id] = (user_doc.to_dict())
    return {}, Response.OK


@app.route('/users/<user>', methods=['DELETE'])
async def delete_user(user):
    user_doc_ref = db.collection(USERS_COLLECTION).document(user)
    user_doc = await user_doc_ref.get()
    if not user_doc.exist:
        return {}, Response.NO_CONTENT
    await user_doc_ref.delete()
    return user_doc.to_dict, Response.OK


################ SEAT QUERY ##################


# @celery.task()
# def background():
#     return


if __name__ == '__main__':
    app.run(debug=True)
