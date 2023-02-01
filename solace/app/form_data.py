from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, RadioField
from wtforms.validators import DataRequired, Email


class ContactForm(FlaskForm):
  name = StringField('name', validators=[DataRequired()])
  email = StringField('email', validators=[DataRequired(), Email()])
  phone_number = StringField('phone_number', validators=[DataRequired()])
  password = StringField('password', validators=[DataRequired()])
  birthday = StringField('birthday', validators=[DataRequired()])
  gender = RadioField(label='gender', choices=[('female', 'female'), ('male', 'male')], validators=[DataRequired()])
  send = SubmitField('send')