from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()


def create_app(config='config.DevConfig'):
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config)

    # Initialize Plugins
    db.init_app(app)
    migrate.init_app(app, db)
    # r.init_app(app)

    with app.app_context():
        from views.index import bp as index_bp
        app.register_blueprint(index_bp)

        return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0')
