from flask import (Flask , request , g, make_response, render_template, 
                    session, redirect, url_for, flash )
from app.main import main
from app.models import Employer
from datetime import datetime
from app.main.forms import NameForm




# Creating a route i.e matching the url with the function
@main.route('/')
@main.route('/home')
def home():
    date = datetime.utcnow()
    test = 'https://www.youtube.com'
    return render_template('index.html', date=date, test=test)


@main.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html')

@main.route('/salespage', methods=['GET', 'POST'])
def sale_page():
    return render_template('sales-page.html')

@main.route("/test", methods=['GET', 'POST'])
def test():
    form = NameForm()
    print('before')
    if form.validate_on_submit():
        user = Employer.query.filter_by(username=form.name.data).first()
        print('after')
        if user is None:
            session['KNOWN'] = False
            user = Employer(username=form.name.data, email = form.name.data, first_name = form.name.data, last_name=form.name.data )
            db.session.add(user)
            db.session.commit()
        else:
            print('know')
            session['KNOWN'] = True
        session['name'] = user.username
        return redirect(url_for('main.text'))
    return render_template('text.html', name=session.get('name'), form=form, known=session.get('KNOWN') )





