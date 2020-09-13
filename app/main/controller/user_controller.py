from flask import request
from flask_restx import Resource

from ..util.decorator import admin_token_required
from ..util.dto import UserDto
from ..service.user_service import save_new_user, get_all_users, get_a_user

api = UserDto.api
_user = UserDto.user
_post_user = UserDto.post_user


@api.route('/')
class UserList(Resource):
    @api.doc('list_of_registered_users')
    @api.doc(params={'Authorization': {'in': 'header', 'description': 'An authorization token'}})
    @api.marshal_list_with(_user, envelope='data')
    @admin_token_required
    def get(self):
        """List all registered users"""
        users = get_all_users()
        res = []
        for user in users:
            res.append(user._to_dict())
        return res, 200

    @api.expect(_post_user, validate=True)
    @api.doc(params={'Authorization': {'in': 'header', 'description': 'An authorization token'}})
    @api.response(201, 'User successfully created.')
    @api.doc('create a new user')
    @admin_token_required
    def post(self):
        """Creates a new User """
        data = request.json
        return save_new_user(data=data)


@api.route('/<id>')
@api.doc(params={'Authorization': {'in': 'header', 'description': 'An authorization token'}})
@api.param('id', 'User identifier')
@api.response(404, 'User not found.')
class User(Resource):
    @api.doc('get a user')
    @api.marshal_with(_user)
    @admin_token_required
    def get(self, id):
        """get a user given its identifier"""
        user = get_a_user(id)
        if not user:
            api.abort(404)
        else:
            return user, 200
