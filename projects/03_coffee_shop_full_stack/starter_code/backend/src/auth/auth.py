import json
import os
from functools import wraps
from urllib.request import urlopen

import requests
from flask import request
from jose import jwt

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", 'maao.us.auth0.com')
API_AUDIENCE = os.getenv("AUTH0_API_AUDIENCE", 'dev')
CLIENT_ID = os.getenv("AUTH0_CLIENT_ID", "HGeauqJ232uOWakMtQ2xV8RdNynHxBps")
ALGORITHMS = ['RS256']
# Management API Access Tokens
# Testing: You can get a token manually using the Auth0 Dashboard for testing purposes.
API_ACCESS_TOKEN = os.getenv("API_ACCESS_TOKEN", "")
API_HOST = 'https://maao.us.auth0.com/api/v2'
API_HEADER_AUTH = {'Authorization': 'Bearer {}'.format(API_ACCESS_TOKEN)}

ROLE_BARISTA_ID = 'rol_J24FmR9Rx8P1K18p'
ROLE_MANAGER_ID = 'rol_JWbghF0gMj7igznN'
ROLE_BARISTA = 'BARISTA'
ROLE_MANAGER = 'MANAGER'

ROLES = {ROLE_BARISTA: ROLE_BARISTA_ID, ROLE_MANAGER: ROLE_MANAGER_ID}

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header

'''
@TODO implement get_token_auth_header() method
    it should attempt to get the header from the request
        it should raise an AuthError if no header is present
    it should attempt to split bearer and the token
        it should raise an AuthError if the header is malformed
    return the token part of the header
'''


def get_token_auth_header():
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError({"code": "authorization_header_missing",
                         "description":
                             "Authorization header is expected"}, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError({"code": "invalid_header",
                         "description":
                             "Authorization header must start with"
                             " Bearer"}, 401)
    if len(parts) == 1:
        raise AuthError({"code": "invalid_header",
                         "description": "Token not found"}, 401)
    if len(parts) > 2:
        raise AuthError({"code": "invalid_header",
                         "description":
                             "Authorization header must be"
                             " Bearer token"}, 401)

    token = parts[1]
    return token


'''
@TODO implement check_permissions(permission, payload) method
    @INPUTS
        permission: string permission (i.e. 'post:drink')
        payload: decoded jwt payload

    it should raise an AuthError if permissions are not included in the payload
        !!NOTE check your RBAC settings in Auth0
    it should raise an AuthError if the requested permission string is not in the payload permissions array
    return true otherwise
'''


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
        }, 400)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 403)
    return True


'''
@TODO implement verify_decode_jwt(token) method
    @INPUTS
        token: a json web token (string)

    it should be an Auth0 token with key id (kid)
    it should verify the token using Auth0 /.well-known/jwks.json
    it should decode the payload from the token
    it should validate the claims
    return the decoded payload

    !!NOTE urlopen has a common certificate error described here: https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
'''


def verify_decode_jwt(token):
    jsonurl = urlopen('https://{}/.well-known/jwks.json'.format(AUTH0_DOMAIN))
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
            break

    if not rsa_key:
        raise AuthError({"code": "invalid_header",
                         "description": "Unable to find appropriate key"}, 401)
    # public_key = jwk.construct(rsa_key)
    issuer = 'https://{}/'.format(AUTH0_DOMAIN)
    try:
        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=ALGORITHMS,
            audience=API_AUDIENCE,
            issuer=issuer
        )
    except jwt.ExpiredSignatureError:
        raise AuthError({"code": "token_expired",
                         "description": "token is expired"}, 401)
    except jwt.JWTClaimsError:
        raise AuthError({"code": "invalid_claims",
                         "description":
                             "incorrect claims,"
                             "please check the audience and issuer"}, 401)
    except Exception:
        raise AuthError({"code": "invalid_header",
                         "description":
                             "Unable to parse authentication"
                             " token."}, 401)
    return payload


'''
@TODO implement @requires_auth(permission) decorator method
    @INPUTS
        permission: string permission (i.e. 'post:drink')

    it should use the get_token_auth_header method to get the token
    it should use the verify_decode_jwt method to decode the jwt
    it should use the check_permissions method validate claims and check the requested permission
    return the decorator which passes the decoded payload to the decorated method
'''


def requires_auth(permission='', inject_payload=False):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs) if inject_payload else f(*args, **kwargs)

        return wrapper

    return requires_auth_decorator


def create_user_auth0(name, email, password, role):
    """
    create a user
    /api/v2/users
    associate users to a role
    /api/v2/roles/{id}/users
    """
    payload = {
        "connection": "Username-Password-Authentication",
        "email": email,
        "password": password,
        "user_metadata": {
            "name": name
        },
        "email_verified": False,
        "verify_email": False,
        "app_metadata": {}
    }
    result = requests.post(API_HOST + str('/users'), json=payload, headers=API_HEADER_AUTH).json()

    if 'error' in result:
        return result
    user_id = result['user_id']

    payload = {
        "users": [user_id]
    }
    result = requests.post(API_HOST + str('/roles/{}/users'.format(ROLES[role.upper()])), json=payload,
                           headers=API_HEADER_AUTH).json()
    if 'error' in result:
        return result
    return None


def list_users_by_role(role):
    result = requests.get(API_HOST + str('/roles/{}/users'.format(ROLES[role.upper()])),
                          headers=API_HEADER_AUTH).json()
    if 'error' in result:
        return []
    return result
