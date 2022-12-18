from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,EmailField
from wtforms.validators import DataRequired,EqualTo,Length,Email,ValidationError
from app.models import *

#** The form used for the sign in page (to fetch data )
class LoginForm(FlaskForm):
    username = StringField('username',validators=[DataRequired()])
    password = PasswordField('password',validators=[DataRequired()])
    remember_me = BooleanField('remember_me')
    submit = SubmitField('Sign In')
    
#** The form used for the sign up page (to fetch data )
class SignUpForm(FlaskForm):
    email = EmailField('email',validators=[DataRequired(),Email(message="Invalid Email"),Length(max=50)])
    username = StringField('username',validators=[DataRequired(),Length(min=4,max=15)])
    password = PasswordField('password',validators=[DataRequired(),Length(min=8,max=40)])
    password2 = PasswordField('password2',validators=[DataRequired(),EqualTo('password')])
    register = SubmitField('Register')
    #!! Check whether the username given have been used
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
    #!! Check whether a email given have been used
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
