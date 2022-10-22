from flask import Flask, request
from firebase_admin import credentials
from firebase_admin import firestore
from tools import Response
from tools import json2dict
from config import *
# from tools import make_celery
# from unit import User
# from unit import Seat
import firebase_admin as fb
# import json
import os
import asyncio
import threading

cred = credentials.Certificate(os.path.abspath(CREDENTIAL_PATH))
app_fb = fb.initialize_app(cred)
db = firestore.client()
app = Flask(__name__)


# ####################### BACKEND COMMAND HERE ########################

class Command:
    def __init__(self, instance_id=0):
        self.__instance_id = instance_id
        return

    @property
    def instance_id(self):
        return self.__instance_id

    @instance_id.setter
    def instance_id(self, value):
        self.__instance_id = value

    # Insert commands below
    @staticmethod
    async def remove_user_from_seat(*, user=None, seat=None):
        if user is not None and seat is not None:
            raise Exception('Input either user or seat, not both.')
        if user is not None:
            pass
        if seat is not None:
            pass
        return


# ####################### INSERT BACKGROUND TASKS HERE, E.G. CHECKING SOMETHING EVERY 1 S ########################

async def background_tasks(instance: Command):
    print('Running some tasks in the background...')
    print('Instance id =', instance.instance_id)
    return


# ####################### CUSTOM COMMAND FROM FRONTEND QUERY ########################

