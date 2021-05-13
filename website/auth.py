from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method =='POST':
        email = request.form.get('email')
        password = request.form.get('password')
    
        user = User.query.filter_by(email = email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password', category='error')
        else:
            flash('User not found', category='error')
    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        email = request.form.get('email')
        password = request.form.get('password')
        confPassword = request.form.get('password1')

        user = User.query.filter_by(email = email).first()
        if user :
            flash('Email already exists', category = 'error')
        elif len(email)<4:
            flash('Email must be greater than 3 character.', category='error')
        elif len(firstName)<2:
            flash('First Name cannot be single character', category='error')
        elif password != confPassword:
            flash('Password don\'t match', category='error')
        elif len(password)<7:
            flash('Password too short', categoru='error')
        else:
             #add user to database
            new_user = User(email=email, password=generate_password_hash(password, method='sha256'), firstName=firstName, lastName=lastName,)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created', category='success')

            login_user(new_user, remember=True)

            return redirect(url_for('views.home'))


           
    return render_template('signup.html', user=current_user)
