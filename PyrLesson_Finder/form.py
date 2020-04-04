from wtforms import Form, StringField, PasswordField, SubmitField, BooleanField, SelectField, SelectMultipleField, \
    DateTimeField, IntegerField, DateField, TimeField, RadioField, validators
from wtforms import IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from wtforms_components import TimeField, DateField
from .models import User
from .services.user_record import UserService


levels = [('None', 'None'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6')]
days = [('None', 'None'), ('Monday', 'Monday'), ('Tuesday', 'Tuesday'),
                                                  ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'),
                                                  ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')]


class SignupForm(Form):
    active = True
    fName = StringField('First Name', validators=[DataRequired()])
    lName = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    birthday = DateField('Birthday', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class SearchForm(Form):
    location = StringField('Location')
    organization = StringField('Organization')
    startDate = DateField('Start Date', validators=[Optional()])
    startTime = TimeField('Start Time', validators=[Optional()])
    day = SelectField('Day of the Week', choices=days)
    level = SelectField('Level', choices=levels)
    submit = SubmitField('Search')


class LessonForm(Form):
    name = StringField('Name')
    startDate = DateField('Start Date', render_kw={'placeholder': 'MM/DD/YYYY'})
    endDate = DateField('End Date', render_kw={'placeholder': 'MM/DD/YYYY'})
    startTime = TimeField('Start Time', render_kw={'placeholder': 'HH:MM'})
    endTime = TimeField('End Time', render_kw={'placeholder': 'HH:MM'})
    email = StringField('Contact Email')
    level = SelectField('Level', choices=levels[1:7])
    location = StringField('Location')
    desc = StringField('Add Description')
    cap = IntegerField('Max Enrollment')
    instructor = StringField('Instructor')
    submit = SubmitField('Create Lesson')
    day = SelectField('Day of the Week', choices=days)


class RegistrationForm(Form):
    fName = StringField('First Name of Participant', validators=[DataRequired()])
    lName = StringField('Last Name of Participant', validators=[DataRequired()])
    contactNum = StringField('Contact Phone Number (Optional)', validators=[Optional()], render_kw={'placeholder': '123-456-7890'})
    contactEmail = StringField('Contact Email', validators=[DataRequired()])
    submit = SubmitField('Register')


class UpdateUsernameForm(Form):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Submit Changes')

    # TODO: figure out why this doesn't work
    # def validate_username(self, username):
    #     pdb.set_trace()
    #     user = UserService.by_username(username, request)
    #     if user:
    #         raise ValidationError('Username is taken. Choose another.')


class EditRegistrationForm(Form):
    contactNum = StringField('Contact Phone Number', render_kw={'placeholder': '123-456-7890'})
    contactEmail = StringField('Contact Email', validators=[Optional()])
    submit = SubmitField('Submit Changes')




