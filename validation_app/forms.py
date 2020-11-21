from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FloatField, FileField, TextAreaField, SelectField, DateField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from wtforms.widgets import TextArea
#from validation_app.models import User



class RegistrationForm(FlaskForm):
    ad_id = StringField('AD ID', validators=[DataRequired(), Length(min = 2, max = 20)])
    password = PasswordField('Password',  validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')

    # def validate_ad_id(self, ad_id):
    #     user = User.query.filter_by(ad_id = ad_id.data).first()
    #     if user:
    #         raise ValidationError('Given AD ID is already registered!')

class LoginForm(FlaskForm):
    ad_id = StringField('AD ID', validators=[DataRequired(), Length(min = 2, max = 20)])
    password = PasswordField('Password',  validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class ScorecardForm(FlaskForm):
    type = SelectField('Type', choices = ['Application', 'Behavior', 'Debit'],validators=[DataRequired(), Length(min = 2, max = 20)])
    product = StringField('Product', validators=[DataRequired(), Length(min = 2, max = 20)])
    owner = StringField('Model Owner', validators=[DataRequired(), Length(min = 2, max = 20)])
    bad_definition = StringField('Bad Definition', validators=[DataRequired(), Length(min = 2, max = 100)])
    dev_period = StringField('Development Period', validators=[DataRequired(), Length(min = 2, max = 20)])
    pdv_period = StringField('PDV Period', validators=[DataRequired(), Length(min = 2, max = 20)])
    dev_ks = FloatField('Development KS', validators=[DataRequired()])
    pdv_ks = FloatField('PDV KS', validators=[DataRequired()])
    #relative_ks_change = FloatField('Relative KS Change', validators=[DataRequired(), Length(min = 2, max = 20)])
    psi = FloatField('PSI', validators=[DataRequired()])
    #ks_absolute_rating = StringField('Absolute Discrimination Rating', validators=[DataRequired(), Length(min = 2, max = 20)])
    #ks_relative_rating = StringField('Relative Discrimination Rating', validators=[DataRequired(), Length(min = 2, max = 20)])
    #discriminatory_rating = StringField('Final Discrimination Rating', validators=[DataRequired(), Length(min = 2, max = 20)])
    #psi_rating = StringField('PSI Rating', validators=[DataRequired(), Length(min = 2, max = 20)])
    final_rating = SelectField('Final Rating', choices = ['Accepted', 'Rebuild', 'Other'], validators=[DataRequired(), Length(min = 2, max = 20)])
    final_rating_comments = TextAreaField('Detailed Report', validators=[Length(min = 0, max = 500)], widget=TextArea(), render_kw={"rows": 10, "cols": 70})
    pdv_date = DateField('PDV Date', validators=[DataRequired()],render_kw = {'type': 'date'})
    report_owner = StringField('Report Owner', validators=[DataRequired(), Length(min = 2, max = 20)])
    attached_report = FileField('Attach Report', validators=[DataRequired()], render_kw = {'type': 'file', 'class': 'div-input-file'})

    submit = SubmitField('Sumbit PDV Report')

class MonitoringForm(FlaskForm):
    monitoring_period = StringField('Monitoring Period', validators=[DataRequired(), Length(min = 2, max = 20)])
    current_period = StringField('Current Period', validators=[DataRequired(), Length(min = 2, max = 20)])
    proxy_bad_definition = StringField('Proxy Bad Definition (Optional)')
    monitoring_ks = FloatField('Monitoring KS', validators=[DataRequired()])
    psi = FloatField('PSI', validators=[DataRequired()])
    final_rating = SelectField('Final Rating', choices = ['Accepted', 'Rebuild', 'Other'], validators=[DataRequired(), Length(min = 2, max = 20)])
    final_rating_comments = TextAreaField('Detailed Report', validators=[Length(min = 0, max = 500)], widget=TextArea(), render_kw={"rows": 10, "cols": 70})
    monitoring_date = DateField('Monitoring Date', validators=[DataRequired()],render_kw = {'type': 'date'})
    attached_report = FileField('Attach Report', validators=[DataRequired()],render_kw = {'type': 'file'})
    report_owner = StringField('Report Owner', validators=[DataRequired(), Length(min = 2, max = 20)])
    submit = SubmitField('Sumbit Monitoring Report')