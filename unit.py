class User:
    def __init__(self, id='', friends=None, status=0, seat_id=''):
        if friends is None:
            friends = []
        self.__id = id
        self.__friends = friends
        self.__status = status
        self.__seat_id = seat_id
        return

    @property
    def user(self):
        return {
            'id': self.id,
            'friends': self.friends,
            'status': self.status,
            'current_seat_id': self.seat_id
        }

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = value

    @property
    def friends(self):
        return self.__friends

    @friends.setter
    def friends(self, value):
        self.__friends = value

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        self.__status = value

    @property
    def seat_id(self):
        return self.__seat_id

    @seat_id.setter
    def seat_id(self, value):
        self.__seat_id = value


class Seat:
    def __init__(self, seat_id='', status=0, caption=''):
        self.__seat_id = seat_id
        self.__status = status
        self.__caption = caption

    @property
    def seat_id(self):
        return self.__seat_id

    @seat_id.setter
    def seat_id(self, value):
        self.__seat_id = value
        return

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        self.__status = value
        return

    @property
    def caption(self):
        return self.__caption

    @caption.setter
    def caption(self, value):
        self.__caption = value


if __name__ == '__main__':
    seat = Seat()
    user = User()
    seat.id = 'xx'
    print(seat.id)
    user.friends.append('xxz')
    print(user.friends)


