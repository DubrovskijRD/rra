from flask import Flask, url_for, redirect
from flask_admin import helpers as admin_helpers

from flask_babel import Babel
from app.models.db import db
from app.security import security, user_datastore
from app.admin import admin
from app.views.admin import admin_views


class PrefixMiddleware(object):

    def __init__(self, app, prefix=''):
        self.app = app
        self.prefix = prefix

    def __call__(self, environ, start_response):

        if environ['PATH_INFO'].startswith(self.prefix):
            environ['PATH_INFO'] = environ['PATH_INFO'][len(self.prefix):]
            environ['SCRIPT_NAME'] = self.prefix
            return self.app(environ, start_response)
        else:
            start_response('404', [('Content-Type', 'text/plain')])
            return ["This url does not belong to the app.".encode()]


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix='/rra')
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

    @app.route('/')
    def bar():

        return redirect(url_for('admin.index'))

    return app
