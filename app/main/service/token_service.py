import datetime

from app.main import db
from ..model.token import Token
from .user_service import save_changes


def get_all_tokens(user_id):
    return Token.query.filter_by(user_id=user_id).all()


def create_token(user_id, jti):
    token = Token(user_id=user_id, jti=jti)
    save_changes(token)


def blacklist_token(jti):
    token = Token.query.filter_by(jti=jti).first()
    token.is_active = False
    token.blacklisted_on = datetime.datetime.now()
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback
        response_object = {
            'status': 'fail',
            'message': e
        }
        return response_object, 400
