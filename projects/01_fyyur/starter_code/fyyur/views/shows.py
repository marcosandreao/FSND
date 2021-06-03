from flask import render_template, flash, request, url_for
from sqlalchemy import desc
from werkzeug.utils import redirect

from fyyur import app, db
from fyyur.forms import *

#  Shows
#  ----------------------------------------------------------------
from fyyur.models import Venue, Artist, Show
from fyyur.repositories import ShowRepository

service = ShowRepository()


@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.

    values = Show.query.order_by(desc(Show.start_time))
    data = [{'venue_id': v.venue_id,
             'artist_id': v.artist_id,
             'start_time': v.start_time,
             'artist_name': v.artist.name,
             'venue_name': v.venue.name,
             'artist_image_link': v.artist.image_link} for v in values]
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/search', methods=['POST'])
def search_shows():
    search_term = request.form.get('search_term', '')

    values = Show.query.search(search_term)

    data = [{'venue_id': v.venue_id,
             'artist_id': v.artist_id,
             'start_time': v.start_time,
             'venue_name': v.venue.name,
             'artist_name': v.artist.name} for v in values]

    response = {
        "count": len(data),
        "data": data
    }
    return render_template('pages/search_shows.html', results=response,
                           search_term=search_term)


@app.route('/shows/create', methods=['GET', 'POST'])
def create_shows():
    form = ShowForm(coerce=str)
    if request.method == 'POST' and form.validate_on_submit():
        venue_id = form.data['venue_id']
        artist_id = form.data['artist_id']
        has_show = Show.query.by_artist_and_venue(venue_id, artist_id).count() > 0
        if has_show:
            flash('There is a similar Show.')
        elif Show.query.by_date(form.start_time.data, artist_id).count() > 0:
            flash('Artist: schedule conflict.')
        else:
            model = Show()
            model.venue_id = form.data['venue_id']
            model.artist_id = form.data['artist_id']
            model.start_time = form.data['start_time']
            service.persiste(model)
            flash('Show was successfully listed!')
            return redirect(url_for('shows'))

    form.venue_id.choices = [(v.id, v.name) for v in
                             Venue.query.with_entities(Venue.id, Venue.name).order_by(Venue.name)]
    form.artist_id.choices = [(v.id, v.name) for v in
                              Artist.query.with_entities(Artist.id, Artist.name).order_by(Artist.name)]
    return render_template('forms/new_show.html', form=form)
