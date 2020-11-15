from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from sqlalchemy.orm import backref
#from flask.helpers import flash
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '40702441b4d60a037091caa7349a0dac'

POSTGRES = {
    'user': 'postgres',
    'pw': 'password',
    'db': 'model_repository',
    'host': 'localhost',
    'port': '5432',
}
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://" + POSTGRES['user'] + ":" + \
    POSTGRES['pw'] + "@" + POSTGRES['host'] + ":" + POSTGRES['port'] + "/" + POSTGRES['db']
db = SQLAlchemy(app)

class User(db.Model):
    ad_id = db.Column(db.Integer, primary_key = True)
    password = db.Column(db.String(60), nullable = False)
    scorecards = db.relationship('Scorecard', backref = 'validator', lazy = True)

    def __repr__(self):
        return f"User({self.ad_id})"

class Scorecard(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    product = db.Column(db.String(60), nullable = False)
    type = db.Column(db.String(60), nullable = False)
    deployment_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    discrimatory_power = db.Column(db.String(12), nullable = False)
    psi = db.Column(db.String(12), nullable = False)
    final_rating = db.Column(db.String(12), nullable = False)
    validator_id = db.Column(db.Integer, db.ForeignKey('user.ad_id'), nullable = False)
    
    def __repr__(self):
        return f"Scorecard({self.id}, {self.product}, {self.type})"

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
        flash(f"Account created for {form.ad_id.data}!", category='success')
        return redirect(url_for('home'))
    return render_template("register.html", title = "Registration", form=form)

@app.route("/login")
def login():
    form = LoginForm()
    return render_template("login.html", title = "Login", form=form)

if __name__ == '__main__':
    app.run(debug=True)