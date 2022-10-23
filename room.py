class Room:
    def __init__(self) :
        self.__all_users = []
        self.__all_seats = []

        return

    @property
    def room(self):
        return {
            'users': self.__all_users,
            'seats': self.__all_seats
        }

    @property
    def occupied_user_size(self):
        return len(self.__all_users)

    @property
    def occupied_seat_size(self):
        return len(self.__all_seats)

    @property
    def all_users(self):
        return self.__all_users

    @all_users.setter
    def all_users(self, value):
        self.__all_users = value
        return

    @property
    def all_seats(self):
        return self.__all_seats

    @all_seats.setter
    def all_seats(self, value):
        self.__all_seats = value
        return

    def insert_user(self, user):
        if user in self.__all_users:
            return False
        self.__all_users.append(user)
        return True

    def remove_user(self, user):
        if user in self.__all_users:
            self.__all_users.remove(user)
            return True
        return False

    def occupy_seat(self, seat):
        if seat in self.__all_seats:
            return False
        self.__all_seats.append(seat)
        return True

    def unoccupy_seat(self, seat):
        if seat in self.__all_seats:
            self.__all_seats.remove(seat)
            return True
        return False

    def __str__(self):
        return str(self.room)

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return self.occupied_seat_size


class Library:
    def __init__(self):
        new_room_1 = Room()
        new_room_2 = Room()
        self.__floors = {
            '1': new_room_1,
            '2': new_room_2
        }
        return

    @property
    def floors(self):
        return self.__floors

    @property
    def floor_1(self):
        return self.__floors.get('1')

    @property
    def floor_2(self):
        return self.__floors.get('2')

    @property
    def occupied_user_size(self):
        return sum([e.occupied_user_size for e in self.__floors.values()])

    @property
    def occupied_seat_size(self):
        return sum([e.occupied_seat_size for e in self.__floors.values()])


if __name__ == '__main__':
    eng_lib = Library()
    eng_lib.floor_1.insert_user('1000')
    eng_lib.floor_1.insert_user('1001')
    eng_lib.floor_1.occupy_seat('x1')
    eng_lib.floor_1.occupy_seat('x2')
    eng_lib.floor_1.occupy_seat('x3')
    eng_lib.floor_1.occupy_seat('x3')
    print(eng_lib.floor_1.room)
    print(eng_lib.floor_2.room)
