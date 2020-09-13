from .. import db
from .base import BaseModel


class Token(BaseModel):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    jti = db.Column(db.String(100), unique=True, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    blacklisted_on = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return '<Token: {}'.format(self.jti)

    @staticmethod
    def check_blacklist(jti):
        # check whether auth token has been blacklisted
        res = Token.query.filter_by(jti=str(jti)).first()
        if res.is_active:
            return False
        else:
            return True
