from flask import Blueprint, request
from flask import current_app as app
from flask_restful import Api, Resource, fields, marshal_with, reqparse, abort

from flaskr import Category, Question

api = Blueprint("api", __name__, url_prefix='/api')
rest_api = Api(api)

parser = reqparse.RequestParser()
parser.add_argument('page', type=int, location='args', default=1)

# https://flask-restful.readthedocs.io/en/latest/
cat_field = {
    'type': fields.String,
    'id': fields.Integer
}

id_field = {
    'id': fields.Integer
}

q_fields = {
    'id': fields.Integer,
    'question': fields.String,
    'difficulty': fields.Integer,
    'answer': fields.String,
    'category': fields.String,
}
p_fields = {
    'page': fields.Integer,
    'limit': fields.Integer,
    'total_pages': fields.Integer,
    'has_next': fields.Boolean,
    'has_prev': fields.Boolean,
    'total': fields.Integer,
    'data': fields.Nested(q_fields),
}


def marshal_list_all(nested):
    return {
        'data': fields.Nested(nested),
        'total': fields.Integer,
    }


class CategoryListResource(Resource):

    @marshal_with(marshal_list_all(cat_field))
    def get(self):
        app.logger.debug('list categories')
        data = Category.query.ordered().all()
        return {
            'total': len(data),
            'data': data
        }


class QuestionListResource(Resource):

    @marshal_with(p_fields)
    def get(self):
        app.logger.debug('list questions')
        search_term = request.form.get('search_term', '')
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))

        query = Question.query.order_by(Question.question)
        if not search_term:
            query = query.search(search_term)

        pagination = query.paginate(page, per_page=limit)
        return {
            'data': pagination.items,
            'total': pagination.total,
            'page': pagination.page,
            'total_pages': pagination.pages,
            'has_prev': pagination.has_prev,
            'has_next': pagination.has_next,
        }

    @marshal_with(id_field)
    def post(self):
        def cat_exist(_id):
            if not _id:
                raise ValueError("category cannot be converted")
            if not Category.query.get(int(_id)):
                raise ValueError("category cannot be found")
            return int(_id)

        q_parser = reqparse.RequestParser()
        q_parser.add_argument('difficulty', type=int, help='difficulty cannot be converted', location='json')
        q_parser.add_argument('answer', required=True, help="answer cannot be blank!", location='json')
        q_parser.add_argument('question', required=True, help="question cannot be blank!", location='json')
        q_parser.add_argument('category', type=cat_exist, location='json')
        args = q_parser.parse_args()

        model = Question(args['question'], args['answer'], args['category'], args['difficulty'])
        model.insert()
        return model, 201


class QuestionResource(Resource):

    def delete(self, question_id):
        model = Question.query.get(question_id)
        if not model:
            abort(404, message="Question {} doesn't exist".format(question_id))
        model.delete()
        return '', 204


class CategoryQuestionResource(Resource):

    @marshal_with(marshal_list_all(q_fields))
    def get(self, cat_id):
        questions = Question.query.by_category(cat_id).all()
        return {
            'data': questions,
            'total': len(questions)
        }


rest_api.add_resource(CategoryListResource, '/categories')
rest_api.add_resource(CategoryQuestionResource, '/categories/<int:cat_id>/questions')
rest_api.add_resource(QuestionListResource, '/questions')
rest_api.add_resource(QuestionResource, '/questions/<int:question_id>')

