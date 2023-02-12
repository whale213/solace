from models.Thriftstore import Thriftstore
from acct_mgmt_classes import User

u1 = User("bob", "bobLee@gmail.com", "91234567", "yourmother123???", "2001-11-09","male", "paya lebar road 1", "4102920199126573")
u2 = User("jack", "jackTyson@gmail.com", "92345678", "yourfather123???", "2009-06-18","female", "yishun road 3", "4863726493419090")

usersTableAttributes = '''
    user_id INTEGER PRIMARY KEY, 
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone_number TEXT NOT NULL, 
    password TEXT NOT NULL,
    birthday TEXT NOT NULL, 
    gender TEXT NOT NULL,
    addresses TEXT NOT NULL,
    card_details TEXT NOT NULL
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

# user_update_query = f'''UPDATE Users 
# SET name = ?,
#     email = ?, 
#     phone_number = ?, 
#     password = ?, 
#     birthday = ?, 
#     gender = ?, 
#     addresses = ?, 
#     card_details = ?, 
#     WHERE user_id = ?"
# '''



db = Thriftstore()

db.create_table("Users", usersTableAttributes)

db.insert_into_table(user_insert_query, u1)
db.insert_into_table(user_insert_query, u2)


db.close_connection()