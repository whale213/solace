from flask import Flask, redirect, url_for, render_template, request
from wtforms import *
from form_data import ContactForm
import sqlite3
from Thriftstore import Thriftstore

app = Flask(__name__)

app.config["SECRET_KEY"] = '9d034acbdfb1cf833a20b26fc2a124bc'

@app.route("/")
def home():
    return render_template("account_management/log_in.html")

class User:
    def __init__(self, user_id,name, email, phone_number, password, birthday, gender, addresses, card_details):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.password = password
        self.birthday = birthday
        self.gender = gender
        self.addresses = addresses
        self.card_details = card_details


@app.route("/register", methods=["GET", "POST"])
def register():
    db = Thriftstore()
    db.create_connection("Thriftstore")
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data  
        phone_number = form.phone_number.data
        password = form.password.data
        birthday = form.birthday.data
        gender = form.gender.data 

        u1 = User(10, name,email,phone_number,password, birthday, gender, 'tbc', 'tbc')
        user_insert_query = '''INSERT INTO Users(user_id, name, email, phone_number, password, birthday, gender) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);
        ''' 
        db.insert_into_table(user_insert_query, u1)
        
    db.close_connection()
 
    return render_template('account_management/register.html', form=form)

# class UserAccountManagement:
#     def __init__(self):
#         self.conn = sqlite3.connect('Thriftstore.db')
#         self.create_table()

#     def create_table(self):
#         c = self.conn.cursor()
#         c.execute('''CREATE TABLE IF NOT EXISTS users
#                      (name TEXT, email TEXT, phone_number TEXT, password TEXT, birthday TEXT, gender TEXT,
#                      addresses TEXT, card_details TEXT, ordered_items TEXT, donated_items TEXT, commission REAL)''')
#         self.conn.commit()

#     def add_user(self, user):
#         c = self.conn.cursor()
#         c.execute("INSERT INTO users VALUES (?,?,?,?,?,?,?,?,?,?,?)",
#                   (user.name, user.email, user.phone_number, user.password, user.birthday, user.gender,
#                    user.addresses, user.card_details, user.ordered_items, user.donated_items, user.commission))
#         self.conn.commit()

#     def update_user(self, user):
#         c = self.conn.cursor()
#         c.execute("UPDATE users SET email = ?, phone_number = ?, password = ?, birthday = ?, gender = ?, addresses = ?, card_details = ?, ordered_items = ?, donated_items = ?, commission = ? WHERE name = ?",
#                   (user.email, user.phone_number, user.password, user.birthday, user.gender, user.addresses, user.card_details, user.ordered_items, user.donated_items, user.commission, user.name))
#         self.conn.commit()

#     def delete_user(self, user_name):
#         c = self.conn.cursor()
#         c.execute("DELETE FROM users WHERE name = ?", (user_name,))
#         self.conn.commit()

#     def get_user(self, user_name):
#         c = self.conn.cursor()
#         c.execute("SELECT * FROM users WHERE name = ?", (user_name,))
#         return c.fetchone()


if __name__ == "__main__":
    app.run(debug = True)