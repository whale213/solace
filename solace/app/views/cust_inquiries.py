from flask import Flask, render_template, request, redirect, url_for, Blueprint
from models.Thriftstore import Thriftstore
import sqlite3
import smtplib
from form import InquiryForm

solace_homepage = Blueprint('solace_homepage', __name__)


customer_inquiries = Blueprint('customer_inquiries', __name__)
staff_read_inquiries = Blueprint('staff_read_inquiries', __name__)
staff_reply_inquiries = Blueprint('staff_reply_inquiries', __name__)
staff_delete_inquiries = Blueprint('staff_delete_inquiries', __name__)
staff_reply_inquiries = Blueprint('staff_reply_inquiries', __name__)

customer_faq = Blueprint('customer_faq', __name__)
staff_add_faq = Blueprint('staff_add_faq', __name__)
staff_delete_faq = Blueprint('staff_delete_faq', __name__)




db = Thriftstore()


inquiryTable = 'id INTEGER PRIMARY KEY, name TEXT, email TEXT, inquiry TEXT'



db.create_table('inquiry', inquiryTable)
db.close_connection()


class Inquiry:
    def __init__(self, name, email, inquiry):
        self.name = name
        self.email = email
        self.inquiry = inquiry

@solace_homepage.route("/")
def index():
    return render_template("customer_support/Homepage.html")

@customer_inquiries.route("/submit", methods=["POST", "GET"])
def createinquiry():
    if request.method == 'POST':
        name = request.form["nm"]
        email = request.form["em"]
        inquiry = request.form["inq"]
    else:
        return render_template('customer_support/cust_inquiries_page.html')

    inquiry_obj = Inquiry(name, email, inquiry)
    db = Thriftstore()
    inquiry_insert_query = '''INSERT INTO inquiry (
        name, 
        email, 
        inquiry) 
        VALUES (?, ?, ?);
        '''
    db.insert_into_table(inquiry_insert_query, inquiry_obj)
    db.close_connection()

    return redirect ('/submit')



@staff_read_inquiries.route("/inquiries")
def readinquiries():
    db = Thriftstore()
    inquiries = db.get_all_items('inquiry')
    faq = db.get_ordered_by_custom_value('faq', 'Category', 'DESC')
    db.close_connection()   

    return render_template("customer_support/staff_inquiries_read_page.html", inquiries = inquiries, faq = faq)

@staff_reply_inquiries.route("/update", methods=["POST","GET"])
def replyinquiries():
    id = request.args.get('id')
    db = Thriftstore()
    inquiries = db.get_item_by_id('inquiry', 'id', id)
    db.close_connection()
    form = InquiryForm(request.form)

    if request.method == 'POST':
        reply = form.reply.data
        sender_email = 'susraaan@gmail.com'
        receiver_email = inquiries[0][2]
        message = 'Subject: Reply from Solace Singapore: \n\n' + reply

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)       
            server.starttls()
            server.login(sender_email, "hkuz iras qmvj qokq")
            server.sendmail(sender_email, receiver_email, message)
            server.close()
            return redirect('/inquiries')
        except Exception as e:
            return f"An error occurred: {e}"
    else:
        print(inquiries)
        return render_template('customer_support/staff_inquiries_reply_page.html', inquiries=inquiries, form=form)


    
    

@staff_delete_inquiries.route("/delete", methods=["POST"])
def delete():
    id = request.form.get("id")
    db = Thriftstore()
    db.delete_by_id_from_table('inquiry', 'id', id)
    db.close_connection()

    return redirect('/inquiries')


@customer_faq.route('/FAQ', methods=["POST", "GET"])
def faq():
    db = Thriftstore()

    category_query = 'SELECT * FROM faq WHERE Category = ?'
    ship = db.get_item_by_custom_value(category_query, 'Shipping & Handling')
    donations = db.get_item_by_custom_value(category_query, 'Clothes Donation')
    grading = db.get_item_by_custom_value(category_query, 'Grading of Clothes')
    print(donations)

    db.close_connection()   

    return render_template('customer_support/cust_faq_page.html', ship = ship, donations = donations, grading = grading)

@staff_add_faq.route('/FAQa', methods=["POST", "GET"])
def faq_add():
    if request.method == 'POST':
        name = request.form['cat']
        qn = request.form['qn']
        ans = request.form['ans']

    else:
        return render_template('customer_support/staff_faq_add_page.html')


    inquiry_obj = Inquiry(name, qn, ans)
    inquiry_insert_query = '''INSERT INTO faq (
        Category, 
        Question, 
        Answer) 
        VALUES (?, ?, ?);
        '''
    db = Thriftstore()
    db.insert_into_table(inquiry_insert_query, inquiry_obj)

    db.close_connection()

    return redirect('/inquiries')



@staff_delete_faq.route("/FAQ_delete", methods=["POST"])
def faq_delete():

    id = request.form.get("id")
    db = Thriftstore()
    db.delete_by_id_from_table('faq', 'Id', id)
    db.close_connection()

    return redirect('/inquiries')


# @.route('/chatbot', methods = ["POST", "GET"])
# def chatbot():
#     return render_template('customer_support/cust_chatbot_page.html')


