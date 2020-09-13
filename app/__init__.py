from flask import Blueprint
from flask_restx import Api
from .main.controller.auth_controller import api as auth_ns
from .main.controller.user_controller import api as user_ns

blueprint = Blueprint('api', __name__)

authorizations = {
    'basic': {
        'type': 'basic',
        'in': 'headers',
        'name': 'Authorization'
    }
}

api = Api(blueprint,
          title='Simple Flask JWT Auth With Admin',
          version='1.0',
          authorizations=authorizations,
          security='basic',
          description='flask JWT based auth system with admin as a web service'
          )

api.add_namespace(auth_ns, path='/auth')
api.add_namespace(user_ns, path='/user')
