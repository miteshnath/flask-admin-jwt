from flask import request
from flask_restx import Resource

from ..service.auth_service import Auth
from ..util.decorator import admin_token_required
from ..service.user_service import save_new_user, get_a_user
from ..util.dto import AuthDto

api = AuthDto.api
user_auth = AuthDto.user_auth
user_token = AuthDto.user_token


@api.route('/register')
class UserRegister(Resource):
    """
        User Register Resource
    """
    @api.doc('user register')
    @api.expect(user_auth, validate=True)
    def post(self):
        # get the post data
        data = request.json
        return save_new_user(data=data)
    
    
@api.route('/login')
class UserLogin(Resource):
    """
        User Login Resource
    """
    @api.doc('user login')
    @api.expect(user_auth, validate=True)
    def post(self):
        # get the post data
        post_data = request.json
        return Auth.login_user(data=post_data)


@api.route('/logout')
class LogoutAPI(Resource):
    """
    Logout Resource
    """
    @api.doc('logout a user')
    @api.doc(params={'Authorization': {'in': 'header', 'description': 'An authorization token'}})
    def post(self):
        """
        logout user
        """
        # get auth token
        auth_header = request.headers.get('Authorization')
        return Auth.logout_user(data=auth_header)


@api.route('/force-logout/<id>')
class ForceLogoutAPI(Resource):
    """
    Force Logout Resource
    """
    @api.doc('force logout a user')
    @api.doc(params={'Authorization': {'in': 'header', 'description': 'An authorization token'}})
    @api.response(404, 'User not found.')
    @admin_token_required
    def post(self, id):
        """
        force logout a user and blacklist all the tokens
        """
        user = user = get_a_user(id)
        if not user:
            api.abort(404)
        return Auth.force_logout_user(user)



@api.route('/expire-token')
class ExpireTokenAPI(Resource):
    """
    Expire Token Resource
    """
    @api.doc('expire a user token')
    @api.doc(params={'Authorization': {'in': 'header', 'description': 'An authorization token'}})
    @api.expect(user_token, validate=True)
    @admin_token_required
    def post(self):
        """
        expire a token passed in post body, admin only authorized
        """
        token = request.json['token']
        return Auth.expire_token(token)
