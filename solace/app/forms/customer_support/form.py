from wtforms import Form
from wtforms import TextAreaField

class InquiryForm(Form):
    reply = TextAreaField("")

