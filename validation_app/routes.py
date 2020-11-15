from flask_login import login_user
from validation_app.models import User, Scorecard
from flask import render_template, url_for, flash, redirect
from validation_app.forms import RegistrationForm, LoginForm
from validation_app import app, db, bcrypt

scorecards = [
    {
        'product': 'PL',
        'owner': 'Ankur Nahar',
        'type': 'Application Scorecard',
        'deployment_date': 'May 30, 2020',
        'discrimatory_power': 'At Par',
        'psi': 'Average',
        'final_rating': 'Acceptable'
    },
    {
        'product': 'TWL',
        'owner': 'Nikhil Chhedha',
        'deployment_date': 'Sept 18, 2020',
        'type': 'Fraud Scorecard',
        'discrimatory_power': 'Average',
        'psi': 'Average',
        'final_rating': 'Rebuild'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", scorecards=scorecards)

@app.route("/about")
def about():
    return render_template("about.html", title = "About Us")

@app.route("/register", methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(ad_id = form.ad_id.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for {form.ad_id.data}!", category='success')
        return redirect(url_for('login'))
    return render_template("register.html", title = "Registration", form=form)

@app.route("/login", methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(ad_id = form.ad_id.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Incorrect AD ID or password. Please check ID and password.', 'danger')
    return render_template("login.html", title = "Login", form=form)