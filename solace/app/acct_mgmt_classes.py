class User:

    # initializer method
    def __init__(self, name, email, phone_number, password, birthday, gender, addresses, card_details):
        self.__name = name
        self.__email = email
        self.__phone_number = phone_number
        self.__password = password
        self.__birthday = birthday
        self.__gender = gender
        self.__addresses = addresses
        self.__card_details = card_details
    
    # accessor methods
    def get_name(self):
        return self.__name

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

    def get_addresses(self):
        return self.__addresses

    def get_card_details(self):
        return self.__card_details
    
    # mutator methods

    def set_name(self, name):
        self.__name = name

    def set_email(self, email):
        self.__email = email

    def set_phone_number(self, phone_number):
        self.__phone_number = phone_number

    def set_password(self, password):
        self.__password = password

    def set_birthday(self, birthday):
        self.__birthday = birthday

    def set_gender(self, gender):
        self.__gender = gender

    def set_addresses(self, addresses):
        self.__addresses = addresses

    def set_card_details(self, card_details):
        self.__card_details = card_details