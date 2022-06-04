from flask import Flask, Blueprint
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
rest_api = Api()


def create_app(config='config.DemoConfig'):
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db)

    from service.auth import load_user
    login_manager.init_app(app)

    @app.before_first_request
    def create_tables():
        from service.db import create_demo_db
        db.create_all()
        if app.config['DEMO_MODE']:
            create_demo_db(db)

    with app.app_context():
        from rest import event, subject
        api_bp = Blueprint('api', __name__, url_prefix='/api')
        rest_api.init_app(api_bp)
        rest_api.add_resource(subject.Subject, '/subject')
        rest_api.add_resource(subject.Subjects, '/subjects')
        rest_api.add_resource(subject.Search, '/subjects/search')

        rest_api.add_resource(event.Event, '/event')
        rest_api.add_resource(event.Events, '/events')
        rest_api.add_resource(event.Now, '/event/now')
        rest_api.add_resource(event.Next, '/event/next')

        from views.index import bp as index_bp
        from views.auth import bp as auth_bp
        from views.schedule import bp as schedule_bp

        app.register_blueprint(api_bp)
        app.register_blueprint(index_bp)
        app.register_blueprint(auth_bp)
        app.register_blueprint(schedule_bp)

        return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0')
