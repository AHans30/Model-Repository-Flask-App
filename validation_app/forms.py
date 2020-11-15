from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from validation_app.models import User


class RegistrationForm(FlaskForm):
    ad_id = StringField('AD ID', validators=[DataRequired(), Length(min = 2, max = 20)])
    password = PasswordField('Password',  validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')

    def validate_ad_id(self, ad_id):
        user = User.query.filter_by(ad_id = ad_id.data).first()
        if user:
            raise ValidationError('Given AD ID is already registered!')

class LoginForm(FlaskForm):
    ad_id = StringField('AD ID', validators=[DataRequired(), Length(min = 2, max = 20)])
    password = PasswordField('Password',  validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')