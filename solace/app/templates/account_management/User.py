# User class
class User:
    count_id = 0

    # initializer method
    def __init__(self, first_name, last_name, email, phone_number, password, birthday, gender, address, card):
        User.count_id += 1
        self.__user_id = User.count_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__email = email
        self.__phone_number = phone_number
        self.__password = password
        self. __birthday = birthday
        self.__gender = gender
        self.__address = address
        self.__card = card

    # accessor methods
    def get_user_id(self):
        return self.__user_id

    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name

    def get_email(self):
        return self.__email

    def get_phone_number(self):
        return self.__phone_number

    def get_password(self):
        return self.__password

    def get_birthday(self):
        return self.__birthday

    def get_gender(self):
        return self.__gender

    def get_address(self):
        return self.__address

    def get_card(self):
        return self.__card

    # mutator methods
    def set_user_id(self, user_id):
        self.__user_id = user_id

    def set_first_name(self, first_name):
        self.__first_name = first_name

    def set_last_name(self, last_name):
        self.__last_name = last_name

    def set_phone_number(self, phone_number):
        self.__phone_number = phone_number

    def set_password(self, password):
        self.__password = password

    def set_user_id(self, user_id):
        self.__user_id = user_id

    def set_first_name(self, first_name):
        self.__first_name = first_name

    def set_last_name(self, last_name):
        self.__last_name = last_name

    def set_gender(self, gender):
        self.__gender = gender

    def set_birthday(self, birthday):
        self.__birthday = birthday

    def set_gender(self, gender):
        self.__gender = gender

    def set_address(self, address):
        self.__address = address

    def set_card(self, card):
        self.__card = card
