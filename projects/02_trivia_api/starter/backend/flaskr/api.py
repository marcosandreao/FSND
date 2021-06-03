from flask import Blueprint
from flask import current_app as app
from flask_restful import Api, Resource, fields, marshal_with

from flaskr import Category

api = Blueprint("api", __name__, url_prefix='/api')
rest_api = Api(api)


# https://flask-restful.readthedocs.io/en/latest/
def marshal_list_all(nested):
    return {
        'data': fields.Nested(nested),
        'total': fields.Integer,
    }


def marshal_pagination(nested):
    return marshal_list_all(nested).update({
        'page': fields.Integer,
        'limit': fields.Integer
    })


class CategoryList(Resource):
    cat_field = {
        'type': fields.String,
        'id': fields.Integer
    }

    @marshal_with(marshal_list_all(cat_field))
    def get(self):
        app.logger.debug('list categories')
        data = Category.query.order_by(Category.type).all()
        return {
            'total': len(data),
            'data': data
        }


rest_api.add_resource(CategoryList, '/categories')
