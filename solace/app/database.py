# from Thriftstore import *
from acct_mgmt_classes import User
from models.Thriftstore import Thriftstore

u1 = User(1, "bob", "bob@gmail.com", "91234567", "yourmother123???", "2001-11-09","male", "paya lebar road 1", "4102920199126573")
u2 = User(2, "jack", "jack@gmail.com", "92345678", "yourfather123???", "2009-06-18","female", "yishun road 3", "4863726493419090")

usersTableAttributes = '''
    user_id INTEGER PRIMARY KEY,
    name TEXT, 
    email TEXT, 
    phone_number TEXT, 
    password TEXT, 
    birthday TEXT, 
    gender TEXT,
    addresses TEXT, 
    card_details TEXT 
''' 

user_insert_query = '''INSERT INTO Users(
    user_id,
    name,
    email,
    phone_number,
    password,
    birthday,
    gender,
    addresses,
    card_details)
    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);
'''

user_update_query = '''"UPDATE Users 
SET name = ?,
    email = ?,
    phone_number = ?,
    password = ?,
    birthday = ?,
    gender = ?,
    addresses = ?,
    card_details = ?,
    WHERE user_id = ?"
'''

db = Thriftstore()
db.create_table("Users", usersTableAttributes)

db.insert_into_table(user_insert_query, u1)
db.insert_into_table(user_insert_query, u2)

db.drop_table('inquiry')
db.drop_table("faq")

db.close_connection()