import sqlite3

class User:
    def __init__(self, name, email, phone_number, password, birthday, gender, addresses, card_details, ordered_items, donated_items, commission):
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.password = password
        self.birthday = birthday
        self.gender = gender
        self.addresses = addresses
        self.card_details = card_details
        self.ordered_items = ordered_items
        self.donated_items = donated_items
        self.commission = commission

class UserAccountManagement:
    def __init__(self):
        self.conn = sqlite3.connect('users.db')
        self.create_table()

    def create_table(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users
                     (name TEXT, email TEXT, phone_number TEXT, password TEXT, birthday TEXT, gender TEXT,
                     addresses TEXT, card_details TEXT, ordered_items TEXT, donated_items TEXT, commission REAL)''')
        self.conn.commit()

    def add_user(self, user):
        c = self.conn.cursor()
        c.execute("INSERT INTO users VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                  (user.name, user.email, user.phone_number, user.password, user.birthday, user.gender,
                   user.addresses, user.card_details, user.ordered_items, user.donated_items, user.commission))
        self.conn.commit()

    def update_user(self, user):
        c = self.conn.cursor()
        c.execute("UPDATE users SET email = ?, phone_number = ?, password = ?, birthday = ?, gender = ?, addresses = ?, card_details = ?, ordered_items = ?, donated_items = ?, commission = ? WHERE name = ?",
                  (user.email, user.phone_number, user.password, user.birthday, user.gender, user.addresses, user.card_details, user.ordered_items, user.donated_items, user.commission, user.name))
        self.conn.commit()

    def delete_user(self, user_name):
        c = self.conn.cursor()
        c.execute("DELETE FROM users WHERE name = ?", (user_name,))
        self.conn.commit()

    def get_user(self, user_name):
        c = self.conn.cursor()
        c.execute("SELECT * FROM users WHERE name = ?", (user_name,))
        return c.fetchone()
