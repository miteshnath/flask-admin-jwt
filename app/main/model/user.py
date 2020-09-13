import uuid
from datetime import date, datetime, timedelta
from .. import db, flask_bcrypt

from .token import Token
from ..util.exceptions import TokenException
from ..config import key
from .base import BaseModel
import jwt


class User(BaseModel):
    """
    Model for the users table
    """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    @staticmethod
    def encode_auth_token(user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=1, seconds=5),
                'iat': datetime.utcnow(),
                'sub': user_id,
                'jti': str(uuid.uuid4())
            }
            return jwt.encode(
                payload,
                key,
                algorithm='HS256'
            ), payload['jti']
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, key)
            is_blacklisted_token = Token.check_blacklist(payload['jti'])
            if is_blacklisted_token:
                raise TokenException('Token blacklisted. Please log in again.')
            else:
                return {"sub": payload['sub'], "jti": payload["jti"]}
        except jwt.ExpiredSignatureError:
            raise TokenException('Signature expired. Please log in again.')
        except jwt.InvalidTokenError:
            raise TokenException('Invalid token. Please log in again.')
    
    def _to_dict(self): 
        as_json = {}
        for column, value in self.__dict__.items():
            if column == '_sa_instance_state':
                continue
            elif isinstance(value, (datetime, date)):
                as_json[column] = value.isoformat()
            else:
                as_json[column] = value
        return as_json
    
    def __str__(self):
        return f"{self.__class__.__name__}, {self.id}"

    def __repr__(self):
        return "<User '{}'>".format(self.id)
