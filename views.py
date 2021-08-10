from flask import Flask , request , g, make_response, render_template, session, redirect, url_for, flash 
from flask_script import Manager, Shell
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate, MigrateCommand
from datetime import datetime
from forms import NameForm
import os

basedir = os.path.abspath(os.path.dirname(__file__))

username = "makeem49"
password = "Olayinka1?"
dbname = "management"



app = Flask(__name__)
app.config['SECRET_KEY'] = '369f9d5158f5ec45f4c51ce6a1ab74'
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{username}:{password}@localhost/{dbname}"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


manager = Manager(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(64), nullable = False, unique = True, index=True)
    description = db.Column(db.Text, nullable = False)
    employers = db.relationship('Employer', backref='product', lazy='dynamic', cascade = 'all, delete')

    def __repr__(self):
        return '{0} products'.format(self.product_name)


class Employer(db.Model):
    __tablename__ = 'employers'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(28), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    first_name = db.Column(db.String(44), unique=True, nullable=False)
    last_name = db.Column(db.String(44), unique=True, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    position_id = db.Column(db.Integer, db.ForeignKey('positions.id'))

    def __repr__(self):
        return 'Employer {0}'.format(self.username)


class Position(db.Model):
    __tablename__ = 'positions'
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(64), nullable=False, unique=True)
    employers = db.relationship('Employer', backref='position')

    def __repr__(self):
        return 'Position {0}'.format(self.role)


def make_shell_context():
    return dict(app=app, db=db, Product=Product, Employer=Employer, Position=Position)

manager.add_command('shell', Shell(make_context = make_shell_context))
manager.add_command('db', MigrateCommand)



# Creating a route i.e matching the url with the function
@app.route('/')
@app.route('/home')
def home():
    date = datetime.utcnow()
    test = 'https://www.youtube.com'
    return render_template('index.html', date=date, test=test)


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html')

@app.route('/salespage', methods=['GET', 'POST'])
def sale_page():
    return render_template('sales-page.html')

@app.route("/test", methods=['GET', 'POST'])
def text():
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
        return redirect(url_for('text'))
    return render_template('text.html', name=session.get('name'), form=form, known=session.get('KNOWN') )

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/error404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error/error500.html'), 500



if __name__ == '__main__':
    manager.run()