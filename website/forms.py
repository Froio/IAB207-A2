from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, IntegerField
from wtforms.validators import InputRequired, Length, Email, EqualTo, NumberRange, Regexp

# creates the login information
class LoginForm(FlaskForm):
    email = StringField("Email Address", validators=[
        InputRequired('Enter email address'),
        Email('Please enter a valid email')
    ])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

# this is the registration form
class RegisterForm(FlaskForm):
    firstname = StringField("First Name", validators=[InputRequired('Enter first name')])
    surname = StringField("Surname", validators=[InputRequired('Enter surname')])
    email = StringField("Email Address", validators=[
        InputRequired('Enter email address'),
        Email("Please enter a valid email")
    ])
    contact_number = StringField("Contact Number", validators=[
        InputRequired('Enter contact number'),
        Regexp(r'^[0-9\s\-\+\(\)]{8,}$', message='Please enter a valid phone number')
    ])
    street_address = StringField("Street Address", validators=[
        InputRequired('Enter street address'),
        Length(max=255, message='Street address is too long')
    ])
    # linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")

    # submit button
    submit = SubmitField("Register")

class TicketForm(FlaskForm):
    quantity = IntegerField('Number of Tickets', validators=[
        InputRequired('Please enter a quantity'),
        NumberRange(min=1, max=99, message='You can only book between 1 and 99 tickets')
    ])
    submit = SubmitField('Buy Tickets')