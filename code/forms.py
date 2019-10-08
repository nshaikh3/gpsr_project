from flask_wtf import FlaskForm
from wtforms import IntegerField, TextField, SubmitField, SelectField
from wtforms.validators import DataRequired
from processing import countries, materials, wgi

country_list = countries.loc[:, "Country Name"]

country_list = list(zip(country_list.index, country_list))

indicator_list = [("WGI Score", "WGI Score"), ("HDI Score", "HDI Score")]



class gpsr_calc_form(FlaskForm):
    country = SelectField('Country Code', choices=country_list, coerce=int, validators=[DataRequired()])
    material = IntegerField('Material', validators=[DataRequired()])
    year = IntegerField('Year', validators=[DataRequired()])
    indicator = SelectField(label='Indicators', choices=indicator_list, validators=[DataRequired()])
    submit = SubmitField('Calculate')

class rec_calc_form(FlaskForm):
    country = SelectField('Country Code', choices=country_list, coerce=int, validators=[DataRequired()])
    material = IntegerField('Material', validators=[DataRequired()])
    year = IntegerField('Year', validators=[DataRequired()])
    indicator = SelectField(label='Indicators', choices=indicator_list, validators=[DataRequired()])
    reduction = IntegerField('Reduction Rate', validators=[DataRequired()])
    submit = SubmitField('Calculate')