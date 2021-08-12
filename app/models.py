from app import db
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash


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
    time = db.Column(db.DateTime(), default=datetime.utcnow, nullable = False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return 'Employer {0}'.format(self.username)

    @property
    def password(self):
        raise AttributeError("Password is not readable")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)




class Position(db.Model):
    __tablename__ = 'positions'
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(64), nullable=False, unique=True)
    employers = db.relationship('Employer', backref='position')

    def __repr__(self):
        return 'Position {0}'.format(self.role)