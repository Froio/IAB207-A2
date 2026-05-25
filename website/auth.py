from urllib.parse import urlparse
from flask import Blueprint, flash, render_template, request, url_for, redirect
from flask_login import login_user, login_required, logout_user
from .models import User
from .forms import LoginForm, RegisterForm
from . import db, bcrypt

# Create a blueprint - make sure all BPs have unique names
auth_bp = Blueprint('auth', __name__)

# this is a hint for a login function
@auth_bp.route('/login', methods=['GET', 'POST'])
# view function
def login():
    login_form = LoginForm()
    error = None
    if login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data
        user = db.session.scalar(db.select(User).where(User.email==email))
        if user is None:
            error = 'Incorrect email'
        elif not bcrypt.check_password_hash(user.password_hash, password): # takes the hash and cleartext password
            error = 'Incorrect password'
        if error is None:
            login_user(user)
            nextp = request.args.get('next') # this gives the url from where the login page was accessed
            if not nextp:
                return redirect(url_for('main.index'))
            parsed_nextp = urlparse(nextp)
            if parsed_nextp.scheme or parsed_nextp.netloc or not nextp.startswith('/'):
                return redirect(url_for('main.index'))
            return redirect(nextp)
        else:
            flash(error)
    return render_template('user.html', form=login_form, heading='Login')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        firstname = register_form.firstname.data
        surname = register_form.surname.data
        email = register_form.email.data
        contact_number = register_form.contact_number.data
        street_address = register_form.street_address.data
        password = register_form.password.data

        # check for existing email
        existing_email = db.session.scalar(db.select(User).where(User.email==email))
        if existing_email is not None:
            flash('Email already registered')
            return render_template('user.html', form=register_form, heading='Register')

        # hash password and store user
        pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(
            firstname=firstname,
            surname=surname,
            email=email,
            contact_number=contact_number,
            street_address=street_address,
            password_hash=pw_hash
        )
        db.session.add(user)
        db.session.commit()
        flash('Registration successful — please log in')
        return redirect(url_for('auth.login'))

    return render_template('user.html', form=register_form, heading='Register')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))