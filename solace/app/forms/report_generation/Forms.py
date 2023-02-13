from wtforms import Form, IntegerField, validators

class ReportDeleteForm(Form):
    order_id = IntegerField('Order ID', [validators.DataRequired()])