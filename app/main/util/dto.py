from flask_restx import Namespace, fields


class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password')
    })
    user_token = api.model('token', {
        'token': fields.String(required=True, description='Token to be expired.')
    })


class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'email': fields.String(required=True, description='email address'),
        'is_admin': fields.Boolean(required=False, description='is_admin')
    })
    post_user = api.model('user', {
        'email': fields.String(required=True, description='email address'),
        'password': fields.String(required=True, description='password'),
        'is_admin': fields.Boolean(required=True, description='is_admin')
    })
