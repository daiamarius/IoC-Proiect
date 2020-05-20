from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, RadioField,IntegerField, SelectField,MultipleFileField
from wtforms.validators import DataRequired,NumberRange,ValidationError,Length
from flask_wtf.file import FileAllowed
import subprocess
def validate_number(a):
    try:
        if a.isdigit():
            return True
        else:
            return False
    except ValueError as err:
        return False

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(),Length(min=5,max=50)])
    content = TextAreaField('Additional details', validators=[DataRequired()])
    
    postType = RadioField('Annoucement Type', choices=[('Sell','Sell'),('Rent','Rent')], validators=[DataRequired()])
    houseType = RadioField('Immobile Type', choices=[('Apartment', 'Apartment'),('House', 'House')], validators=[DataRequired()])
    
    price = StringField('Price (€)', validators=[DataRequired()])
    sqMeters = StringField('SquareMeters (m2)', validators=[DataRequired()])
    nmbRooms = StringField('Number of rooms', validators=[DataRequired()])

    country = SelectField('Country', validators=[DataRequired()])
    city = SelectField('City', validators=[DataRequired()])

    address = StringField('Address', validators=[DataRequired(),Length(min=5,max=50)])

    picture = MultipleFileField('Choose pictures', validators=[FileAllowed(['jpg', 'png'],"Wrong format! Allowed: .jpg, .png")])

    phonenumber = StringField('Additional phone number(optional)')
    submit = SubmitField('Submit post')

    def __init__(self,city_choices,country_choices):
        FlaskForm.__init__(self)
        self.country.choices = country_choices
        self.city.choices = city_choices
    
    def validate_price(self,price):
        if not validate_number(self.price.data):
            raise ValidationError('Please input a number!')

    def validate_sqMeters(self,sqMeters):
        if not validate_number(self.sqMeters.data):
            raise ValidationError('Please input a number!')
        if int(self.sqMeters.data)<10:
            raise ValidationError('Please input a valid input!')
        if int(self.sqMeters.data)>400:
            raise ValidationError('Please input a valid input!')

    def validate_nmbRooms(self,nmbRooms):
        if not validate_number(self.nmbRooms.data):
            raise ValidationError('Please input a number!')
        if int(self.nmbRooms.data)<1:
            raise ValidationError('Please input a valid input!')
        if int(self.nmbRooms.data)>15:
            raise ValidationError('Please input a valid input!')

    def validate_address(self,address):
        if len(self.address.data)<10:
            raise ValidationError('Address too short!')
        if len(self.address.data)>30:
            raise ValidationError('Address too long!')


class CardForm(FlaskForm):
    cardname = StringField('Name on card')
    cardnumber = StringField('Card number')
    expirationdate = StringField('Expiration Date')
    cpv = StringField('CPV Code')
    submit = SubmitField('Pay')