@app.route('/custom/<command>', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
async def run_cmd(command):
    """
    Custom command

    :param command:
    :return:
    """
    query_args = request.args.get('args')
    query = [] if not query_args or query_args is None else query_args.strip().split(',')
    del query_args
    if command == 'get_all_users':
        return await get_users()

    return {}, Response.BAD_REQUEST


# ####################### TEMPLATE FOR THING QUERY ########################

async def get_things(collection_name: str):
    data = json2dict(request.data)
    if not data or data.get(collection_name) is None:
        things_collection_stream = db.collection(collection_name).stream()
        things = {thing.id: thing.to_dict() for thing in things_collection_stream}
        if not things:
            return {}, Response.NO_CONTENT
        return things, Response.OK

    return_dict = {}
    for thing_id in data.get(collection_name):
        thing_doc_ref = db.collection(collection_name).document(thing_id)
        thing_doc = thing_doc_ref.get()
        if thing_doc.exists:
            return_dict[thing_id] = thing_doc.to_dict()

    return return_dict, (Response.OK if return_dict else Response.NO_CONTENT)


async def get_thing(thing, /, collection_name: str):
    thing_doc_ref = db.collection(collection_name).document(thing)
    thing_doc = thing_doc_ref.get()
    if not thing_doc.exists:
        return {}, Response.NO_CONTENT
    return thing_doc.to_dict(), Response.OK


async def set_thing(thing, /, collection_name: str):
    thing_doc_ref = db.collection(collection_name).document(thing)
    thing_doc = thing_doc_ref.get()
    data = json2dict(request.data)
    if not thing_doc.exists:
        thing_doc_ref.set(data, merge=True)
        thing_doc = thing_doc_ref.get()
        return thing_doc.to_dict(), Response.CREATED
    thing_doc_ref.set(data, merge=True)
    thing_doc = thing_doc_ref.get()
    return thing_doc.to_dict(), Response.OK


async def update_thing(thing, /, collection_name: str):
    thing_doc_ref = db.collection(collection_name).document(thing)
    thing_doc = thing_doc_ref.get()
    data = {k: v for k, v in json2dict(request.data).items() if
            k in thing_doc.to_dict()} if thing_doc.exists else json2dict(request.data)
    if not thing_doc.exists:
        thing_doc_ref.set(data, merge=True)
        thing_doc = thing_doc_ref.get()
        return thing_doc.to_dict(), Response.CREATED
    thing_doc_ref.set(data, merge=True)
    thing_doc = thing_doc_ref.get()
    return thing_doc.to_dict(), Response.OK


async def delete_things(collection_name: str):
    data = json2dict(request.data)
    return_dict = {}
    if not data or data.get(collection_name) is None:
        return {}, Response.BAD_REQUEST
    for thing_id in data.get(collection_name):
        thing_doc_ref = db.collection(collection_name).document(thing_id)
        thing_doc = thing_doc_ref.get()
        if thing_doc.exists:
            thing_doc_ref.delete()
            return_dict[thing_id] = (thing_doc.to_dict())
    return return_dict, Response.OK


async def delete_thing(thing, /, collection_name: str):
    thing_doc_ref = db.collection(collection_name).document(thing)
    thing_doc = thing_doc_ref.get()
    if not thing_doc.exists:
        return {}, Response.NO_CONTENT
    thing_doc_ref.delete()
    return thing_doc.to_dict(), Response.OK


# ####################### USER QUERY ########################

@app.route('/users', methods=['GET'])
async def get_users():
    """
    Get all users' data if request body is empty, users' data in request body's key "users". If there are no users
    in the database, and empty dictionary and NO_CONTENT is returned, otherwise list of users with id as key and OK
    is returned.

    :return:
    """
    return await get_things(collection_name=USERS_COLLECTION)


@app.route('/users/<user>', methods=['GET'])
async def get_user(user):
    """
    Get one user's data. Return dictionary of user data and OK if exists, else NO_CONTENT

    :param user:
    :return:
    """
    return await get_thing(user, collection_name=USERS_COLLECTION)


@app.route('/users/<user>', methods=['POST', 'PUT'])
async def set_user(user):
    """
    Set user's value in request body's key: value accordingly, merge if exists.

    **!!!Additional keys are added!!!**

    :param user:
    :return:
    """
    return await set_thing(user, collection_name=USERS_COLLECTION)


@app.route('/users/<user>', methods=['PATCH'])
async def update_user(user):
    """
    Update user's value in request body's key: value accordingly, merge if exists.

    :param user:
    :return:
    """
    return await update_thing(user, collection_name=USERS_COLLECTION)


@app.route('/users', methods=['DELETE'])
async def delete_users():
    return await delete_things(collection_name=USERS_COLLECTION)


@app.route('/users/<user>', methods=['DELETE'])
async def delete_user(user):
    return await delete_thing(user, collection_name=USERS_COLLECTION)


# ####################### SEAT QUERY ########################

@app.route('/seats', methods=['GET'])
async def get_seats():
    """
    Get all seats' data if request body is empty, seats' data in request body's key "seats". If there are no seats
    in the database, and empty dictionary and NO_CONTENT is returned, otherwise list of seats with id as key and OK
    is returned.

    :return:
    """
    return await get_things(collection_name=SEATS_COLLECTION)


@app.route('/seats/<seat>', methods=['GET'])
async def get_seat(seat):
    """
    Get one seat's data. Return dictionary of seat data and OK if exists, else NO_CONTENT

    :param seat:
    :return:
    """
    return await get_thing(seat, collection_name=SEATS_COLLECTION)


@app.route('/seats/<seat>', methods=['POST', 'PUT'])
async def set_seat(seat):
    """
    Set seat's value in request body's key: value accordingly, merge if exists.

    **!!!Additional keys are added!!!**

    :param seat:
    :return:
    """
    return await set_thing(seat, collection_name=SEATS_COLLECTION)


@app.route('/seats/<seat>', methods=['PATCH'])
async def update_seat(seat):
    """
    Update seat's value in request body's key: value accordingly, merge if exists.

    :param seat:
    :return:
    """
    return await update_thing(seat, collection_name=SEATS_COLLECTION)


@app.route('/seats', methods=['DELETE'])
async def delete_seats():
    return await delete_things(collection_name=SEATS_COLLECTION)


@app.route('/seats/<seat>', methods=['DELETE'])
async def delete_seat(seat):
    return await delete_thing(seat, collection_name=SEATS_COLLECTION)


# ####################### SHUTDOWN QUERY (BETA) ########################

@app.route('/shutdown', methods=['GET'])
async def shutdown():
    passwd = request.args.get('auth')
    if passwd != 'haha':
        return {}, Response.UNAUTHORIZED
    return shutdown_server()


def shutdown_server():
    # Currently do nothing...
    return {}, Response.ACCEPTED


# ####################### CONCURRENCY SETUP ########################

async def background_handler(loop_f=background_tasks, interval=LOOP_INTERVAL):
    cmd_instance = Command()
    while True:
        await loop_f(cmd_instance)
        await asyncio.sleep(interval)


def setup_loop(loop_arg: asyncio.BaseEventLoop):
    asyncio.set_event_loop(loop_arg)
    loop_arg.run_until_complete(background_handler())
    return


loop = asyncio.new_event_loop()
concurrent_thread = threading.Thread(target=setup_loop, args=(loop,), daemon=True)
concurrent_thread.start()

if __name__ == '__main__':
    app.run(debug=False)
