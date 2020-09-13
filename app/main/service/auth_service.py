from app.main.model.user import User
from .token_service import blacklist_token, create_token, get_all_tokens
from ..util.exceptions import TokenException


class Auth:
    @staticmethod
    def login_user(data):
        try:
            # fetch the user data
            user = User.query.filter_by(email=data.get('email')).first()
            if user and user.check_password(data.get('password')):
                auth_token, jti = User.encode_auth_token(user.id)
                create_token(user.id, jti)
                if auth_token:
                    response_object = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'Authorization': auth_token.decode()
                    }
                    return response_object, 200
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'email or password does not match.'
                }
                return response_object, 401

        except Exception as e:
            print(e)
            response_object = {
                'status': 'fail',
                'message': 'Try again'
            }
            return response_object, 500

    @staticmethod
    def logout_user(data):
        if data:
            auth_token = data.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            try:
                resp = User.decode_auth_token(auth_token)
                blacklist_token(resp['jti'])
                response_object = {
                    'status': 'success',
                    'message': 'Successfully logged out.'
                }
                return response_object, 200
            except TokenException as e:
                response_object = {
                    'status': 'fail',
                    'message': str(e)
                }
                return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object, 403

    @staticmethod
    def force_logout_user(user):
        tokens = get_all_tokens(user.id)
        for _tok in tokens:
            blacklist_token(_tok.jti)

        response_object = {
            'status': 'success',
            'message': f'Successfully forced logged out user {user.email} from all devices.'
        }
        return response_object, 200

    @staticmethod
    def expire_token(token):
        try:
            _tok = User.decode_auth_token(token)
            blacklist_token(_tok['jti'])
            response_object = {
                'status': 'success',
                'message': f'Successfully expired token'
            }
            return response_object, 200
        except TokenException as e:
            response_object = {
                'status': 'fail',
                'message': str(e)
            }
            return response_object, 400

    @staticmethod
    def get_logged_in_user(new_request):
        # get the auth token
        auth_token = new_request.headers.get('Authorization').split(" ")[1]
        if auth_token:
            try:
                resp = User.decode_auth_token(auth_token)
                user = User.query.filter_by(id=resp['sub']).first()
                response_object = {
                    'status': 'success',
                    'data': {
                        'user_id': user.id,
                        'email': user.email,
                        'admin': user.is_admin
                    }
                }
                return response_object, 200
            except TokenException as e:
                response_object = {
                    'status': 'fail',
                    'message': str(e)
                }
                return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object, 401
