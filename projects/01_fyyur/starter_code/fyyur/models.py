from datetime import datetime

from flask_sqlalchemy import BaseQuery
from sqlalchemy import desc

from fyyur import db


class ShowQuery(BaseQuery):
    def artist_upcoming_shows(self, id_model):
        return self.filter(Show.artist_id == id_model, Show.start_time >= datetime.now())

    def venue_upcoming_shows(self, id_model):
        return self.filter(Show.venue_id == id_model, Show.start_time >= datetime.now())

    def search(self, search_term):
        return self.join(Venue).join(Artist) \
            .filter((Venue.name.ilike('%{0}%'.format(search_term))) | (Artist.name.ilike('%{0}%'.format(search_term)))) \
            .order_by(desc(Show.start_time))

    def by_artist_and_venue(self, venue_id, artist_id):
        return self.filter(Show.venue_id == venue_id, Show.artist_id == artist_id)

    def by_date(self, date, artist_id):
        date_start = date.replace(hour=0, minute=0, second=0, microsecond=0)
        date_end = date.replace(hour=23, minute=59, second=59, microsecond=0)
        return self.filter(Show.start_time.between(date_start, date_end), Show.artist_id == artist_id)


class VenueQuery(BaseQuery):
    def group_state_and_city(self):
        return self.with_entities(Venue.state, Venue.city) \
            .group_by(Venue.state, Venue.city).order_by(Venue.state, Venue.city)

    def by_state_and_city(self, state, city):
        return self.filter(Venue.state == state, Venue.city == city).order_by(Venue.name)

    def search(self, term):
        return self.filter(Venue.name.ilike('%{0}%'.format(term)))

    def top_10(self):
        return self.with_entities(Venue.id, Venue.name, Venue.views).filter(Venue.views > 0).order_by(desc(Venue.views)).limit(10)


class ArtistQuery(BaseQuery):
    def search(self, term):
        return self.filter(Artist.name.ilike('%{0}%'.format(term)))

    def top_10(self):
        return self.with_entities(Artist.id, Artist.name, Artist.views)\
            .filter(Artist.views > 0).order_by(desc(Artist.views))\
            .limit(10)


class Show(db.Model):
    """relationship N-M"""
    __tablename__ = 'Shows'
    query_class = ShowQuery

    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    venue = db.relationship('Venue', lazy='select', backref=db.backref("shows"))
    artist = db.relationship('Artist', lazy='select', backref=db.backref("shows"))


class Venue(db.Model):
    __tablename__ = 'Venue'
    query_class = VenueQuery

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(250))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    views = db.Column(db.Integer, default=0)

    def fill_from_dict(self, data):
        self.name = data['name']
        self.city = data['city']
        self.state = data['state']
        self.address = data['address']
        self.phone = data['phone']
        self.genres = ','.join(data['genres'])
        self.image_link = data['image_link']
        self.facebook_link = data['facebook_link']
        self.website_link = data['website_link']
        self.seeking_talent = data['seeking_talent']
        self.seeking_description = data['seeking_description']
        return self

    @staticmethod
    def from_dict(data):
        venue = Venue()
        venue.fill_from_dict(data)
        return venue


class Artist(db.Model):
    __tablename__ = 'Artist'
    query_class = ArtistQuery

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(250))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    views = db.Column(db.Integer, default=0)

    def fill_from_dict(self, data):
        self.name = data['name']
        self.city = data['city']
        self.state = data['state']
        self.phone = data['phone']
        self.genres = ','.join(data['genres'])
        self.image_link = data['image_link']
        self.facebook_link = data['facebook_link']
        self.website_link = data['website_link']
        self.seeking_venue = data['seeking_venue']
        self.seeking_description = data['seeking_description']
        return self

    @staticmethod
    def from_dict(data):
        artist = Artist()
        artist.fill_from_dict(data)
        return artist
