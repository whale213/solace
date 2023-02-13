from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, Blueprint
import sqlite3
from models.Thriftstore import Thriftstore
from models.report import Report
from forms.report_generation.Forms import ReportDeleteForm



reporthome = Blueprint("reporthome", __name__)
reportcreate = Blueprint("reportcreate", __name__)
reportdelete = Blueprint("reportdelete", __name__)
reportupdate = Blueprint("reportupdate", __name__)

@reporthome.route("/report-generation-home")
def home():
    db = Thriftstore()
    getcustomerinfo = db.get_all_items('customerinfo')

    return render_template("report_generation/staff_base_eg.html", getcustomerinfo=getcustomerinfo)


@reportcreate.route("/customer-reports-create", methods=['GET','POST'])
def cust_reports():
    if request.method == 'POST':
        gender = request.form['Gender']
        date = request.form['Date']
        items = request.form['Items']
        totalcost = request.form['Total_Cost']

        report = Report(gender, date, items, totalcost)
        query = 'INSERT INTO customerinfo (Gender, Date, Items, Total_Cost) VALUES (?,?,?,?)'
        db = Thriftstore()
        # insert query
        
        db.insert_into_table(query, report)
        #return "Report created successfully."
    return render_template("report_generation/report_generation_create.html")

@reportdelete.route("/customer-reports-delete", methods=['GET', 'POST'])
def cust_reports_delete():
    report_delete_form = ReportDeleteForm(request.form)
    if request.method == 'POST':
        db = Thriftstore()
        Order_ID = report_delete_form.order_id.data
        db.delete_by_id_from_table('customerinfo', 'Order_ID', Order_ID)
        db.close_connection()
        flash("Report deleted successfully")
        return redirect(url_for("reporthome.home"))
    return render_template("report_generation/report_generation_delete.html", form=report_delete_form)

@reportupdate.route("/customer-reports-update", methods=['GET', 'POST'])
def cust_reports_update():
    if request.method == 'POST':
        gender = request.form['Gender']
        date = request.form['Date']
        items = request.form['Items']
        totalcost = request.form['Total_Cost']

        db = Thriftstore()
        order_id = request.form.get("ordid")
        custom_query = f"UPDATE customerinfo SET Gender = '{gender}', Date = '{date}', Items = {items}, Total_Cost = {totalcost} WHERE Order_ID = {order_id}"
        db_cur = db.get_cursor()
        db_con = db.get_connection()
        db_cur.execute(custom_query)
        db_con.commit()
        db.close_connection()
        flash("Report updated successfully")
        return redirect(url_for("reporthome.home"))
    return render_template("report_generation/report_generation_update.html")




    
   