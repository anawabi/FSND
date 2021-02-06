from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
db = SQLAlchemy()
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    website=db.Column(db.String(200), default='No Website', nullable=True)
    phone = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=False, nullable=True)
    seeking_description = db.Column(db.String(), default='Not currently seeking performance venues', nullable=True)
    image_link = db.Column(db.String(500))
    genres = db.Column(db.ARRAY(db.String()))
    facebook_link = db.Column(db.String(120))
    venue_shows = db.relationship('Show', backref='Venue', lazy=True, cascade='all, delete-orphan')

    
    def __repr__(self):
        return f'<Venue {self.id} {self.name}>'

    # TODO: implement any missing fields, as a database migration using Flask-Migrate - COMPLETED

class Artist(db.Model):
    __tablename__ = 'Artist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(200))
    seeking_venue = db.Column(db.String())
    seeking_description = db.Column(db.String(1000))
    artist_shows = db.relationship('Show', backref='Artist', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Artist {self.id} {self.name}>'

    # TODO: implement any missing fields, as a database migration using Flask-Migrate -COMPLETED

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration. - COMPLETED
class Show(db.Model):
  __tablename__ = 'Show'

  id = db.Column(db.Integer, primary_key=True)
  start_time = db.Column(db.DateTime())
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)

  def __repr__(self):
        return f'<Show {self.id} {self.start_time}>'