from firebase_admin import credentials
from firebase_admin import firestore
import firebase_admin as fb
import os
import datetime
import random
from names import names

random.seed(777778)

cred = credentials.Certificate(os.path.join(os.path.dirname(__file__),
                                            '../credentials/seat-booking-db-firebase-adminsdk-4e0g2-518adfa3cc.json'))
app_fb = fb.initialize_app(cred)
db = firestore.client()

if __name__ == '__main__':
    for k in range(1, 81):
        sid = '643{}21'.format(str(k).zfill(5))
        name = random.choice(names) + ' ' + random.choice(names)
        u = {
            'id': sid,
            'name': name,
            'friends': ['643{}21'.format(str(i).zfill(5)) for i in random.choices(range(1, 81), k=8) if i != k],
            'status': 0,
            'current_seat_id': '',
            'booked_time': datetime.datetime.now(),
            'temp_time': datetime.datetime.now(),
            'unique_id': hash(sid)
        }
        user_doc_ref = db.collection('users').document(sid)
        user_doc_ref.set(u)
        print(u)
