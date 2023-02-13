from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators, PasswordField, validators, \
     EmailField, IntegerField, ValidationError, DateField, DecimalField, SelectMultipleField, FileField, MultipleFileField, BooleanField, HiddenField
from flask import flash
from wtforms.validators import Regexp
from wtforms import FileField


class LoginForm(Form):
    email = EmailField('Email', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired(), validators.Length(min=7, max=150)])
    remember_me = BooleanField('Remember me', default=False)

class RegisterForm(Form):
    name = StringField('Name', [validators.DataRequired()])
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    phone_number = IntegerField('Phone Number', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    birthday = DateField('Birthday', format='%Y-%m-%d')
    gender = SelectField('Gender', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    addresses = StringField('Address', [validators.DataRequired()])
    card_details = IntegerField('Card Details', [validators.DataRequired()])

class UpdateUserForm(Form):
    name = StringField('Name', [validators.DataRequired()])
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    phone_number = IntegerField('Phone Number', [validators.DataRequired()])
    birthday = DateField('Birthday', format='%Y-%m-%d')
    gender = SelectField('Gender', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')