from appcode import app, db
from flask import request, render_template, url_for, flash, redirect, send_file
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from io import BytesIO
from appcode.processing import *
from appcode.forms import RegistrationForm, LoginForm, gpsr_calc_form, rec_calc_form
from appcode.models import *

@app.route("/", methods=["GET", "POST"])
def homepage():
    return render_template("home.html", title="Home")

@app.route("/about", methods=["GET", "POST"])
def aboutpage():
    return render_template("about.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('homepage')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('homepage'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/gpsr", methods=["GET", "POST"])
@login_required
def calculate():
    form = gpsr_calc_form()
    showresult = Result.query.all()
    
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
        result = Result(countryname=countryname, materialname=materialname, indicatorname=indicator,
         year=year, hhi=hhi, gpsr=gpsr)
        db.session.add(result)
        db.session.commit()
        showresult = Result.query.all()
        xresult1 = [r.materialname for r in Result.query.filter(Result.indicatorname=="WGI Score")
        .with_entities(Result.materialname).order_by(Result.id)]
        xresult2 = [r.materialname for r in Result.query.filter(Result.indicatorname=='HDI Score')
        .with_entities(Result.materialname).order_by(Result.id)]
        yresult1 = [r.gpsr for r in Result.query.filter(Result.indicatorname=="WGI Score")
        .with_entities(Result.gpsr).order_by(Result.id)]
        yresult2 = [r.gpsr for r in Result.query.filter(Result.indicatorname=='HDI Score')
        .with_entities(Result.gpsr).order_by(Result.id)]
        graph1 = gpsrplot(xresult1, xresult2, yresult1, yresult2)
        graph2 = indicatorplot(country)
        #graph3 = timeplot(material, country, indicator)
        return render_template('gpsr.html', form=form, results=showresult, plot1=graph1, plot2=graph2,
         xresult1=xresult1, xresult2=xresult2, yresult1=yresult1, yresult2=yresult2, countryname=countryname)
    return render_template('gpsr.html', form=form, results=showresult)


@app.route("/deletegpsr", methods=["POST"])
def deletegpsr():
    resultid = request.form.get("resultid")
    result = Result.query.filter_by(id=resultid).first()
    db.session.delete(result)
    db.session.commit()
    return redirect("/gpsr")

@app.route("/download", methods=["GET", "POST"])
@login_required
def download():
    df = pd.read_sql(sql = db.session.query(Result)\
                         .with_entities(Result.countryname, Result.materialname,
                         Result.indicatorname, Result.year, Result.hhi,
                         Result.gpsr).statement, con = db.session.bind)
    strIO = BytesIO()
    excel_writer = pd.ExcelWriter(strIO, engine="xlsxwriter")
    df.to_excel(excel_writer, sheet_name="sheet1")
    excel_writer.save()
    excel_data = strIO.getvalue()
    strIO.seek(0)

    return send_file(strIO,
     attachment_filename='data.xlsx',
     as_attachment=True)

@app.route("/recycling", methods=["GET", "POST"])
@login_required
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