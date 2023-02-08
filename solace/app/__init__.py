from flask import Flask, request, redirect, url_for, render_template
from form import RegisterForm, LoginForm
from acct_mgmt_classes import User
from Thriftstore import Thriftstore

app = Flask(__name__)


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
        return redirect('/register')
    return render_template('account_management/register.html', form=user_registration_form)


@app.route('/loginUser', methods=['GET', 'POST'])
def login_user():
    user_login_form = LoginForm(request.form)
    if request.method == 'POST' and user_login_form.validate():
        pass
    return render_template('loginUser.html', form=user_login_form)





if __name__ == "__main__":
#     usersTableAttributes = '''
#     user_id INTEGER PRIMARY KEY AUTOINCREMENT, 
#     name TEXT NOT NULL,
#     email TEXT NOT NULL,
#     phone_number TEXT NOT NULL, 
#     password TEXT NOT NULL,
#     birthday TEXT NOT NULL, 
#     gender TEXT NOT NULL,
#     addresses TEXT NOT NULL,
#     card_details TEXT NOT NULL
# '''    
#     db = Thriftstore()
#     db.drop_table("Users")
#     db.create_table("Users", usersTableAttributes)
    app.run(debug=True)


