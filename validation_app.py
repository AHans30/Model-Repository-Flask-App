from flask import Flask, render_template, url_for
app = Flask(__name__)


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

if __name__ == '__main__':
    app.run(debug=True)