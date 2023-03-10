from models.Thriftstore import Thriftstore
import sqlite3
from models.Chatbot import Chatbot
        
q1 = Chatbot(1, 'The grading system of our clothes', 'We grade our clothes ...')
q2 = Chatbot(2, 'The pricing system', 'We price our clothes...')
q3 = Chatbot(3, 'Sales available', 'The sales which are available are...')
q4 = Chatbot(4, 'Directions to our store', 'The directions are...')

chatbotTable = '''
QuestionId INT PRIMARY KEY,
Question CHAR(200) NOT NULL,
Answer CHAR(200) NOT NULL
'''

chatbot_insert_query = '''INSERT OR IGNORE INTO ChatBot(
    QuestionId,
    Question,
    Answer)
    VALUES (?, ?, ?);
    '''

chatbot_update_query = '''UPDATE ChatBot
SET Answer = ?
WHERE QuestionId = ?;
'''

get_custom_query = ''' SELECT * FROM ChatBot 
WHERE QuestionId = ?
'''


db = Thriftstore()

db.create_connection('ChatBot')

db.create_table('ChatBot', chatbotTable)

db.insert_into_table(chatbot_insert_query, q1)
db.insert_into_table(chatbot_insert_query, q2)
db.insert_into_table(chatbot_insert_query, q3)
db.insert_into_table(chatbot_insert_query, q4)

db.close_connection()







