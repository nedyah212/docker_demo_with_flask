from .logging import logger
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Regexp
from . models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',validators=[DataRequired(),Regexp(
                r'^[\w\.-]+@[\w\.-]+\.\w+$',
                message="Invalid email format")])

    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=60)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    # custom username check
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            logger.warning(f"ContstraintViolation: {user} allready exists in the database")
            raise ValidationError('That username is already taken. Please choose another.')

    # custom email check
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            logger.warning(f"ContstraintViolation: {user} allready exists in the database")
            raise ValidationError('That email is already registered. Please log in.')