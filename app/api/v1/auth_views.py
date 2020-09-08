from datetime import timedelta

import redis
from flask import Blueprint, url_for, flash, render_template, redirect
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import current_user, login_user, logout_user
from flask_jwt_extended import create_access_token, get_jti

from app import db, jti_store
from app.models import User
from app.forms import LoginForm, SignupForm

ACCESS_EXPIRES = timedelta(minutes=15)
REFRESH_EXPIRES = timedelta(days=30)

revoked_store = redis.StrictRedis(host='localhost', port=6379, db=0,
                                  decode_responses=True)

auth_bp = Blueprint('auth_bp', __name__)


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    User sign-up page.
    GET requests serve sign-up page.
    POST requests validate form & user creation.
    """
    form = SignupForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if not existing_user:
            user = User(
                username=form.username.data,
                password=generate_password_hash(form.password.data)
            )
            db.session.add(user)
            db.session.commit()  # Create new user
            return redirect(url_for('auth_bp.login'))

        flash('A user already exists with that email address.')
    return render_template(
        'signup.jinja2',
        title='Create an Account.',
        form=form,
        template='signup-page',
        body="Sign up for a user account."
    )


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Log-in page for registered users.
    GET requests serve Log-in page.
    POST requests validate and redirect user to dashboard.
    """
    # Bypass if user is logged in
    if current_user and current_user.is_authenticated and jti_store.get(current_user.id):
        return redirect(url_for('admin.index'))

    form = LoginForm()
    # Validate login attempt
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and check_password_hash(user.password, form.password.data):
            login_user(user)
            jwt = create_access_token(identity=user.username)
            jti = get_jti(jwt)
            jti_store.set(user.id, jti, ex=timedelta(minutes=5))
            next_page = request.args.get('next')
            return redirect(next_page or url_for('admin.index'))

        flash('Invalid username/password combination')

    return render_template(
        'login.jinja2',
        form=form,
        title='Log in.',
        template='login-page',
        body="Log in with your User account."
    )


@auth_bp.route('/logout')
def logout():
    jti_store.delete(current_user.id)
    logout_user()
    return redirect(url_for('auth_bp.login'))
