import logging
from logging import Formatter, FileHandler

from flask import Flask
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from . import config

app = Flask(__name__)
app.config.from_object(config)

db = SQLAlchemy()
db.init_app(app)

moment = Moment()
moment.init_app(app)

migrate = Migrate(app, db, directory='fyyur/migrations')
migrate.init_app(app)

from . import forms, filters, models, views

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')
