from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password :-(!', category='error')
        else:
            flash(f'User {user} doesnt exist!', category='error')

    return render_template("login.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        pw1 = request.form.get('pw1')
        pw2 = request.form.get('pw2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash(f'User {user} already exists!', category='error')
        elif len(email) < 4:
            flash('Please enter a valid E-Mail address!', category='error')
        elif len(firstName) < 2:
            flash('First Name must be greater than 2 characters!', category='error')
        elif pw1 != pw2:
            flash('Password don´t match!', category='error')
        elif len(pw1) < 7:
            flash('Password must be at least 7 Characters!', category='error')
        else:
            new_user = User(email=email, first_name=firstName, password=generate_password_hash(pw1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            
            flash('Account created!', category='success')
            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
