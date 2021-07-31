from flask import Flask , request , g, make_response, render_template
from flask_script import Manager
from flask_moment import Moment
from datetime import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = '369f9d5158f5ec45f4c51ce6a1ab74'

manager = Manager(app)
moment = Moment(app)

# Creating a route i.e matching the url with the function
@app.route('/')
@app.route('/home')
def index():
    date = datetime.utcnow()
    test = 'https://www.youtube.com'
    return render_template('index.html', date=date, test=test)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error500.html'), 500



if __name__ == '__main__':
    manager.run()