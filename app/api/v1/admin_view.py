from datetime import datetime

from flask import redirect, url_for
from flask_login import current_user
from werkzeug.security import generate_password_hash
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView

from app import jti_store


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if current_user and current_user.is_authenticated:
            if not jti_store.get(current_user.id):
                return False
            return current_user.is_authenticated
        return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth_bp.login'))


class UserAdminModelView(ModelView):
    column_list = ('id', 'username', 'is_admin')

    def is_accessible(self):
        if current_user and current_user.is_authenticated:
            if not jti_store.get(current_user.id):
                return False
            return current_user.is_authenticated
        return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth_bp.login'))

    def on_model_change(self, form, model, is_created):
        model.password = generate_password_hash(model.password)

        if is_created:
            model.registered_on = datetime.now()

    def get_query(self, *args, **kwargs):
        if not current_user.is_authenticated:
            return None
        qs = super(UserAdminModelView, self).get_query(*args, **kwargs)
        qs = qs.filter_by(id=current_user.id)
        return qs
