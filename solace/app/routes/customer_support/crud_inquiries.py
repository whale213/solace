from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators

class createinquiry():
    name = StringField('Name', [validators.Length(min = 1, max = 150), validators.Datarequired('Please enter your name')])
    email = StringField('Email', [validators.Length(min = 1, max = 150), validators.Email('PLease enter a valid email')])
    inquiry = TextAreaField('Inquiry', [validators.Lenght(min = 1), validators.DataRequired('Please enter your inquiry')])

