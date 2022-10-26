from http.client import OK
from http.cookies import BaseCookie
from urllib import response
from webbrowser import get
from flask import Flask
from flask import request
from firebase_admin import credentials
from firebase_admin import firestore
from requests import ReadTimeout
from tools import Response, time_now
from tools import json2dict
from config import *
import flask
import tools
import firebase_admin as fb
import os
import asyncio
import threading
import room

# Override fast loop interval (default=1)
# LOOP_1_INTERVAL = 1

# Override slow loop interval (default=10)
# LOOP_2_INTERVAL = 2

cred = credentials.Certificate(os.path.join(os.path.dirname(__file__), CREDENTIAL_PATH))
app_fb = fb.initialize_app(cred)
db = firestore.client()
app = Flask(__name__)

f1_ocpd_seats = 0
f2_ocpd_seats = 0
all_ocpd_seats = 0
my_library = room.Library()  # Library with 2 floors, view usages in lib.
all_users = None


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
        return

    @staticmethod
    async def book(user: str, seat: str):
        user_ref = (await get_user(user))[0]
        user_status = user_ref.get('status')
        if user_status == 0:
            my_library.insert_booked_user(user, tools.time_now())
            await update_user(user, {
                'status': 3,
                'current_seat_id': seat,
                'booked_time': tools.time_now()
            })
            await update_seat(seat, {
                'status': 1,
                'seat_user': user
            })
            return {}, Response.CREATED
        elif user_status in (1, 3):
            await Command.remove_user(user)
            await update_user(user, {
                'status': 3,
                'current_seat_id': seat,
                'booked_time': tools.time_now()
            })
            await update_seat(seat, {
                'status': 1,
                'seat_user': user
            })
            if user_status == 1:
                # Automatically change seat and re-check in (user already checked in)
                await Command.check_in(user)
            elif user_status == 2:
                # EXTEND_TIME IS DURATION OF THAT TIME WAS EXTENDED// TIME STAMP OR INT?
                my_library.insert_extend_user(user, tools.time_now(), user_ref.get('extend_time'))
            elif user_status == 3:
                my_library.insert_booked_user(user, tools.time_now())
            return {}, Response.CREATED
        return {}, Response.BAD_REQUEST

    @staticmethod
    async def remove_user(user: str):
        user_ref = (await get_user(user))[0]
        seat_id = user_ref.get('current_seat_id')

        my_library.remove_extend_user(user)
        my_library.remove_booked_user(user)

        if not user_ref:
            return {}, Response.NO_CONTENT
        seat = user_ref.get('current_seat_id')
        if seat[:3] == 'F01':
            my_library.floor_1.remove_user(user)
            my_library.floor_1.unoccupy_seat(seat)
        elif seat[:3] == 'F02':
            my_library.floor_2.remove_user(user)
            my_library.floor_2.unoccupy_seat(seat)
        await update_user(user, {
            'status': 0,
            'current_seat_id': ''
        })
        await update_seat(user_ref.get('current_seat_id'), {
            'status': 0,
            'seat_user': ''
        })

        return {}, Response.OK

    @staticmethod
    async def remove_users(users: list):
        for user in users:
            await Command.remove_user(user)
        return {}, Response.OK

    @staticmethod
    async def remove_seat(seat: str):
        seat_ref = (await get_seat(seat))[0]
        if not seat_ref:
            return {}, Response.NO_CONTENT
        user = seat_ref.get('seat_user')
        if seat[:3] == 'F01':
            my_library.floor_1.remove_user(user)
            my_library.floor_1.unoccupy_seat(seat)
        elif seat[:3] == 'F02':
            my_library.floor_2.remove_user(user)
            my_library.floor_2.unoccupy_seat(seat)
        user = seat_ref.get('seat_user')

        my_library.remove_extend_user(user)
        my_library.remove_booked_user(user)

        await update_user(seat_ref.get('seat_user'), {
            'status': 0,
            'current_seat_id': ''
        })
        await update_seat(seat, {
            'status': 0,
            'seat_user': ''
        })
        return {}, Response.OK

    @staticmethod
    async def remove_seats(seats: list):
        for seat in seats:
            await Command.remove_seat(seat)
        return {}, Response.OK

    @staticmethod
    async def check_in(user: str):
        user_ref = (await get_user(user))[0]
        if user_ref.get('status') == 3 and user_ref.get('current_seat_id'):
            seat_id = user_ref.get('current_seat_id')
            # my_library.remove_extend_user(user)
            my_library.remove_booked_user(user)
            if seat_id[:3] == 'F01':
                my_library.floor_1.insert_user(user)
                my_library.floor_1.occupy_seat(seat_id)
            else:
                my_library.floor_2.insert_user(user)
                my_library.floor_2.occupy_seat(seat_id)
            return await update_user(user, {
                'status': 1
            })
        return {}, Response.BAD_REQUEST

    @staticmethod
    async def check_out(user: str = None, seat: str = None):
        if user is not None and seat is not None:
            raise Exception('Input either user or seat, not both.')
        try:
            if user is not None:
                return await Command.remove_user(user=user)
            elif seat is not None:
                return await Command.remove_seat(seat=seat)
        except Exception:
            pass
        return {}, Response.BAD_REQUEST

    @staticmethod
    async def check_book_timeout():
        for user, booked_time in my_library.booked_users:
            booked_datetime = tools.to_datetime(booked_time)
            time_diff = tools.time_now() - booked_datetime
            if time_diff.total_seconds() > 300:
                my_library.remove_booked_user(user)
                await Command.remove_user(user)

    @staticmethod
    async def check_extend_timeout():
        for user, extend_prop in my_library.extend_users:
            extend_datetime = tools.to_datetime(extend_prop[0])
            time_diff = tools.time_now() - extend_datetime
            if time_diff.total_seconds() > extend_prop[1]:
                my_library.remove_extend_user(user)
                await Command.remove_user(user)

    @staticmethod
    async def add_friend(user,friend,unique_id):
        if (tools.generate_hash(friend)==unique_id):
            return {},Response.OK   
        return {},Response.BAD_REQUEST

    @staticmethod
    async def remove_friend(user,friend):
        user_ref = (await get_user(user))[0]
        if friend in user_ref.get('friends'):
            return {},Response.OK   
        return {},Response.BAD_REQUEST
