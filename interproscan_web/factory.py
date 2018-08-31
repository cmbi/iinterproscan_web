import os
import logging

from flask import Flask

from interproscan_web.controllers.interproscan import interproscan
from interproscan_web.controllers.job import job_manager


def create_app(settings=None):
    app = Flask(__name__)

    app.config.from_object('interproscan_web.default_settings')
    if settings:
        app.config.update(settings)

    # Set for large interpro files
    app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 200

     # Use ProxyFix to correct URL's when redirecting.
    from interproscan_web.middleware import ReverseProxied
    app.wsgi_app = ReverseProxied(app.wsgi_app)

    # Register blueprints
    from interproscan_web.frontend.api.endpoints import bp as api_bp
    app.register_blueprint(api_bp)

    interproscan.interproscan_path = app.config['INTERPROSCAN_PATH']

    job_manager.data_dir = app.config['DATADIR_PATH']

    return app
