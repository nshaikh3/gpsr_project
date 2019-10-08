from flask import Flask, request, render_template, url_for, flash, redirect
from processing import *
from forms import *


app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'SjdnUends821Jsdlkvxh391ksdODnejdDw'

@app.route("/", methods=["GET", "POST"])
def homepage():
    return render_template("home.html")

@app.route("/about", methods=["GET", "POST"])
def aboutpage():
    return render_template("about.html")

@app.route("/gpsr", methods=["GET", "POST"])
def calculate():
    form = gpsr_calc_form()
    if form.validate_on_submit():
        flash('Calculation successful')
        country = form.country.data
        material = form.material.data
        year = form.year.data
        indicator = form.indicator.data

        countryname = country_name(form.country.data)
        materialname = material_name(form.material.data)
        hhi = hhicalc(material, year)
        hhi = format(hhi[0], '.3f')
        gpsr = gpol(year, country, material, indicator)
        gpsr = format(gpsr, '.3f')
        return render_template('gpsr.html', form=form, countryname=countryname, materialname=materialname,
         hhi=hhi, gpsr=gpsr, indicator=indicator)
    return render_template('gpsr.html', form=form)

@app.route("/recycling", methods=["GET", "POST"])
def calculate1():
    form1 = rec_calc_form()
    if form1.validate_on_submit():
        flash('Calculation successful')
        country = form1.country.data
        material = form1.material.data
        year = form1.year.data
        reduction = form1.reduction.data
        indicator = form1.indicator.data

        countryname = country_name(form1.country.data)
        materialname = material_name(form1.material.data)        

        hhi = hhicalc(material, year)
        hhi = format(hhi[0], '.3f')
        gpsr = gpol(year, country, material, indicator)
        gpsr = format(gpsr, '.3f')
        rec = rec_red(year, country, material, reduction, indicator)
        best_case = format(rec[0], '.3f')
        worst_case = format(rec[1], '.3f')

        graph = rec_red_plot(year, country, material, reduction)

        return render_template('recycling.html', form=form1, countryname=countryname,
         materialname=materialname, hhi=hhi, gpsr=gpsr, reduction=rec, indicator=indicator, 
         best_case = best_case, worst_case = worst_case, plot=graph)
    return render_template('recycling.html', form=form1)

@app.route('/graphs')
def graphs():
 
    graph = indicatorplot(842)

    return render_template('graphs.html', plot=graph)

if __name__ == "__main__":
    app.run(debug=True)