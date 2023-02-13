import hashlib
from flask import Flask, request, redirect, session, url_for, render_template, flash
from form import RegisterForm, LoginForm, UpdateUserForm
from acct_mgmt_classes import User
from models.Thriftstore import Thriftstore
from routes.customer_support.faq_table import faqTable
from routes.customer_support.cust_inquiries import solace_homepage, customer_inquiries, staff_read_inquiries, staff_reply_inquiries, staff_delete_inquiries, customer_faq, staff_add_faq, staff_delete_faq
from routes.customer_support.faq_table import faq_insert_query, f1, f2,f3,f4,f5,f6
from routes.report_generation.staff_report_views import reporthome, reportcreate, reportdelete, reportupdate
from reportdatabase import reportTableAttributes
from staff_transaction_db import Config

from routes.staff_transaction.inventory.inventory_views import view_settings, view_inventory, add_Product, edit_Product, delete_Product
from routes.staff_transaction.inventory.dashboard_views import view_bar_chart, view_pie_chart, view_invent_dashboard, get_excel_downloadable
from routes.staff_transaction.donation.donation_views import view_donations, approve_Donation, view_donation_details

app = Flask(__name__)
app.config["PORT_NUMBER"] = 5000
app.config["SECRET_KEY"] = "secretkey"
app.secret_key = app.config["SECRET_KEY"]

# Account Management
# 
# # Customer Transaction

# Customer Support
app.register_blueprint(solace_homepage)
app.register_blueprint(customer_inquiries)
app.register_blueprint(staff_read_inquiries)
app.register_blueprint(staff_reply_inquiries)
app.register_blueprint(staff_delete_inquiries)
app.register_blueprint(customer_faq)
app.register_blueprint(staff_add_faq)
app.register_blueprint(staff_delete_faq)

# Report Generation
app.register_blueprint(reporthome)
app.register_blueprint(reportcreate)
app.register_blueprint(reportdelete)
app.register_blueprint(reportupdate)

# Staff Transaction
app.register_blueprint(get_excel_downloadable)
app.register_blueprint(view_settings)
app.register_blueprint(view_invent_dashboard)
app.register_blueprint(view_bar_chart)
app.register_blueprint(view_pie_chart)
app.register_blueprint(view_inventory)
app.register_blueprint(add_Product)
app.register_blueprint(edit_Product)
app.register_blueprint(delete_Product)
app.register_blueprint(view_donations)
app.register_blueprint(approve_Donation)
app.register_blueprint(view_donation_details)


@app.route('/login', methods=["GET", "POST"])
def login():
    user_login_form = LoginForm(request.form)
    form = user_login_form

    if request.method == "POST" and user_login_form.validate():
        email = user_login_form.email.data
        password = user_login_form.password.data
        if is_valid(email, password):
            session['email'] = email
            return redirect("/profile")
        else:
            # flash("User does not exist")  
            return redirect("/login")

    return render_template("account_management/loginUser.html", form=form)

def is_valid(email, password):
    db = Thriftstore()
    db_cur = db.get_cursor()
    data = db_cur.execute('SELECT email, password FROM Users').fetchall()
    for row in data:
        if row[0] == email and row[1] == hashlib.md5(password.encode()).hexdigest():
            return True
    return False


@app.route('/register', methods=['GET', 'POST'])
def register_user():
    user_registration_form = RegisterForm(request.form)
    print(request.form)

    if request.method == 'POST':
        print(user_registration_form.name.data)

        db = Thriftstore()
        
        user_insert_query = '''INSERT INTO Users(
            name,
            email,
            phone_number,
            password,
            birthday,
            gender,
            addresses,
            card_details)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?);
        '''

        db_cur = db.get_cursor()
        data = db_cur.execute('SELECT email FROM Users').fetchall()
        for row in data:
            print(row[0])
            if user_registration_form.email.data == row[0]:
                flash('User already exists!')
                return redirect('/register')

        user = User(user_registration_form.name.data, user_registration_form.email.data, user_registration_form.phone_number.data, 
                    hashlib.md5(user_registration_form.password.data.encode()).hexdigest(), user_registration_form.birthday.data, 
                    user_registration_form.gender.data, user_registration_form.addresses.data, user_registration_form.card_details.data)

        db.insert_into_table(user_insert_query, user)
        db.close_connection()
        return redirect("/login")
    return render_template('account_management/register.html', form=user_registration_form)


# @app.route('/loginUser', methods=['GET', 'POST'])
# def login_user():
#     user_login_form = LoginForm(request.form)
    
#     if request.method == 'POST' and user_login_form.validate():
#         print(user_login_form.email.data)
#         print(user_login_form.password.data)
#         db = Thriftstore()
#         users = db.get_all_items("Users")
#         for i in range(len(users)):
#            if users[i][2] == user_login_form.email.data and users[i][4] == user_login_form.password.data:
#             print("Shit works")
#             return redirect("/profile")
#     return render_template('loginUser.html', form=user_login_form)


