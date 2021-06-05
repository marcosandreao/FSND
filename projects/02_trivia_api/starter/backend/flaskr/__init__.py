import json

from flask import Flask
from flask_cors import CORS

from flaskr.models import setup_db, Question, Category
from . import config

QUESTIONS_PER_PAGE = 10


# https://pythonise.com/series/learning-flask/application-factory-pattern-%7C-learning-flask-ep.-30
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    if test_config is None:
        app.config.from_object(config)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    setup_db(app)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTION')
        return response

    def error_json(error, status_code):
        response = error.get_response()
        response.data = json.dumps({
            "success": False,
            "error": status_code,
            "message": error.description,
        })
        response.content_type = "application/json"
        return response, 422

    @app.errorhandler(404)
    def not_found_error(error):
        return error_json(error, 404)

    @app.errorhandler(500)
    def server_error(error):
        return error_json(error, 500)

    from . import api
    app.register_blueprint(api.api)

    return app
