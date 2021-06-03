from flask import render_template, request

from fyyur import app
from fyyur.models import Artist, Venue
from fyyur.repositories import BaseRepository


@app.route('/')
def index():
    venues = Venue.query.top_10().all()
    artists = Artist.query.top_10().all()

    return render_template('pages/home.html', venues=venues, artists=artists)


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


@app.before_request
def before_request():
    def get_id():
        return request.view_args[request.url_rule.arguments.copy().pop()]

    def set_view(model):
        repo = BaseRepository()
        model.views = 1 if model.views is None else model.views + 1
        repo.persiste(model)

    if request.url_rule.endpoint == 'show_artist':
        set_view(Artist.query.get(get_id()))
    elif request.url_rule.endpoint == 'show_venue':
        set_view(Venue.query.get(get_id()))
