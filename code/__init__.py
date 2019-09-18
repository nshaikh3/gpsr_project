from flask import Flask, request, render_template, url_for, flash
from flask_bootstrap import Bootstrap
from processing import hhicalc, gpol, rec_red, rec_red_plot
from forms import *


app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'SjdnUends821Jsdlkvxh391ksdODnejdDw'
bootstrap = Bootstrap(app)

@app.route("/", methods=["GET", "POST"])
def homepage():
    return render_template("home.html")


@app.route("/gpsr", methods=["GET", "POST"])
def calculate():
    form = gpsr_calc_form()
    if form.validate_on_submit():
        flash('Calculation successful')
        country = form.country.data
        material = form.material.data
        year = form.year.data
        indicator = form.indicator.data

        hhi = hhicalc(material, year)
        gpsr = gpol(year, country, material, indicator)
        return render_template('gpsr.html', form=form, country=country, hhi=hhi, gpsr=gpsr, indicator=indicator)
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

        hhi = hhicalc(material, year)
        gpsr = gpol(year, country, material, indicator)
        rec = rec_red(year, country, material, reduction, indicator)
        best_case = rec[0]
        worst_case = rec[1]

        graph1_url = rec_red_plot(year, country, material)

        return render_template('recycling.html', form=form1, country=country, hhi=hhi, gpsr=gpsr, reduction=rec, indicator=indicator, 
         best_case = best_case, worst_case = worst_case, graph1=graph1_url)
    return render_template('recycling.html', form=form1)

@app.route('/graphs')
def graphs():
 
    graph1_url = rec_red_plot(2016, 97, 810411)
    graph2_url = rec_red_plot(2016, 97, 810194)
    graph3_url = rec_red_plot(2016, 97, 7403)
    graph4_url = rec_red_plot(2016, 97, 7601)

    return render_template('graphs.html', graph1=graph1_url, graph2=graph2_url, graph3=graph3_url, graph4=graph4_url)

if __name__ == "__main__":
    app.run(debug=True)