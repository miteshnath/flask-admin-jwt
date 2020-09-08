"""Sign-up & log-in forms."""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

from app import db
from app.models import User


class SignupForm(FlaskForm):
    """User Sign-up Form."""
    username = StringField(
        'Name',
        validators=[DataRequired()]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=6, message='Select a stronger password.')
        ]
    )
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    """User Log-in Form."""
    username = StringField(
        'Name',
        validators=[DataRequired()]
    )
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')
    
    def get_user(self):
        return db.session.query(User).filter_by(username=self.username.data).first()