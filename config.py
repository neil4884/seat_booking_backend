LOOP_INTERVAL = 1
USERS_COLLECTION = 'users'
SEATS_COLLECTION = 'seats'
CREDENTIAL_PATH = 'credentials/seat-booking-db-firebase-adminsdk-4e0g2-518adfa3cc.json'


class Config:
    @staticmethod
    def set_loop_interval(interval):
        global LOOP_INTERVAL
        LOOP_INTERVAL = interval
