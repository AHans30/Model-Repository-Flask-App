from flask_login import login_user
from validation_app.models import Scorecard #, User
from flask import render_template, url_for, flash, redirect
from validation_app.forms import RegistrationForm, LoginForm, ScorecardForm
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
    scorecards = Scorecard.query.all()
    return render_template("home.html", scorecards=scorecards)

@app.route("/scorecard/<int:id>")
def scorecard(id):
    scorecard = Scorecard.query.get_or_404(id)
    return render_template("scorecard.html", sc=scorecard)

@app.route("/about")
def about():
    return render_template("about.html", title = "About Us")

# @app.route("/register", methods = ['GET', 'POST'])
# def register():
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
#         user = User(ad_id = form.ad_id.data, password = hashed_password)
#         db.session.add(user)
#         db.session.commit()
#         flash(f"Account created for {form.ad_id.data}!", category='success')
#         return redirect(url_for('login'))
#     return render_template("register.html", title = "Registration", form=form)

@app.route("/login", methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('home'))
    else:
        flash('Incorrect AD ID or password. Please check ID and password.', 'danger')
    return render_template("login.html", title = "Login", form=form)

@app.route("/scorecard_submit", methods = ['GET', 'POST'])
def scorecard_submit():
    form = ScorecardForm()
    if form.validate_on_submit():

        relative_ks_change = (float(form.pdv_ks.data) - float(form.dev_ks.data)) / float(form.dev_ks.data)
        ks_absolute_rating = None
        if(form.dev_ks.data >= 0.30):
            ks_absolute_rating = 'At Par'
        elif(form.dev_ks.data >= 0.22):
            ks_absolute_rating = 'Average'
        else:
            ks_absolute_rating = 'Poor'
         
        ks_relative_rating = None
        if(relative_ks_change>= -0.15):
            ks_relative_rating = 'At Par'
        elif(relative_ks_change >= -0.30):
            ks_relative_rating = 'Average'
        else:
            ks_relative_rating = 'Poor'

        discriminatory_rating = None
        if(ks_absolute_rating == 'At Par' and ks_relative_rating == 'At Par'):
            discriminatory_rating = 'At Par'
        elif(ks_absolute_rating == 'Poor' and ks_relative_rating == 'Poor'):
            discriminatory_rating = 'Poor'
        else: 
            discriminatory_rating = 'Average'

        psi_rating = None
        if(form.psi.data <= 0.01):
            psi_rating = 'At Par'
        elif(form.psi.data <= 0.03):
            psi_rating = 'Average'
        else:
            psi_rating = 'Poor'

        scorecard = Scorecard(
            type = form.type.data,
            product = form.product.data,
            owner = form.owner.data,
            bad_definition = form.bad_definition.data,
            dev_period = form.dev_period.data,
            pdv_period = form.pdv_period.data,
            dev_ks = form.dev_ks.data,
            pdv_ks = form.pdv_ks.data,
            relative_ks_change = relative_ks_change,
            ks_absolute_rating = ks_absolute_rating,
            ks_relative_rating = ks_relative_rating,
            psi = form.psi.data,
            discriminatory_rating = discriminatory_rating,
            psi_rating = psi_rating,
            final_rating = form.final_rating.data,
            final_rating_comments = form.final_rating_comments.data,
            pdv_date = form.pdv_date.data
            )
        db.session.add(scorecard)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("scorecard_submit.html", title = "Scorecard Pre-Deployment Validation", form=form)