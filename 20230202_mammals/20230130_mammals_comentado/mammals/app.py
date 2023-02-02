from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mammals.sqlite3"

    with app.app_context():
        from .models import init_db
        from .views import init_views

        db_access = init_db(app)
        init_views(app, db_access)

    return app