# ####################### INSERT BACKGROUND TASKS HERE, E.G. CHECKING SOMETHING EVERY 1 S ########################


async def run_once_background_tasks(*args, **kwargs):
    global all_users
    all_users = [u for u in (await get_users)[0].keys()]
    return


async def background_tasks_fast(cmd_instance: Command):
    # print('Running fast tasks in the background...')
    # print('Instance id =', cmd_instance.instance_id)
    # library = await get_user('6430000521')
    # await update_user('6430000521', {'friends': []})
    # print(library)
    return


async def background_tasks_slow(cmd_instance: Command):
    # print('Running slow tasks in the background...')
    # print('Instance id =', cmd_instance.instance_id)
    # library = await get_user('6430000521')
    # await update_user('6430000521', {'friends': []})
    # print(library)
    return


# ####################### CUSTOM COMMAND FROM FRONTEND QUERY ########################

@app.route('/api/custom/<command>', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
async def run_cmd(command):
    """
    Custom command

    :param command:
    :return:
    """
    q = json2dict(request.data)

    if command == 'get_all_users':
        return await get_users()
    elif command == 'book':
        return Command.book(q.get('user'),q.get('seat'))
    elif command == 'remove_all_user':
        return Command.remove_users()
    elif command == 'remove_user':
        return Command.remove_user(q.get('user'))
    elif command == 'remove_all_seats':
        return Command.remove_seats
    elif command == 'remove_seat':
        return Command.remove_seat(q.get('seat'))
    elif command == 'check_in':
        return Command.check_in(q.get('user'))
    elif command == 'check_out':
        return Command.check_out(q.get('user'),q.get('seat'))
    elif command == 'get_unique_id':
        return {'unique_id':tools.generate_hash()},Response.OK
    elif command == 'add_friend':
        pass
    elif command == 'remove_friend':
        pass

    return {}, Response.BAD_REQUEST


@app.route('/api/auth/secret/<user>', methods=['GET'])
async def get_secret(user):

    return {}, Response.UNAUTHORIZED


# ####################### TEMPLATE FOR THING QUERY ########################

async def get_things(*args, collection_name: str):
    if args:
        data = args[0]
    elif flask.has_request_context():
        data = json2dict(request.data).get(collection_name)
    else:
        data = None
    if data is None:
        things_collection_stream = db.collection(collection_name).stream()
        things = {thing.id: thing.to_dict() for thing in things_collection_stream}
        if not things:
            return {}, Response.NO_CONTENT
        return things, Response.OK

    return_dict = {}
    for thing_id in data:
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


async def set_thing(thing, /, *args, collection_name: str):
    thing_doc_ref = db.collection(collection_name).document(thing)
    thing_doc = thing_doc_ref.get()
    if args:
        data = args[0]
    else:
        data = json2dict(request.data)

    if not thing_doc.exists:
        thing_doc_ref.set(data, merge=True)
        thing_doc = thing_doc_ref.get()
        return thing_doc.to_dict(), Response.CREATED
    thing_doc_ref.set(data, merge=True)
    thing_doc = thing_doc_ref.get()
    return thing_doc.to_dict(), Response.OK


async def update_thing(thing, /, *args, collection_name: str):
    thing_doc_ref = db.collection(collection_name).document(thing)
    thing_doc = thing_doc_ref.get()
    if args:
        data = {k: v for k, v in args[0].items() if
                k in thing_doc.to_dict()} if thing_doc.exists else args[0]
    else:
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

@app.route('/api/users', methods=['GET'])
async def get_users(*args):
    """
    Get all users' data if request body is empty, users' data in request body's key "users". If there are no users
    in the database, and empty dictionary and NO_CONTENT is returned, otherwise list of users with id as key and OK
    is returned.

    :return:
    """
    return await get_things(*args, collection_name=USERS_COLLECTION)


@app.route('/api/users/<user>', methods=['GET'])
async def get_user(user):
    """
    Get one user's data. Return dictionary of user data and OK if exists, else NO_CONTENT

    :param user:
    :return:
    """
    return await get_thing(user, collection_name=USERS_COLLECTION)


@app.route('/api/users/<user>', methods=['POST', 'PUT'])
async def set_user(user, *args):
    """
    Set user's value in request body's key: value accordingly, merge if exists.

    **!!!Additional keys are added!!!**

    :param user:
    :return:
    """
    return await set_thing(user, *args, collection_name=USERS_COLLECTION)


@app.route('/api/users/<user>', methods=['PATCH'])
async def update_user(user, *args):
    """
    Update user's value in request body's key: value accordingly, merge if exists.

    :param user:
    :return:
    """
    return await update_thing(user, *args, collection_name=USERS_COLLECTION)


@app.route('/api/users', methods=['DELETE'])
async def delete_users():
    return await delete_things(collection_name=USERS_COLLECTION)


@app.route('/api/users/<user>', methods=['DELETE'])
async def delete_user(user):
    return await delete_thing(user, collection_name=USERS_COLLECTION)


# ####################### SEAT QUERY ########################

@app.route('/api/seats', methods=['GET'])
async def get_seats(*args):
    """
    Get all seats' data if request body is empty, seats' data in request body's key "seats". If there are no seats
    in the database, and empty dictionary and NO_CONTENT is returned, otherwise list of seats with id as key and OK
    is returned.

    :return:
    """
    return await get_things(*args, collection_name=SEATS_COLLECTION)


@app.route('/api/seats/<seat>', methods=['GET'])
async def get_seat(seat):
    """
    Get one seat's data. Return dictionary of seat data and OK if exists, else NO_CONTENT

    :param seat:
    :return:
    """
    return await get_thing(seat, collection_name=SEATS_COLLECTION)


@app.route('/api/seats/<seat>', methods=['POST', 'PUT'])
async def set_seat(seat, *args):
    """
    Set seat's value in request body's key: value accordingly, merge if exists.

    **!!!Additional keys are added!!!**

    :param seat:
    :return:
    """
    return await set_thing(seat, *args, collection_name=SEATS_COLLECTION)


@app.route('/api/seats/<seat>', methods=['PATCH'])
async def update_seat(seat, *args):
    """
    Update seat's value in request body's key: value accordingly, merge if exists.

    :param seat:
    :return:
    """
    return await update_thing(seat, *args, collection_name=SEATS_COLLECTION)


@app.route('/api/seats', methods=['DELETE'])
async def delete_seats():
    return await delete_things(collection_name=SEATS_COLLECTION)


@app.route('/api/seats/<seat>', methods=['DELETE'])
async def delete_seat(seat):
    return await delete_thing(seat, collection_name=SEATS_COLLECTION)


# ####################### SHUTDOWN QUERY (BETA) ########################

@app.route('/api/shutdown', methods=['GET'])
async def shutdown():
    passwd = request.args.get('auth')
    if passwd != 'haha':
        return {}, Response.UNAUTHORIZED
    return shutdown_server()


@app.route('/api')
async def api_test():
    return {'status_code': 1}, Response.OK


@app.route('/')
async def hello():
    return 'It worked!', Response.OK


def shutdown_server():
    # Currently do nothing...
    return {}, Response.ACCEPTED


# ####################### CONCURRENCY SETUP ########################

async def background_handler(once_task=None, loop_task=None, interval=LOOP_1_INTERVAL, instance_id=0):
    if callable(once_task):
        await once_task()
    if not callable(loop_task):
        print(loop_task, 'not callable.')
        return
    cmd_instance = Command()
    cmd_instance.instance_id = instance_id
    while True:
        await loop_task(cmd_instance)
        await asyncio.sleep(interval)


def setup_loop(loop_arg: asyncio.BaseEventLoop, handler, loop_task, interval, once_task=None, instance_id=0):
    asyncio.set_event_loop(loop_arg)
    loop_arg.run_until_complete(handler(once_task, loop_task, interval, instance_id))
    return


loop_1, loop_2 = asyncio.new_event_loop(), asyncio.new_event_loop()

concurrent_thread_1 = threading.Thread(target=setup_loop,
                                       args=(
                                           loop_1,
                                           background_handler,
                                           background_tasks_fast,
                                           LOOP_1_INTERVAL,
                                           run_once_background_tasks,
                                           1
                                       ),
                                       daemon=True)
concurrent_thread_1.start()

concurrent_thread_2 = threading.Thread(target=setup_loop,
                                       args=(
                                           loop_2,
                                           background_handler,
                                           background_tasks_slow,
                                           LOOP_2_INTERVAL,
                                           None,
                                           2
                                       ),
                                       daemon=True)
concurrent_thread_2.start()

if __name__ == '__main__':
    app.run(debug=False)
