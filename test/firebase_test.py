from firebase_admin import credentials
from firebase_admin import firestore
import firebase_admin as fb
import os
import datetime

cred = credentials.Certificate(
    os.path.abspath('../credentials/seat-booking-db-firebase-adminsdk-4e0g2-518adfa3cc.json'))
app_fb = fb.initialize_app(cred)
db = firestore.client()

if __name__ == '__main__':
    for k in range(1, 1001):
        id = '643{}21'.format(str(k).zfill(5))
        did = {
            'id': id,
            'friends': ['643{}21'.format(str(i).zfill(5)) for i in range(1, 11) if i != k],
            'status': 0,
            'current_seat_id': 'NO_SEAT',
            'check_in_time': datetime.datetime.now(),
            'check_out_time': datetime.datetime.now()
        }
        user_doc_ref = db.collection('users').document(id)
        user_doc_ref.set(did)
        print(id)

    for k in range(1, 51):
        id = 'F01A{}'.format(str(k).zfill(3))
        did = {
            'id': id,
            'status': 0,
            'caption': '',
            'book_time': datetime.datetime.now(),
            'seat_user': '643{}21'.format(str(400 - k).zfill(5))
        }
        seat_doc_ref = db.collection('seats').document(id)
        seat_doc_ref.set(did)
        print(id)

    for k in range(51, 101):
        id = 'F02A{}'.format(str(k).zfill(3))
        did = {
            'id': id,
            'status': 0,
            'caption': '',
            'book_time': datetime.datetime.now(),
            'seat_user': '643{}21'.format(str(800 - k).zfill(5))
        }
        seat_doc_ref = db.collection('seats').document(id)
        seat_doc_ref.set(did)
        print(id)
