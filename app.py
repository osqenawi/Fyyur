# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#
from sys import exc_info
from datetime import datetime
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from flask_migrate import Migrate

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

db = SQLAlchemy(app)

migrate = Migrate(app, db)


# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'venues'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String, db.CheckConstraint(
        "state IN ('AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY')"))
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), unique=True)
    image_link = db.Column(db.String, unique=True)
    facebook_link = db.Column(db.String, unique=True)
    website = db.Column(db.String, unique=True)
    seeking_talent = db.Column(db.Boolean, server_default='false')
    seeking_description = db.Column(db.String, default='')
    genres = db.relationship('VenueGenre', backref='venue')
    shows = db.relationship('Show', back_populates='venue')

    def __repr__(self):
        return f'{{Venue id: {self.id}, name: {self.name}}}'

    @hybrid_property
    def past_shows(self):
        past_shows = []
        for show in self.shows:
            if show.start_time < datetime.now():
                past_shows.append(show)
        return past_shows

    @hybrid_property
    def upcoming_shows(self):
        upcoming_shows = []
        for show in self.shows:
            if show.start_time > datetime.now():
                upcoming_shows.append(show)
        return upcoming_shows

    @hybrid_property
    def num_upcoming_shows(self):
        count = 0
        for show in self.shows:
            if show.start_time > datetime.now():
                count += 1
        return count

    @hybrid_property
    def num_past_shows(self):
        count = 0
        for show in self.shows:
            if show.start_time < datetime.now():
                count += 1
        return count


class VenueGenre(db.Model):
    __tablename__ = 'venue_genres'
    name = db.Column(db.String, db.CheckConstraint(
        "name IN ('Alternative', 'Blues', 'Classical', 'Country', 'Electronic', 'Folk', 'Funk', 'Hip-Hop', 'Heavy Metal', 'Instrumental', 'Jazz', 'Musical Theatre', 'Pop', 'Punk', 'R&B', 'Reggae', 'Rock n Roll', 'Soul', 'Swing', 'Other')"),
                     primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), primary_key=True)

    def __repr__(self):
        return f'{{VenueGenre name: {self.name}}}'


class Artist(db.Model):
    __tablename__ = 'artists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(2), db.CheckConstraint(
        "state IN ('AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY')"))
    phone = db.Column(db.String(120), nullable=False, unique=True)
    image_link = db.Column(db.String, unique=True)
    facebook_link = db.Column(db.String, unique=True)
    website = db.Column(db.String, unique=True)
    seeking_venue = db.Column(db.Boolean, server_default='false')
    seeking_description = db.Column(db.String, default='')
    genres = db.relationship('ArtistGenre', backref='artist')
    shows = db.relationship('Show', back_populates='artist')

    def __repr__(self):
        return f'{{Artist id: {self.id}, name: {self.name}}}'

    @hybrid_property
    def past_shows(self):
        past_shows = []
        for show in self.shows:
            if show.start_time < datetime.now():
                past_shows.append(show)
        return past_shows

    @hybrid_property
    def upcoming_shows(self):
        upcoming_shows = []
        for show in self.shows:
            if show.start_time > datetime.now():
                upcoming_shows.append(show)
        return upcoming_shows

    @hybrid_property
    def num_upcoming_shows(self):
        count = 0
        for show in self.shows:
            if show.start_time > datetime.now():
                count += 1
        return count

    @hybrid_property
    def num_past_shows(self):
        count = 0
        for show in self.shows:
            if show.start_time < datetime.now():
                count += 1
        return count


class ArtistGenre(db.Model):
    __tablename__ = 'artist_genres'
    name = db.Column(db.String, db.CheckConstraint(
        "name IN ('Alternative', 'Blues', 'Classical', 'Country', 'Electronic', 'Folk', 'Funk', 'Hip-Hop', 'Heavy Metal', 'Instrumental', 'Jazz', 'Musical Theatre', 'Pop', 'Punk', 'R&B', 'Reggae', 'Rock n Roll', 'Soul', 'Swing', 'Other')"),
                     primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), primary_key=True)


class Show(db.Model):
    __tablename__ = 'shows'
    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)
    start_time = db.Column(db.DateTime(), nullable=False, default=datetime.now().isoformat())
    venue = db.relationship("Venue", back_populates="shows")
    artist = db.relationship("Artist", back_populates="shows")

    def __repr__(self):
        return f'{{Show id: {self.id}, start_time: {self.start_time}}}'


# ----------------------------------------------------------------------------#
# Create Database
# ----------------------------------------------------------------------------#

db.create_all()


# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#


