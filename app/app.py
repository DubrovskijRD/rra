from flask import Flask, url_for
from flask_admin import helpers as admin_helpers

from flask_babel import Babel
from app.models.db import db
from app.security import security, user_datastore
from app.admin import admin
from app.views.admin import admin_views


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    babel = Babel(app, default_locale="ru")
    admin.init_app(app)
    security._state = security.init_app(app, datastore=user_datastore)

    @security.context_processor
    def security_context_processor():
        return dict(
            admin_base_template=admin.base_template,
            admin_view=admin.index_view,
            h=admin_helpers,
            get_url=url_for
        )
    for view in admin_views():
        admin.add_view(view)

    return app
