from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields import (
    TextAreaField, SubmitField, StringField, PasswordField,
    IntegerField, SelectField, DateField, TimeField, FloatField, RadioField
)
from wtforms.validators import (
    InputRequired, Length, Email, EqualTo, NumberRange, Regexp, Optional
)



class LoginForm(FlaskForm):
    email = StringField("Email Address", validators=[
        InputRequired('Enter email address'),
        Email('Please enter a valid email')
    ])
    password = PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")


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
    password = PasswordField("Password", validators=[
        InputRequired(),
        EqualTo('confirm', message="Passwords should match")
    ])
    confirm = PasswordField("Confirm Password")
    submit = SubmitField("Register")


class TicketForm(FlaskForm):
    quantity = IntegerField('Number of Tickets', validators=[
        InputRequired('Please enter a quantity'),
        NumberRange(min=1, max=99, message='You can only book between 1 and 99 tickets')
    ])
    submit = SubmitField('Buy Tickets')


class CommentForm(FlaskForm):
    text = TextAreaField('Comment', validators=[
        InputRequired('Please enter a comment'),
        Length(min=1, max=1000, message='Comment must be under 1000 characters')
    ])
    submit_comment = SubmitField('Post Comment')


CATEGORY_CHOICES = [
    ('', 'Select a genre...'),
    ('Indie Rock', 'Indie Rock'),
    ('Folk', 'Folk'),
    ('Dream Pop', 'Dream Pop'),
    ('Lo-Fi', 'Lo-Fi'),
    ('Alt Country', 'Alt Country'),
    ('Shoegaze', 'Shoegaze'),
    ('Post-Punk', 'Post-Punk'),
    ('Other', 'Other'),
]

ACK_CHOICES = [
    ('none', 'No Acknowledgement'),
    ('generic', 'Generic Acknowledgement'),
    ('enhanced', 'Enhanced Acknowledgement'),
]

SEQ_REGION_CHOICES = [
    ('', 'Select a region...'),
    ('Brisbane CBD', 'Brisbane CBD — Turrbal and Jagera peoples'),
    ('Gold Coast', 'Gold Coast — Yugambeh peoples'),
    ('Sunshine Coast', 'Sunshine Coast — Kabi Kabi peoples'),
    ('Toowoomba', 'Toowoomba — Giabal and Jarowair peoples'),
    ('Ipswich', 'Ipswich — Yugarapul peoples'),
    ('Logan/Redlands', 'Logan/Redlands — Quandamooka peoples'),
]

IS_INDIGENOUS_CHOICES = [
    ('yes', 'Yes, I identify as Aboriginal or Torres Strait Islander'),
    ('no', 'No'),
]




class EventForm(FlaskForm):
    title = StringField('Event Title', validators=[
        InputRequired('Enter event title'),
        Length(max=200, message='Title must be under 200 characters')
    ])
    category = SelectField('Genre / Category', choices=CATEGORY_CHOICES,
        validators=[InputRequired('Select a category')])
    description = TextAreaField('Description', validators=[
        InputRequired('Enter a description')
    ])
    image = FileField('Event Image', validators=[
        Optional(),
        FileAllowed(['jpg', 'jpeg', 'png', 'webp', 'avif'],
                    'Only JPG, PNG, WEBP, or AVIF images are allowed')
    ])
    headliner = StringField('Headliner / Main Act', validators=[
        InputRequired('Enter headliner name'),
        Length(max=200)
    ])
    support_acts = StringField('Support Acts', validators=[
        Optional(), Length(max=300)
    ])
    venue = StringField('Venue Name', validators=[
        InputRequired('Enter venue name'), Length(max=200)
    ])
    address = StringField('Venue Address', validators=[
        InputRequired('Enter venue address'), Length(max=300)
    ])
    event_date = DateField('Date', validators=[InputRequired('Enter event date')])
    start_time = TimeField('Start Time', validators=[InputRequired('Enter start time')])
    end_time = TimeField('End Time', validators=[Optional()])
    capacity = IntegerField('Total Capacity', validators=[
        InputRequired('Enter capacity'),
        NumberRange(min=1, message='Capacity must be at least 1')
    ])
    price = FloatField('Ticket Price (AUD)', validators=[
        InputRequired('Enter ticket price'),
        NumberRange(min=0, message='Price cannot be negative')
    ])
    acknowledgement_type = RadioField('Acknowledgement of Country',
        choices=ACK_CHOICES, default='none',
        validators=[InputRequired('Select an acknowledgement option')])
    acknowledgement_region = SelectField(
        'Region',
        choices=SEQ_REGION_CHOICES,
        validators=[Optional()]
    )
    is_indigenous = RadioField(
        'Do you identify as Aboriginal or Torres Strait Islander?',
        choices=IS_INDIGENOUS_CHOICES,
        validators=[Optional()]
    )
    submit = SubmitField('Publish Event')
