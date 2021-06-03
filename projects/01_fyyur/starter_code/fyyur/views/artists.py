from flask import render_template, request, flash, redirect, url_for

from fyyur import app, db
from fyyur.forms import *
from fyyur.models import Artist, Show
from fyyur.repositories import ArtistRepository

service = ArtistRepository()


@app.route('/artists')
def artists():
    data = Artist.query.with_entities(Artist.id, Artist.name).order_by(Artist.id)
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    search_term = request.form.get('search_term', '')
    data = Artist.query.search(search_term) \
        .with_entities(Artist.id, Artist.name).order_by(Artist.id)

    result = []
    for artist in data:
        result.append({
            'id': artist.id,
            'name': artist.name,
            'num_upcoming_shows': Show.query.artist_upcoming_shows(artist.id).count()
        })

    response = {
        "count": len(result),
        "data": result
    }
    return render_template('pages/search_artists.html', results=response, search_term=search_term)


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    data = Artist.query.get(artist_id)
    now = datetime.today().date()
    data.past_shows = []
    data.upcoming_shows = []
    for show in data.shows:
        value = {
            'venue_id': show.venue_id,
            'venue_name': show.venue.name,
            'venue_image_link': show.venue.image_link,
            'start_time': show.start_time,
        }
        if show.start_time.date() < now:
            data.past_shows.append(value)
        else:
            data.upcoming_shows.append(value)
    data.past_shows_count = len(data.past_shows)
    data.upcoming_shows_count = len(data.upcoming_shows)

    return render_template('pages/show_artist.html', artist=data)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET', 'POST'])
def edit_artist(artist_id):
    model = Artist.query.get(artist_id)

    if request.method == 'GET':
        model.genres = model.genres.split(',')
        form = ArtistForm(obj=model)
        return render_template('forms/edit_artist.html', form=form, artist=model)

    form = ArtistForm()
    if form.validate_on_submit():
        model.fill_from_dict(form.data)
        service.persiste(model)
        flash('Artist ' + form.name.data + ' was successfully listed!')
        return redirect(url_for('show_artist', artist_id=artist_id))

    return render_template('forms/edit_artist.html', form=form, artist=model)


#  Create Artist
#  ----------------------------------------------------------------
@app.route('/artists/create', methods=['GET', 'POST'])
def create_artist_form():
    form = ArtistForm()
    if request.method == 'GET':
        return render_template('forms/new_artist.html', form=form)

    if form.validate_on_submit():
        service.persiste(Artist.from_dict(form.data))
        flash('Artist ' + form.name.data + ' was successfully listed!')
        return redirect(url_for('index'))
    else:
        return render_template('forms/new_artist.html', form=form)
