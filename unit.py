class User:
    def __init__(self):
        self.__id = ''
        self.__friends = []
        self.__status = 0
        self.__seat_id = ''

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
    def __init__(self):
        self.__seat_id = ''
        self.__status = 0
        self.__caption = ''

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
