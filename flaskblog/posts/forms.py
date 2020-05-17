from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, RadioField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    
    postType = RadioField('Label', choices=[('Sell','Sell'),('Rent','Rent')])
    houseType = RadioField('Label2', choices=[('Apartment', 'Apartment'),('House', 'House')])
    
    price = StringField('Price', validators=[DataRequired()])
    sqMeters = StringField('SquareMeters', validators=[DataRequired()])
    nmbRooms = StringField('NumberRooms', validators=[DataRequired()])

    country = StringField('Country', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])

    address = StringField('Address', validators=[DataRequired()])

    upload = SubmitField('Upload Image')

    submit = SubmitField('Post')
