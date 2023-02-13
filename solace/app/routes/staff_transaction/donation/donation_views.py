from flask import render_template, request, redirect, Blueprint
from models.Thriftstore import Thriftstore
from forms.staff_transaction.staff_transaction_forms import ApprovalForm
from wtforms import ValidationError
from datetime import date

view_donations = Blueprint("donations", __name__)
approve_Donation = Blueprint("approveDonation", __name__)
view_donation_details = Blueprint("donationDetails", __name__)

# Function to populate the drop down choices with db inputs
def populateDropDownLists(db_drop_down_data, htmlList):

    for drp_down_data in range(len(db_drop_down_data)):
        drp_down_data_tuple = []
        drp_down_data_item = db_drop_down_data[drp_down_data][0]
        for value_and_label in range(2):
            # Assign the value and label to the same value in the db tuple's first data item
            drp_down_data_tuple.append(drp_down_data_item)
        # Add the tuple with value and label into html list to populate into form
        htmlList.append(tuple(drp_down_data_tuple))

get_req_stat_reasons_query = '''SELECT req_stat_reason FROM Static_Inputs WHERE req_stat_reason IS NOT NULL'''

@view_donations.route("/viewDonations")
def donations():
    db = Thriftstore()
    donations = db.get_all_items("Donations")
    today = date.today()
    date_formatted = today.strftime("%B %d, %Y")
    db.close_connection()
    return render_template("staff_transaction/viewDonations.html",
                        donations = donations, today=date_formatted)

@approve_Donation.route("/approveDonation/<int:id>", methods=["GET", "POST"])
def approveDonations(id):
    db = Thriftstore()
    donation_details = db.foreign_key_query(
        t_name_one="Donation_Details",
        t_name_two="Donations",
        fk_name="donation_id",
        pk_name="donation_id",
        select_values=[
            "Donation_Details.donation_item_name",
            "Donation_Details.condition",
            "Donation_Details.quantity",
            "Donation_Details.brand",
            "Donation_Details.size",
            "Donation_Details.donation_image_filename"
        ],
        type_of_join="INNER JOIN",
        specifc_query=f"WHERE Donations.donation_id = {id}"
    )

    cur = db.get_cursor()
    db_req_stat_reasons = cur.execute(get_req_stat_reasons_query).fetchall()
    reject_or_na_reasons = [("None", "Select Reason")]

    populateDropDownLists(db_req_stat_reasons, reject_or_na_reasons)

    donations = db.get_item_by_id("Donations", "donation_id", id)[0]
    donation_id = donations[0]
    donation_of_user_id = donations[1]
    collection_opt = donations[6]
    donation_time = donations[7]
    donation_date = donations[8]
    approvalDonationForm = ApprovalForm(request.form)

    approvalDonationForm.req_stat_reason.choices = reject_or_na_reasons
    if request.method == "POST" and approvalDonationForm.validate():
        all_p_approved = approvalDonationForm.all_products_approved.data
        remarks = approvalDonationForm.remarks.data
        drp_off_donate_req_stat = approvalDonationForm.drp_off_or_donate_req_stat.data
        req_stat_reason = approvalDonationForm.req_stat_reason.data
        delivery_payment = approvalDonationForm.delivery_payment.data
        total_commission = str(approvalDonationForm.total_commission.data)

        update_donation_approval_query = """UPDATE Donations 
        SET donation_approval= ?, 
        donation_remarks = ?, 
        drp_off_or_donate_req_stat = ?,
        req_stat_reason = ?,
        total_delivery_amt = ?,
        total_possible_comm = ?
        WHERE donation_id = ?
        """

        approval_tuple = (all_p_approved, remarks, drp_off_donate_req_stat, req_stat_reason, 
                        delivery_payment, total_commission, id)  

        db.update_table_item(update_donation_approval_query, approval_tuple)
        db.close_connection()
        return redirect("/viewDonations")     
    else:
        approvalDonationForm.remarks.data = donations[5]
        approvalDonationForm.req_stat_reason.data = donations[10]
        db.close_connection()
        return render_template("staff_transaction/approveDonations.html",
                            donations = donation_details, user_id = donation_of_user_id, 
                            collection_opt = collection_opt, donation_id = donation_id,
                            donation_time = donation_time, donation_date= donation_date, form=approvalDonationForm)


@view_donation_details.route("/viewDonationDetails/<int:id>", methods=["GET", "POST"])
def donationDetails(id):
    db = Thriftstore()
    donation_details = db.foreign_key_query(
        t_name_one="Donation_Details",
        t_name_two="Donations",
        fk_name="donation_id",
        pk_name="donation_id",
        select_values=[
            "Donation_Details.donation_item_name",
            "Donation_Details.condition",
            "Donation_Details.quantity",
            "Donation_Details.brand",
            "Donation_Details.size",
            "Donation_Details.donation_image_filename"
        ],
        type_of_join="INNER JOIN",
        specifc_query=f"WHERE Donations.donation_id = {id}"
    )

    donations = db.get_item_by_id("Donations", "donation_id", id)[0]
    donation_id = donations[0]
    donation_of_user_id = donations[1]
    donation_outcome = donations[4]
    donation_remarks = donations[5]
    collection_opt = donations[6]
    donation_time = donations[7]
    donation_date = donations[8]
    drp_off_or_donate_acceptance = donations[9]
    possible_commission = donations[12]
    db.close_connection()
    return render_template("staff_transaction/viewDonationDetails.html",
                            donations = donation_details, user_id = donation_of_user_id, 
                            collection_opt = collection_opt, donation_id = donation_id,
                            donation_time = donation_time, donation_date= donation_date,
                            donation_req_stat=drp_off_or_donate_acceptance, outcome=donation_outcome,
                            possible_commission=possible_commission, remarks=donation_remarks)