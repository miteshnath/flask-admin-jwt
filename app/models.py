from flask_login import UserMixin
from app import db
    

class User(db.Model, UserMixin):
    """
    Model for the users table
    """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    
    def __str__(self):
        return f"{self.__class__.__name__}, {self.id}"

    def __repr__(self):
        return f"{self.__class__.__name__}, {self.id}"
                    
    def _to_dict(self): 
        as_json = {
            column: value for column, value in self.__dict__.items()
        }
        del as_json['password']
        return as_json
