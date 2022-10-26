from firebase_admin import credentials
from firebase_admin import firestore
import firebase_admin as fb
import os
import datetime
import random
from names import names

random.seed(777778)

cred_path = '../credentials/seat-booking-db-firebase-adminsdk-4e0g2-518adfa3cc.json'
cred = credentials.Certificate(os.path.join(os.path.dirname(__file__), cred_path))
app_fb = fb.initialize_app(cred)
db = firestore.client()

list_seats = [
    'F1-' + str(e) for e in ['A{}'.format(str(i).zfill(2)) for i in range(1, 9)] +
    ['B{}'.format(str(i).zfill(2)) for i in range(1, 9)] +
    ['C{}'.format(str(i).zfill(2)) for i in range(1, 65)]
]

list_users = [
    '{}'.format(str(k).zfill(3)) for k in range(1, 101)
]

if __name__ == '__main__':
    for user_id in list_users:
        name = random.choice(names) + ' ' + random.choice(names)
        u = {
            'id': user_id,
            'name': name,
            'friends': [friend for friend in random.choices(list_users, k=4) if friend != user_id],
            'status': 0,
            'current_seat_id': '',
            'booked_time': datetime.datetime.now(),
            'temp_time': '',
            'extend_time': '',
            'caption': '',
            'whatsup': ''
        }
        user_doc_ref = db.collection('users').document(user_id)
        user_doc_ref.set(u)
        print(u)

    for seat_id in list_seats:
        s = {
            'id': seat_id,
            'status': 0,
            'seat_user': '',
            'booked_time': datetime.datetime.now(),
        }
        user_doc_ref = db.collection('seat').document(seat_id)
        user_doc_ref.set(s)
        print(s)
