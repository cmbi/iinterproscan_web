import os
import logging

from celery import Celery
from flask import Flask


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

    return app


def create_celery_app(app):
    app = app or create_app()

    celery = Celery(__name__,
                    backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    import interproscan_web.tasks

    return celery
