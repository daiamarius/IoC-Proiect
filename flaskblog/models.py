from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flaskblog import db, login_manager
from flask_login import UserMixin



images_posts = db.Table('images_posts',
            db.Column('image_id',db.Integer,db.ForeignKey('image.id')),
            db.Column('post_id',db.Integer,db.ForeignKey('post.id')),
            db.PrimaryKeyConstraint('image_id','post_id'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)
    anouncement_type = db.Column(db.String(20), nullable=False)
    house_type = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    square_meters = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(100), nullable=False)

    images = db.relationship('Image', secondary=images_posts)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cities = db.relationship('City', back_populates="country",cascade="all, delete-orphan")

    def __repr__(self):
        return f"Country('{self.name})"

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=False)
    country = db.relationship('Country', back_populates="cities")
    posts = db.relationship('Post', backref='city', lazy=True)

    def __repr__(self):
        return f"City('{self.name})"

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    post = db.relationship('Post', secondary=images_posts)