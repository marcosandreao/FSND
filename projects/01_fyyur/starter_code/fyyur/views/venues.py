from flask import render_template, request, flash, redirect, url_for, jsonify

from fyyur import app
from fyyur.forms import *
from fyyur.models import Venue, Show
from fyyur.repositories import VenueRepository

service = VenueRepository()


@app.route('/venues')
def venues():
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    grouped = Venue.query.group_state_and_city().all()

    data = []
    for group in grouped:
        # TODO: append  num_upcoming_shows": 0,
        list_venue = Venue.query.with_entities(Venue.id, Venue.name).by_state_and_city(group.state, group.city) \
            .all()
        data.append({
            'city': group.city,
            'state': group.state,
            'venues': list_venue
        })
    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    search_term = request.form.get('search_term', '')
    data = Venue.query.search(search_term).with_entities(Venue.id, Venue.name).order_by(Venue.id)

    result = []
    for venue in data:
        result.append({
            'id': venue.id,
            'name': venue.name,
            'num_upcoming_shows': Show.query.venue_upcoming_shows(venue.id).count()
        })

    response = {
        "count": len(result),
        "data": result
    }
    return render_template('pages/search_venues.html', results=response,
                           search_term=search_term)


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    data = Venue.query.get(venue_id)
    now = datetime.now()
    data.past_shows = []
    data.upcoming_shows = []
    for show in data.shows:
        value = {
            'artist_id': show.artist.id,
            'artist_name': show.artist.name,
            'artist_image_link': show.artist.image_link,
            'start_time': show.start_time,
        }
        if show.start_time < now:
            data.past_shows.append(value)
        else:
            data.upcoming_shows.append(value)
    data.past_shows_count = len(data.past_shows)
    data.upcoming_shows_count = len(data.upcoming_shows)
    return render_template('pages/show_venue.html', venue=data)


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET', 'POST'])
def create_venue_form():
    form = VenueForm()
    if request.method == 'GET':
        return render_template('forms/new_venue.html', form=form)

    if form.validate_on_submit():
        service.persiste(Venue.from_dict(form.data))
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
        return redirect(url_for('index'))

    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    if service.delete_by_id(venue_id):
        return jsonify(), 200

    return jsonify({'error': 'Error: there is a show.'}), 400


@app.route('/venues/<int:venue_id>/edit', methods=['GET', 'POST'])
def edit_venue(venue_id):
    model = Venue.query.get(venue_id)
    if request.method == 'GET':
        model.genres = model.genres.split(',')
        form = VenueForm(obj=model)
        return render_template('forms/edit_venue.html', form=form, venue=model)

    form = VenueForm()
    if form.validate_on_submit():
        model.fill_from_dict(form.data)
        service.persiste(model)

        flash('Venue ' + form.name.data + ' was successfully listed!')
        return redirect(url_for('show_venue', venue_id=venue_id))

    return render_template('forms/edit_venue.html', form=form, venue=model)
