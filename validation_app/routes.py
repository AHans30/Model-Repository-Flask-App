from flask_login import login_user
from validation_app.models import Scorecard, Monitoring
from flask import render_template, url_for, flash, redirect, request, send_file, make_response
from validation_app.forms import RegistrationForm, LoginForm, ScorecardForm, MonitoringForm
from validation_app import app, db, bcrypt
from io import BytesIO
from werkzeug.utils import secure_filename
import pandas as pd


@app.route("/")
@app.route("/home")
def home():
    scorecards = Scorecard.query.all()
    return render_template("home.html", scorecards=scorecards)

@app.route("/scorecard/<int:id>")
def scorecard(id):
    scorecard = Scorecard.query.get_or_404(id)
    monitorings = Monitoring.query.filter_by(scorecard_id=id).all()
    if(len(monitorings)==0):
        monitorings = False
    return render_template("scorecard.html", sc=scorecard, monitorings=monitorings)

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
        
        attached_report = request.files['attached_report']
        filename = secure_filename(attached_report.filename)

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
            pdv_date = form.pdv_date.data,
            report_owner = form.report_owner.data,
            attached_report = attached_report.read(),
            attachment_name = filename
            )
        db.session.add(scorecard)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("scorecard_submit.html", title = "Scorecard Pre-Deployment Validation", form=form)

@app.route("/download_pdv/<int:id>")
def download_pdv(id):
    pdv_report = Scorecard.query.get_or_404(id).attached_report
    filename = Scorecard.query.get_or_404(id).attachment_name
    return send_file(BytesIO(pdv_report), as_attachment = True, attachment_filename=filename)

@app.route("/monitoring_submit/<int:scorecard_id>", methods = ['GET', 'POST'])
def monitoring_submit(scorecard_id):
    form = MonitoringForm()
    scorecard = Scorecard.query.get_or_404(scorecard_id)
    if form.validate_on_submit():

        relative_ks_change = (float(form.monitoring_ks.data) - float(scorecard.dev_ks)) / float(scorecard.dev_ks)
         
        ks_relative_rating = None
        if(relative_ks_change>= -0.15):
            ks_relative_rating = 'At Par'
        elif(relative_ks_change >= -0.30):
            ks_relative_rating = 'Average'
        else:
            ks_relative_rating = 'Poor'

        discriminatory_rating = None
        if(scorecard.ks_absolute_rating == 'At Par' and scorecard.ks_relative_rating == 'At Par'):
            discriminatory_rating = 'At Par'
        elif(scorecard.ks_absolute_rating == 'Poor' and scorecard.ks_relative_rating == 'Poor'):
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
        
        attached_report = request.files['attached_report']
        filename = secure_filename(attached_report.filename)

        monitoring = Monitoring(
            scorecard = scorecard,
            monitoring_period = form.monitoring_period.data,
            current_period = form.current_period.data,
            proxy_bad_definition = form.proxy_bad_definition.data,
            monitoring_ks = form.monitoring_ks.data,
            psi = form.psi.data,
            relative_ks_change = relative_ks_change,
            ks_relative_rating = ks_relative_rating,
            discriminatory_rating = discriminatory_rating,
            psi_rating = psi_rating,
            final_rating = form.final_rating.data,
            final_rating_comments = form.final_rating_comments.data,
            monitoring_date = form.monitoring_date.data,
            report_owner = form.report_owner.data,
            attached_report = attached_report.read(),
            attachment_name = filename
            )
        
        db.session.add(monitoring)
        db.session.commit()

        return redirect(url_for('scorecard', id = scorecard.id))

    title = f"Submit Monitoring: {scorecard.id}: {scorecard.type} {scorecard.product}"
    return render_template("monitoring_submit.html", title = title, form=form, sc=scorecard)

@app.route("/download_monitoring/<int:id>")
def download_monitoring(id):
    monitoing_report = Monitoring.query.get_or_404(id).attached_report
    filename = Monitoring.query.get_or_404(id).attachment_name
    return send_file(BytesIO(monitoing_report), as_attachment = True, attachment_filename=filename)

@app.route("/download_repository")
def download_repository():
    repo_df = pd.read_sql_table('scorecard', con=db.engine)
    response = make_response(repo_df.to_csv())
    response.headers["Content-Disposition"] = "attachment; filename=Model_Repository.csv"
    response.headers["Content-Type"] = "text/csv"
    return response