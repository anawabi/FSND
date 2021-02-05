#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from datetime import datetime
from models import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database - Done


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    if isinstance(value, str):
        date = dateutil.parser.parse(value)
    else:
        date = value
    return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#
#Ready
@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------
#Ready
@app.route('/venues')
def venues():
    # TODO: replace with real venues data. - Completed
    #num_shows should be aggregated based on number of upcoming shows per venue.
    data = []
    locations = set()
    areas = Venue.query.all()
    for area in areas:
        locations.add((area.city, area.state))
    for location in locations:
        data.append({
            "city": location[0],
            "state": location[1],
            "venues": []
        })

    for area in areas:
        num_upcoming_shows = 0
        shows = Show.query.filter_by(venue_id=area.id).all()
        now = datetime.now()
        
        for show in shows:
            if show.start_time > now:
               num_upcoming_shows += 1

        for location in data:
            if area.state == location['state'] and area.city == location['city']:
               location['venues'].append({
                    "id": area.id,
                    "name": area.name,
                    "num_upcoming_shows": num_upcoming_shows
               })
    return render_template('pages/venues.html', areas=data)

#Ready
@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term = request.form.get('search_term', '')
  venues = Venue.query.filter(Venue.name.ilike('%{}%'.format(search_term))).all()
  response = {
      "count": len(venues),
      "data": venues
      }
  return render_template('pages/search_venues.html', results=response, search_term=search_term)

#Ready
@app.route('/venues/<int:venue_id>', methods=['GET'])
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id - Completed
    venue = db.session.query(Venue).filter(Venue.id == venue_id).first()
    # genres = venue.genres.split(",")

    now = datetime.utcnow()
    venue.upcoming_shows = (
        db.session.query(Show)
        .join(Venue, Show.venue_id == Venue.id)
        .filter(Show.venue_id == venue_id, Show.start_time > now)
        .all()
    )
    venue.upcoming_shows_count = len(venue.upcoming_shows)
    venue.past_shows = (
        db.session.query(Show)
        .join(Venue, Show.venue_id == Venue.id)
        .filter(Show.venue_id == venue_id, Show.start_time < now)
        .all()
    )    
    return render_template('pages/show_venue.html', venue=venue)


#  Create Venue
#  ----------------------------------------------------------------
#Ready
@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

#Ready
@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead -COMPLETED
    response = {}
    error = False
    try:
        name = request.form.get("name")
        city = request.form.get("city")
        state = request.form.get("state")
        address = request.form.get("address")
        phone = request.form.get("phone")
        facebook_link = request.form.get("facebook_link")
        genres = request.form.getlist("genres")
        venue = Venue(
            name=name,
            city=city,
            state=state,
            address=address,
            phone=phone,
            genres=genres,
            facebook_link=facebook_link,
        )
        response["name"] = venue.name
        db.session.add(venue)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()
        if error == False:
            flash("Venue " + response["name"] + " was successfully listed!")
        else:
            flash(
                "An error occurred. Venue "
                + request.form["name"]
                + " could not be listed."
            )
    return render_template("pages/home.html")

  


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):

  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    error = False
    try:
        venue = Venue.query.filter_by(id=venue_id).first_or_404()
        db.session.delete(venue)
        db.session.commit()
    except():
        db.session.rollback()
        error = True
    finally:
        db.session.close()
    if error:
        flash('An error occured and venue, ' + venue.name + ', could not be deleted.')
        abort(500)
    else:
        flash('The venue, ' + venue.name + ', was deleted.')
        return render_template('pages/home.html')
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
    return None

#  Artists
#  ----------------------------------------------------------------
#Ready
@app.route('/artists')
def artists():
    # TODO: replace with real data returned from querying the database
    data = []
    artists = Artist.query.all()
    for artist in artists:
        data.append(artist)
    return render_template('pages/artists.html', artists=data)
 
#Ready
@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term = request.form.get('search_term', '')
  artists = Artist.query.filter(Artist.name.ilike('%{}%'.format(search_term))).all()
  response = {
      "count": len(artists),
      "data": artists
  }
  return render_template('pages/search_artists.html', results=response, search_term=search_term)

#Ready
@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id - COMPLETED
    artist = Artist.query.filter_by(id=artist_id).first()
    now = datetime.utcnow()
    artist.upcoming_shows = (
        db.session.query(Show)
        .join(Artist, Show.artist_id == artist_id)
        .filter(Show.artist_id == artist_id, Show.start_time > now)
        .all()
    )
    if len(artist.upcoming_shows):
        artist.upcoming_shows_count = len(artist.upcoming_shows)
    artist.past_shows = (
        db.session.query(Show)
        .join(Artist, Show.artist_id == Artist.id)
        .filter(Show.artist_id == artist_id, Show.start_time < now)
        .all()
    )
    if len(artist.past_shows):
        artist.past_shows_count = len(artist.past_shows)

    print(artist.genres)

    return render_template("pages/show_artist.html", artist=artist)    

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)



@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

#Ready
@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)
#Ready
@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
    response = {}
    error = False
    try:
        name = request.form.get("name")
        city = request.form.get("city")
        state = request.form.get("state")
        phone = request.form.get("phone")
        genres = request.form.getlist("genres")
        facebook_link = request.form.get("facebook_link")
        artist = Artist(
            name=name,
            city=city,
            state=state,
            phone=phone,
            genres=genres,
            facebook_link=facebook_link,
        )
        response["name"] = artist.name
        db.session.add(artist)
        db.session.commit()
    except:
        error = True
        flash("An error occurred. Artist " + name + " could not be listed.")
        db.session.rollback()
    finally:
        db.session.close()
        if error == False:
            flash("Artist " + response["name"] + " was successfully listed!")

    return render_template("pages/home.html")


#  Shows
#  ----------------------------------------------------------------
#Ready
@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data. COMPLETED
    # num_shows should be aggregated based on number of upcoming shows per venue.
    data = []
    shows = Show.query.order_by(Show.start_time.desc()).all()
    for show in shows:
        venue = Venue.query.filter_by(id=show.venue_id).first_or_404()
        artist = Artist.query.filter_by(id=show.artist_id).first_or_404()
        data.extend([{
            "venue_id": venue.id,
            "venue_name": venue.name,
            "artist_id": artist.id,
            "artist_name": artist.name,
            "artist_image_link": artist.image_link,
            "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M")
        }])
    return render_template('pages/shows.html', shows=data)


#Ready    
@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

#Ready
@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
   if request.method == 'POST':
       error = False
       artist_id = request.form['artist_id']
       venue_id = request.form['venue_id']
       start_time = request.form['start_time']
       # TODO: modify data to be the data object returned from db insertion
       show = Show(artist_id=artist_id,
                    venue_id=venue_id,
                    start_time=start_time)
       try:
           print(show)
           db.session.add(show)
           db.session.commit()
            # on successful db insert, flash success
           flash('Show was successfully listed!')
           # TODO: on unsuccessful db insert, flash an error instead.
           # e.g., flash('An error occurred. Show could not be listed.')
           # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
       except:
           db.session.rollback()
           error = True
           # on unsuccessful db insert, flash an error instead.
           flash('An error occurred. The show could not be listed.')
           print(sys.exe_info())
       finally:
           db.session.close()
   return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
