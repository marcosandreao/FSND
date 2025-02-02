import json

from flask import Flask, request, jsonify
from flask_cors import CORS

from .auth.auth import AuthError, requires_auth, check_permissions, create_user_auth0, list_users_by_role
from .database.models import setup_db, Drink

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the database
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''


# db_drop_and_create_all()

class ApiError(Exception):
    def __init__(self, error, status_code=422, description=None):
        self.error = error
        self.description = description
        self.status_code = status_code


# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['GET'])
def get_drinks():
    result = Drink.query.order_by(Drink.title).all()
    return jsonify([drink.short() for drink in result])


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def drinks_detail():
    result = Drink.query.order_by(Drink.title).all()
    return jsonify([drink.long() for drink in result])


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink():
    body = request.json
    title = body['title']
    if Drink.query.filter(Drink.title == title).count() > 0:
        raise ApiError("drink_duplicated",
                       description="There is a drink title='{0}'".format(title), status_code=409)
    drink = Drink()
    drink.title = title
    drink.recipe = json.dumps(body['recipe'])
    try:
        drink.insert()
    except:
        raise ApiError("drink_invalid_data", description="error during insert", status_code=400)
    return jsonify([drink.long()])


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def patch_drink(drink_id):
    drink = Drink.query.get(drink_id)
    if not drink:
        raise ApiError("drink_not_found",
                       description="There is not a drink id='{0}'".format(drink_id), status_code=404)

    body = request.json
    if 'title' in body:
        title = body['title']
        if Drink.query.filter(Drink.title == title, Drink.id != drink_id).count() > 0:
            raise ApiError("drink_duplicated",
                           description="There is a drink title='{0}'".format(title), status_code=409)

        drink.title = title
    if 'recipe' in body:
        recipe = body['recipe']
        drink.recipe = json.dumps(recipe)
    try:
        drink.update()
    except:
        raise ApiError("drink_invalid_data", description="error during update", status_code=400)
    return jsonify([drink.long()])


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink_by_id(drink_id):
    drink = Drink.query.get(drink_id)
    if not drink:
        raise ApiError("drink_not_found",
                       description="There is not a drink id='{0}'".format(drink_id), status_code=404)
    try:
        drink.delete()
    except:
        raise ApiError("drink_invalid_data", description="error during delete", status_code=400)
    return jsonify({'deleted': drink_id})


'''
@TODO Create endpoints to manage users using the Auth0 API
Barista access is limited (can do nothing)
Manager access is limited (can manage baristas)
Administrator access is limited (can manage baristas, managers)
'''


@app.route('/users', methods=['POST'])
@requires_auth('post:users', True)
def create_user(payload):
    body = request.json
    role = body['role']

    permission = 'post:users:' + str(role).lower()
    check_permissions(permission, payload)

    error = create_user_auth0(body['name'], body['email'], body['password'], body['role'])
    if error:
        raise ApiError(error['errorCode'], description=error['message'])
    return ''


@app.route('/users', methods=['GET'])
@requires_auth('get:users', True)
def list_users(payload):
    role = request.args['role']

    permission = 'get:users:' + str(role).lower()
    check_permissions(permission, payload)

    return jsonify(list_users_by_role(role))


# Error Handling
'''
Example error handling for unprocessable entity
'''

'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''


@app.errorhandler(ApiError)
def handler_api_error(e):
    return jsonify({"error": e.error,
                    "message": e.description}), e.status_code


'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''


@app.errorhandler(404)
def handler_api_error(e):
    return jsonify({"error": "resource_not_found",
                    "message": "resource not found"}), 404


@app.errorhandler(500)
def handler_api_error(e):
    return jsonify({"error": "internal_server_error",
                    "message": "unexpected error"}), 422


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''


@app.errorhandler(AuthError)
def handler_api_error(e):
    return jsonify(e.error), e.status_code
