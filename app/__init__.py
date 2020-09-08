import os
from datetime import timedelta

import redis
from flask import Flask, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.menu import MenuLink
from flask_login import LoginManager
from flask_jwt_extended import JWTManager

from config import config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

ACCESS_EXPIRES = timedelta(seconds=300)
REFRESH_EXPIRES = timedelta(minutes=30)

jti_store = redis.StrictRedis(host=os.environ.get('REDIS_HOST'),
                              port=os.environ.get('REDIS_PORT'),
                              db=os.environ.get('REDIS_DB'),
                              password=os.environ.get('REDIS_PWD'),
                              decode_responses=True)


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('CONFIG', 'development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    from .models import User
    migrate.init_app(app, db)

    from app.api.v1 import auth_bp
    app.register_blueprint(auth_bp)

    login_manager.init_app(app)
    _jwt = JWTManager(app)

    @login_manager.user_loader
    def load_user(user_id):
        print("user_id", user_id)
        """Check if user is logged-in upon page load."""
        if user_id is not None:
            return User.query.get(user_id)
        return None

    @login_manager.unauthorized_handler
    def unauthorized():
        """Redirect unauthorized users to Login page."""
        flash('You must be logged in to view that page.')
        return redirect(url_for('auth_bp.login'))

    from app.api.v1.admin_view import UserAdminModelView, MyAdminIndexView
    app.config['FLASK_ADMIN_SWATCH'] = os.environ.get('FLASK_ADMIN_SWATCH')
    admin = Admin(app, name='flask-jwt', index_view=MyAdminIndexView(), template_mode='bootstrap3')
    admin.add_view(UserAdminModelView(User, db.session, endpoint='user'))
    admin.add_link(MenuLink(name='Logout', category='', url="/logout"))
    return app
