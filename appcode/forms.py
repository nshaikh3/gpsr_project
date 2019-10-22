from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, SelectField, PasswordField, BooleanField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from appcode.models import User
from appcode.processing import countries, materials, wgi

country_list = countries.loc[:, "Country Name"]
country_list = list(zip(country_list.index, country_list))

material_list = materials.loc[:, "Commodity"]
material_list = list(zip(material_list.index, material_list))

indicator_list = [("WGI Score", "WGI Score"), ("HDI Score", "HDI Score"), ("CPI Score", "CPI Score")]

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class gpsr_calc_form(FlaskForm):
    country = SelectField('Country Code', choices=country_list, coerce=int, validators=[DataRequired()])
    material = SelectField('Material', choices=material_list, coerce=int, validators=[DataRequired()])
    year = IntegerField('Year', validators=[DataRequired()])
    indicator = SelectField(label='Indicators', choices=indicator_list, validators=[DataRequired()])
    submit = SubmitField('Calculate')

class rec_calc_form(FlaskForm):
    country = SelectField('Country Code', choices=country_list, coerce=int, validators=[DataRequired()])
    material = SelectField('Material', choices=material_list, coerce=int, validators=[DataRequired()])
    year = IntegerField('Year', validators=[DataRequired()])
    indicator = SelectField(label='Indicators', choices=indicator_list, validators=[DataRequired()])
    reduction = IntegerField('Reduction Rate', validators=[DataRequired()])
    submit = SubmitField('Calculate')