@app.route("/profile", methods=['GET', 'POST'])
def user_profile():
    db = Thriftstore()
    db_cur = db.get_cursor()
    print(session["email"]) 
    user_info = 0
    data = db_cur.execute("SELECT * FROM Users").fetchall()
    for row in data:
        # print(row)
        if row[2] == session["email"]:
            user_info = row
    
    # Loop through all user data in db
    # check if session email equal to any in data
    # if have then append to user data
    db.close_connection()
    return render_template("account_management/insert_acc.html", user_info=user_info)

@app.route("/profileupdate", methods=["POST", "GET"])
def updateprofile():
    user_update_form = UpdateUserForm(request.form)
    print(request.form)

    if request.method == 'POST':
        print(user_update_form.name.data)

        db = Thriftstore()
        db_cur = db.get_cursor()
        data = db_cur.execute("SELECT * FROM Users").fetchall()
        user_id = 0
        for row in data:
            if row[2] == session["email"]:
                user_id = row[0]

        update_user_query = '''UPDATE Users
        SET name = ?,
        email = ?,
        phone_number = ?,
        birthday = ?,
        gender = ?
        WHERE user_id = ?
        '''
        user_data = (user_update_form.name.data, user_update_form.email.data, user_update_form.phone_number.data,
                     user_update_form.birthday.data, user_update_form.gender.data, user_id)
        print(user_data)
        db.update_table_item(update_user_query, user_data)
        session["email"] = user_update_form.email.data
        db.close_connection()
        # flash("User details updated!")
        # print(data)
        return redirect("/profile")
    return render_template('account_management/insert_acc_update.html', form=user_update_form)

    # print(session["email"]) 
    # user_data = []
    # data = db_cur.execute("SELECT * FROM Users").fetchall()
    # for row in data:
    #     # print(row)
    #     if row[2] == session["email"]:
    #         user_data.append(row[1])
    #         user_data.append(row[2])
    #         user_data.append(row[3])
    #         user_data.append(row[5])
    #         user_data.append(row[6])

    #         print(user_data)

    db.close_connection()        
    return render_template("account_management/insert_acc_update.html")

@app.route("/paymentmethods")
def user_paymentmethods():
    db = Thriftstore()
    users = db.get_all_items("Users")
    db.close_connection()

    return render_template("account_management/payment_methods.html", users = users)

@app.route("/savedaddresses")
def user_savedaddresses():
    db = Thriftstore()
    users = db.get_all_items("Users")
    db.close_connection()

    return render_template("account_management/saved_addresses.html", users = users)  

@app.route("/orderhistory")
def user_orderhistory():
    db = Thriftstore()
    users = db.get_all_items("Users")
    db.close_connection()

    return render_template("account_management/order_history.html", users = users)     

@app.route("/mydonations")
def user_mydonations():
    db = Thriftstore()
    users = db.get_all_items("Users")
    db.close_connection()

    return render_template("account_management/my_donations.html", users = users)    

@app.route("/logout")
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))

@app.route("/userdelete", methods=["POST", "GET"])
def user_delete():
    db = Thriftstore()
    db_cur = db.get_cursor()
    print(session["email"]) 
    data = db_cur.execute("SELECT * FROM Users").fetchall()
    for row in data:
        if row[2] == session["email"]:
            user_id = row[0]
    
    db.delete_by_id_from_table('Users','user_id', user_id)
    db.close_connection()

    return redirect("/login")






if __name__ == "__main__":
    db = Thriftstore()
    # db.create_table("customerinfo", reportTableAttributes)
    # db.close_connection()
    
    usersTableAttributes = '''
     user_id INTEGER PRIMARY KEY AUTOINCREMENT, 
     name TEXT NOT NULL,
     email TEXT NOT NULL,
     phone_number TEXT NOT NULL, 
     password TEXT NOT NULL,
     birthday TEXT NOT NULL, 
     gender TEXT NOT NULL,
     addresses TEXT NOT NULL,
     card_details TEXT NOT NULL
    '''  

    db.create_table('Users', usersTableAttributes)

    # db.insert_into_table(faq_insert_query, f1)
    # db.insert_into_table(faq_insert_query, f2)
    # db.insert_into_table(faq_insert_query, f3)
    # db.insert_into_table(faq_insert_query, f4)
    # db.insert_into_table(faq_insert_query, f5)
    # db.insert_into_table(faq_insert_query, f6)

    # # db.update_table_item(faq_update_query, ('Clothes Donation 1', 3))
    # # db.update_table_item(faq_update_query, ('Clothes Donation 2', 4))

    # # db.question(faq_update_query, ('Clothes Donation 1', 3))
    # # db.question(faq_update_query, ('Clothes Donation 2', 4))

    # # db.delete_by_id_from_table('faq', 'Id', '')

    # db.close_connection()
#     db = Thriftstore() 
# #     db = Thriftstore()
# #     db.drop_table("Users")
#     db.create_table("Users", usersTableAttributes)
    app.run(debug=True)


