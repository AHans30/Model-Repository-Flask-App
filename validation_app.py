from flask import Flask, render_template, url_for
from forms import RegistraionForm, LoginForm
app = Flask(__name__)

app.config['SECRET_KEY'] = '40702441b4d60a037091caa7349a0dac'

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

@app.route("/register")
def register():
    form = RegistraionForm()
    return render_template("register.html", title = "Registration", form=form)

@app.route("/login")
def login():
    form = LoginForm()
    return render_template("login.html", title = "Login", form=form)

if __name__ == '__main__':
    app.run(debug=True)