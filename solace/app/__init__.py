from flask import Flask, request, redirect, url_for, render_template
from form import RegisterForm, LoginForm
from acct_mgmt_classes import User
from models.Thriftstore import Thriftstore
from routes.customer_support.faq_table import faqTable
from routes.customer_support.cust_inquiries import solace_homepage, customer_inquiries, staff_read_inquiries, staff_reply_inquiries, staff_delete_inquiries, customer_faq, staff_add_faq, staff_delete_faq
from routes.customer_support.faq_table import faq_insert_query, f1, f2,f3,f4,f5,f6
from routes.report_generation.staff_report_views import reporthome, reportcreate, reportdelete, reportupdate
from reportdatabase import reportTableAttributes

app = Flask(__name__)
app.config["PORT_NUMBER"] = 5000
app.config["SECRET_KEY"] = "secretkey"
app.secret_key = app.config["SECRET_KEY"]

# Customer Support
app.register_blueprint(solace_homepage)
app.register_blueprint(customer_inquiries)
app.register_blueprint(staff_read_inquiries)
app.register_blueprint(staff_reply_inquiries)
app.register_blueprint(staff_delete_inquiries)
app.register_blueprint(customer_faq)
app.register_blueprint(staff_add_faq)
app.register_blueprint(staff_delete_faq)

# Blueprint views / routes for app
app.register_blueprint(reporthome)
app.register_blueprint(reportcreate)
app.register_blueprint(reportdelete)
app.register_blueprint(reportupdate)


@app.route('/')
def home():
    user_login_form = LoginForm(request.form)
    form = user_login_form

    if request.method == "POST" and user_login_form.validate():

        user = User(user_login_form.email.data,
                    user_login_form.password.data)

        pass
    return render_template("account_management/loginUser.html", form=(user_login_form))

    
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

        user = User(user_registration_form.name.data, user_registration_form.email.data,
                    user_registration_form.phone_number.data, user_registration_form.password.data, user_registration_form.birthday.data,
                    user_registration_form.gender.data, user_registration_form.addresses.data, user_registration_form.card_details.data)

        db.insert_into_table(user_insert_query, user)
        db.close_connection()
        return redirect(url_for(home))
    return render_template('account_management/register.html', form=user_registration_form)


@app.route('/loginUser', methods=['GET', 'POST'])
def login_user():
    user_login_form = LoginForm(request.form)
    
    if request.method == 'POST' and user_login_form.validate():
        print(user_login_form.email.data)
        print(user_login_form.password.data)
        db = Thriftstore()
        users = db.get_all_items("Users")
        for i in range(len(users)):
           if users[i][2] == user_login_form.email.data and users[i][4] == user_login_form.password.data:
            print("Shit works")
            return redirect("/profile")
    return render_template('loginUser.html', form=user_login_form)
        


@app.route("/profile", methods=['GET', 'POST'])
def user_profile():
    db = Thriftstore()
    users = db.get_all_items("Users")
    db.close_connection()
    return render_template("account_management/insert_acc.html", users = users)

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



if __name__ == "__main__":
    # db = Thriftstore()
    # db.create_table("customerinfo", reportTableAttributes)
    # db.close_connection()
    
    # db.create_table('faq', faqTable)

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
#     usersTableAttributes = '''
#      user_id INTEGER PRIMARY KEY AUTOINCREMENT, 
#      name TEXT NOT NULL,
#      email TEXT NOT NULL,
#      phone_number TEXT NOT NULL, 
#      password TEXT NOT NULL,
#      birthday TEXT NOT NULL, 
#      gender TEXT NOT NULL,
#      addresses TEXT NOT NULL,
#      card_details TEXT NOT NULL
#  '''    
# #     db = Thriftstore()
# #     db.drop_table("Users")
#     db.create_table("Users", usersTableAttributes)
    app.run(debug=True)


