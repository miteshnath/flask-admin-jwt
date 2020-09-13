from .. import db


class BaseModel(db.Model):
    """
    Base data model
    """
    __abstract__ = True
    
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