# def format_datetime(value, format='medium'):
#     # date = value.isoformat()
#     date = dateutil.parser.parse(value)
#     if format == 'full':
#         format = "EEEE MMMM, d, y 'at' h:mma"
#     elif format == 'medium':
#         format = "EE MM, dd, y h:mma"
#     return babel.dates.format_datetime(date, locale='en')
#
# app.jinja_env.filters['datetime'] = format_datetime


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    areas = db.session.query(Venue.city, Venue.state).distinct().order_by(Venue.state).all()
    venues_per_area = [
        {
            'city': city,
            'state': state,
            'venues': db.session.query(Venue.id, Venue.name).filter(Venue.city == city, Venue.state == state).order_by(Venue.id).all()
         }
        for city, state in areas
    ]

    data = venues_per_area
    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    search_term = request.form.get('search_term')

    venues = db.session.query(Venue.id, Venue.name). \
        filter(Venue.name.ilike(f"%{search_term}%")). \
        order_by(Venue.id).all()

    response = {
        "count": len(venues),
        "data": venues
    }
    return render_template('pages/search_venues.html', results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    venue = Venue.query.get(venue_id)

    genre_names = []
    for genre in venue.genres:
        genre_names.append(genre.name)

    past_shows = [{
        'artist_id': show.artist.id,
        'artist_name': show.artist.name,
        'artist_image_link': show.artist.image_link,
        'start_time': show.start_time
    } for show in venue.past_shows]

    upcoming_shows = [{
        'artist_id': show.artist.id,
        'artist_name': show.artist.name,
        'artist_image_link': show.artist.image_link,
        'start_time': show.start_time
    } for show in venue.upcoming_shows]

    data = {
        "id": venue.id,
        "name": venue.name,
        "genres": genre_names,
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": venue.num_past_shows,
        "upcoming_shows_count": venue.num_upcoming_shows,
    }
    return render_template('pages/show_venue.html', venue=data, datetime=datetime)


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    name = request.form.get('name')
    city = request.form.get('city')
    state = request.form.get('state')
    address = request.form.get('address').strip()
    phone = request.form.get('phone').strip()
    genres = request.form.getlist('genres')
    seeking_description = request.form.get('seeking_description').strip()
    seeking_talent = True if seeking_description != '' else False
    image_link = request.form.get('image_link').strip()
    facebook_link = request.form.get('facebook_link').strip()
    try:
        venue = Venue(name=name, city=city, state=state, address=address, phone=phone, seeking_talent=seeking_talent,
                      seeking_description=seeking_description, image_link=image_link, facebook_link=facebook_link)
        for genre in genres:
            g = VenueGenre(name=genre)
            venue.genres.append(g)
        db.session.add(venue)
        db.session.commit()
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except:
        db.session.rollback()
        print(exc_info())
        flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.', 'error')
    finally:
        db.session.close()
        return render_template('pages/home.html')


# @app.route('/venues/<venue_id>', methods=['DELETE'])
# def delete_venue(venue_id):
#     # TODO: Complete this endpoint for taking a venue_id, and using
#     # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
#
#     # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
#     # clicking that button delete it from the db then redirect the user to the homepage
#     return None


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    artists = db.session.query(Artist.id, Artist.name)
    return render_template('pages/artists.html', artists=artists)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    search_term = request.form.get('search_term')
    artists = db.session.query(Artist.id, Artist.name). \
        filter(Artist.name.ilike(f"%{search_term}%")). \
        order_by(Artist.id).all()

    response = {
        "count": len(artists),
        "data": artists
    }
    return render_template('pages/search_artists.html', results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    artist = Artist.query.get(artist_id)

    genre_names = []
    for genre in artist.genres:
        genre_names.append(genre.name)

    past_shows = [{
        'venue_id': show.venue.id,
        'venue_name': show.venue.name,
        'venue_image_link': show.venue.image_link,
        'start_time': show.start_time
    } for show in artist.past_shows]

    upcoming_shows = [{
        'venue_id': show.venue.id,
        'venue_name': show.venue.name,
        'venue_image_link': show.venue.image_link,
        'start_time': show.start_time
    } for show in artist.upcoming_shows]

    data = {
        "id": artist.id,
        "name": artist.name,
        "genres": genre_names,
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website": artist.website,
        "facebook_link": artist.facebook_link,
        "seeking_venue": artist.seeking_venue,
        "seeking_description": artist.seeking_description,
        "image_link": artist.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": artist.num_past_shows,
        "upcoming_shows_count": artist.num_upcoming_shows,
    }
    return render_template('pages/show_artist.html', artist=data)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = {
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


# @app.route('/artists/<int:artist_id>/edit', methods=['POST'])
# def edit_artist_submission(artist_id):
#     # TODO: take values from the form submitted, and update existing
#     # artist record with ID <artist_id> using the new attributes
#
#     return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = {
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


# @app.route('/venues/<int:venue_id>/edit', methods=['POST'])
# def edit_venue_submission(venue_id):
#     # TODO: take values from the form submitted, and update existing
#     # venue record with ID <venue_id> using the new attributes
#     return redirect(url_for('show_venue', venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    name = request.form.get('name')
    city = request.form.get('city')
    state = request.form.get('state')
    phone = request.form.get('phone').strip()
    genres = request.form.getlist('genres')
    seeking_description = request.form.get('seeking_description').strip()
    seeking_venue = True if seeking_description != '' else False
    image_link = request.form.get('image_link').strip()
    facebook_link = request.form.get('facebook_link')
    try:
        artist = Artist(name=name, city=city, state=state, phone=phone, seeking_venue=seeking_venue,
                        seeking_description=seeking_description, image_link=image_link, facebook_link=facebook_link)
        for genre in genres:
            g = ArtistGenre(name=genre)
            artist.genres.append(g)
        db.session.add(artist)
        db.session.commit()
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except:
        db.session.rollback()
        print(exc_info())
        flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.', 'error')
    finally:
        db.session.close()
        return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    data = [{
        "venue_id": 1,
        "venue_name": "The Musical Hop",
        "artist_id": 4,
        "artist_name": "Guns N Petals",
        "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
        "start_time": "2019-05-21T21:30:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 5,
        "artist_name": "Matt Quevedo",
        "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
        "start_time": "2019-06-15T23:00:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 6,
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "start_time": "2035-04-01T20:00:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 6,
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "start_time": "2035-04-08T20:00:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 6,
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "start_time": "2035-04-15T20:00:00.000Z"
    }]
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


# @app.route('/shows/create', methods=['POST'])
# def create_show_submission():
#     # called to create new shows in the db, upon submitting new show listing form
#     # TODO: insert form data as a new Show record in the db, instead
#
#     # on successful db insert, flash success
#     flash('Show was successfully listed!')
#     # TODO: on unsuccessful db insert, flash an error instead.
#     # e.g., flash('An error occurred. Show could not be listed.')
#     # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
#     return render_template('pages/home.html')


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

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
