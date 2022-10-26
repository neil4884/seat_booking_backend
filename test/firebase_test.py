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
    for k in range(1, 101):
        sid = '643{}21'.format(str(k).zfill(5))
        did = {
            'id': sid,
            'friends': ['643{}21'.format(str(i).zfill(5)) for i in range(1, 11) if i != k],
            'status': 0,
            'current_seat_id': 'NO_SEAT',
            'check_in_time': datetime.datetime.now(),
            'check_out_time': datetime.datetime.now(),
            'caption': ''
        }
        user_doc_ref = db.collection('users').document(sid)
        user_doc_ref.set(did)
        print(sid)

    for k in range(1, 51):
        sid = 'F01A{}'.format(str(k).zfill(3))
        did = {
            'id': sid,
            'status': 0,
            'book_time': datetime.datetime.now(),
            'seat_user': ''
        }
        seat_doc_ref = db.collection('seats').document(sid)
        seat_doc_ref.set(did)
        print(sid)

