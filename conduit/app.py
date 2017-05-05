# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from flask import Flask, render_template
from conduit.extensions import bcrypt, cache, db, migrate, jwt

from conduit import commands, user, profile, articles
from conduit.assets import assets
from conduit.settings import ProdConfig
from conduit.exceptions import InvalidUsage


def create_app(config_object=ProdConfig):
    """An application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    assets.init_app(app)
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(user.views.blueprint)
    app.register_blueprint(profile.views.blueprint)
    app.register_blueprint(articles.views.blueprint)
    return None


def register_errorhandlers(app):
    def errorhandler(error):
        response = error.to_json()
        response.status_code = error.status_code
        return response
    app.errorhandler(InvalidUsage)(errorhandler)


def register_shellcontext(app):
    """Register shell context objects."""
    def shell_context():
        """Shell context objects."""
        return {
            'db': db,
            'User': user.models.User,
            'UserProfile': profile.models.UserProfile,
            'Article': articles.models.Article,
            'Tag': articles.models.Tags,
        }

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)
    app.cli.add_command(commands.clean)
    app.cli.add_command(commands.urls)