from flaskblog import db
from flaskblog.models import City,Country
from flaskblog import create_app

app = create_app()

with app.app_context():
    db.init_app(app)
    db.drop_all()
    db.create_all()
    
    romania = Country(name="Romania")
    germania = Country(name="Germany")
    franta = Country(name="France")

    buc = City(name="Bucharest",country=romania)
    cluj = City(name="Cluj",country=romania)
    sibiu = City(name="Sibiu",country=romania)
    brasov = City(name="Brasov",country=romania)

    db.session.add(romania)
    db.session.add(germania)
    db.session.add(franta)
    db.session.add(buc)
    db.session.add(sibiu)
    db.session.add(cluj)
    db.session.add(brasov)

    db.session.commit()
