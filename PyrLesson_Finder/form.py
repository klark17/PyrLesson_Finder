from wtforms import Form, StringField, PasswordField, SubmitField, BooleanField, SelectField, SelectMultipleField, \
    DateTimeField, IntegerField, DateField, TimeField, RadioField, validators
from wtforms import IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from wtforms.widgets import HiddenInput
from wtforms_components import TimeField, DateField, DateRange
from datetime import date
from dateutil.relativedelta import relativedelta

strip_filter = lambda x: x.strip() if x else None
levels = [('None', 'None'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6')]
days = [('None', 'None'), ('Monday', 'Monday'), ('Tuesday', 'Tuesday'),
                                                  ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'),
                                                  ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')]


class SignupForm(Form):
    active = True
    fName = StringField('First Name', validators=[DataRequired()], filters=[strip_filter])
    lName = StringField('Last Name', validators=[DataRequired()], filters=[strip_filter])
    username = StringField('Username',
                           validators=[DataRequired(),
                                       Length(min=2, max=20)],
                           filters=[strip_filter])
    email = StringField('Email', validators=[DataRequired(), Email()], filters=[strip_filter])
    birthday = DateField('Birthday', validators=[DataRequired(), DateRange(max=date.today()-relativedelta(years=18))])
    password = PasswordField('Password', validators=[DataRequired()], filters=[strip_filter])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                     EqualTo('password')],
                                     filters=[strip_filter])
    submit = SubmitField('Sign Up')


class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired()], filters=[strip_filter])
    password = PasswordField('Password', validators=[DataRequired()], filters=[strip_filter])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class SearchForm(Form):
    location = StringField('Location', filters=[strip_filter])
    organization = StringField('Organization', filters=[strip_filter])
    startDate = DateField('Start Date', validators=[Optional()])
    startTime = TimeField('Start Time', validators=[Optional()])
    day = SelectField('Day of the Week', choices=days)
    level = SelectField('Level', choices=levels)
    submit = SubmitField('Search')


class LessonForm(Form):
    name = StringField('Name', filters=[strip_filter])
    startDate = DateField('Start Date', render_kw={'placeholder': 'MM/DD/YYYY'})
    endDate = DateField('End Date', render_kw={'placeholder': 'MM/DD/YYYY'})
    startTime = TimeField('Start Time', render_kw={'placeholder': 'HH:MM'})
    endTime = TimeField('End Time', render_kw={'placeholder': 'HH:MM'})
    email = StringField('Contact Email', filters=[strip_filter])
    level = SelectField('Level', choices=levels[1:7])
    location = StringField('Location', filters=[strip_filter])
    desc = StringField('Add Description', filters=[strip_filter])
    cap = IntegerField('Max Enrollment', filters=[strip_filter])
    instructor = StringField('Instructor', filters=[strip_filter])
    submit = SubmitField('Create Lesson')
    day = SelectField('Day of the Week', choices=days)


class RegistrationForm(Form):
    fName = StringField('First Name of Participant', validators=[DataRequired()], filters=[strip_filter])
    lName = StringField('Last Name of Participant', validators=[DataRequired()], filters=[strip_filter])
    contactNum = StringField('Contact Phone Number (Optional)',
                             validators=[Optional()],
                             render_kw={'placeholder': '123-456-7890'},
                             filters=[strip_filter])
    contactEmail = StringField('Contact Email', validators=[DataRequired()], filters=[strip_filter])
    submit = SubmitField('Register')


class UpdateUsernameForm(Form):
    id = IntegerField(widget=HiddenInput())
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)],
                           filters=[strip_filter])
    submit = SubmitField('Submit Changes')


class EditRegistrationForm(Form):
    contactNum = StringField('Contact Phone Number',
                             render_kw={'placeholder': '123-456-7890'},
                             filters=[strip_filter])
    contactEmail = StringField('Contact Email',
                               validators=[Optional()],
                             filters=[strip_filter])
    submit = SubmitField('Submit Changes')




