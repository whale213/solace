from models.Thriftstore import Thriftstore
import sqlite3

class FAQ:

    def __init__(self, category, question, answer) -> None:
        self.__category = category
        self.__question = question
        self.__answer =  answer
        
f1 = FAQ('Shipping & Handling', 'How are our products packed?', 'We iron and steam our products before shipping them out')
f2 = FAQ('Shipping & Handling', 'What if our products get lost in shipping?', 'Once you contact us, we will try to replace the products or give you back your money as compensation.')
f3 = FAQ('Clothes Donation', 'Who do you donate clothes to?', 'We donate clothes to multiple donation organisations.')
f4 = FAQ('Clothes Donation', 'What do you do with items you were unable to donate?', 'We instead sell them and donate our profit from selling the items')
f5 = FAQ('Grading of Clothes', 'What are the tiers in your grading system?', 'We have A tier, B tier, C tier and D tier')
f6 = FAQ('Grading of Clothes', 'How do you grade your clothing?', 'Our staff looks through each item and give the item a rating based on a system we have carefully created')
# f7 = FAQ(6, 'Exchanges and Returns', '?', '?')
# f8 = FAQ(6, 'Exchanges and Returns', '?', '?')




faqTable = '''
id INTEGER PRIMARY KEY,
Category TEXT,
Question TEXT,
Answer TEXT
'''

faq_insert_query = '''INSERT INTO faq (
    Category,
    Question,
    Answer)
    VALUES (?, ?, ?);
    '''

faq_update_query = '''UPDATE faq
SET Answer = ?
WHERE id = ?;
'''

question = '''UPDATE faq
SET Question = ?
WHERE i d = ?;
'''

get_custom_query = ''' SELECT * FROM faq
WHERE Category = ?
'''


db = Thriftstore()

db.create_table('faq', faqTable)

db.insert_into_table(faq_insert_query, f1)
db.insert_into_table(faq_insert_query, f2)
db.insert_into_table(faq_insert_query, f3)
db.insert_into_table(faq_insert_query, f4)
db.insert_into_table(faq_insert_query, f5)
db.insert_into_table(faq_insert_query, f6)

# db.update_table_item(faq_update_query, ('Clothes Donation 1', 3))
# db.update_table_item(faq_update_query, ('Clothes Donation 2', 4))

# db.question(faq_update_query, ('Clothes Donation 1', 3))
# db.question(faq_update_query, ('Clothes Donation 2', 4))

# db.delete_by_id_from_table('faq', 'Id', '')






id_view = int(input('Enter the Id of the question you want to view:'))

print(db.get_item_by_custom_value(get_custom_query, id_view))



db.close_connection()







