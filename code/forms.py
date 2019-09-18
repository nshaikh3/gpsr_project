from flask_wtf import FlaskForm
from wtforms import IntegerField, TextField, SubmitField, SelectField
from wtforms.validators import DataRequired
from processing import countries, materials, wgi


class gpsr_calc_form(FlaskForm):
    country = IntegerField('Country Code', validators=[DataRequired()])
    material = IntegerField('Material', validators=[DataRequired()])
    year = IntegerField('Year', validators=[DataRequired()])
    indicator = TextField('Indicator Selection', validators=[DataRequired()])
    submit = SubmitField('Calculate')

country_list = countries.loc[:, "Country Name"]

country_list = tuple(zip(country_list.index, country_list))

class rec_calc_form(FlaskForm):
    #country = SelectField(u'Country Code', choices=country_list, validators=[DataRequired()])
    country = IntegerField('Country Code', validators=[DataRequired()])
    material = IntegerField('Material', validators=[DataRequired()])
    year = IntegerField('Year', validators=[DataRequired()])
    indicator = TextField('Indicator Selection', validators=[DataRequired()])
    reduction = IntegerField('Reduction Rate', validators=[DataRequired()])
    submit = SubmitField('Calculate')