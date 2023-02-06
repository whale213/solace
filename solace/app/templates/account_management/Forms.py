from wtforms import Form, StringField, RadioField, TextAreaField, PasswordField, validators
from wtforms.fields import EmailField, DateField


class RegisterForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    phone_number = TextAreaField('Card Number', [validators.length(max=8)])
    password = PasswordField('Shippping Address 1', [validators.length(max=200), validators.DataRequired()])
    birthday = DateField('Birthday', format='%Y-%m-%d')
    gender = RadioField('Gender', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    address = TextAreaField('Shippping Address 1', [validators.length(max=200), validators.DataRequired()])
    card = TextAreaField('Card Number', [validators.length(max=16)])


class LoginForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(
        min=1, max=150), validators.DataRequired()]) 
    address = TextAreaField('Mailing Address', [validators.length(max=200), validators.DataRequired()])
    membership = RadioField('Membership', choices=[(
        'F', 'Fellow'), ('S', 'Senior'), ('P', 'Professional')], default='F')
    remarks = TextAreaField('Remarks', [validators.Optional()])
