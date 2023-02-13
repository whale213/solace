from Thriftstore import *


reportTableAttributes = '''
    Order_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Gender CHAR(2) NOT NULL,
    Date TEXT NOT NULL,
    Items INTEGER NOT NULL,
    Total_Cost TEXT NOT NULL
    '''

db = Thriftstore()
db.create_table('customerinfo', reportTableAttributes)

db.close_connection()