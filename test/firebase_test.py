from firebase_admin import credentials
from firebase_admin import firestore
from unit import User
from unit import Seat
import firebase_admin as fb
import json
import os
import tools

cred = credentials.Certificate(os.path.abspath('../credentials/seat-booking-db-firebase-adminsdk-4e0g2-518adfa3cc.json'))
app_fb = fb.initialize_app(cred)
db = firestore.client()

if __name__ == '__main__':
    user_doc_ref = db.collection('users').document('6430000022')
    user_collection_stream = db.collection('users').stream()
    # did = {
    #     'id': '6430000021',
    #     'friends': ['6430000{}21'.format(i) for i in range(1, 10)],
    #     'status': 2,
    #     'current_seat_id': 'NO_SEAT'
    # }
    # user_doc_ref.set(did)

    user_doc = user_doc_ref.get()

    print(user_doc.exists)
    print(user_doc.to_dict())

    for user in user_collection_stream:
        print(user.id, user.to_dict())
    pass
