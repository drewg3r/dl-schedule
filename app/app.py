from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def create_app(config='config.DevConfig'):
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config)

    # Initialize Plugins
    db.init_app(app)
    migrate.init_app(app, db)

    from models import load_user
    login_manager.init_app(app)

    with app.app_context():
        from views.index import bp as index_bp
        from views.auth import bp as auth_bp
        from views.schedule import bp as schedule_bp

        app.register_blueprint(index_bp)
        app.register_blueprint(auth_bp)
        app.register_blueprint(schedule_bp)

        return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0')
