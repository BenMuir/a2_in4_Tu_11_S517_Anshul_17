import os
from flask import Flask, render_template
from .extensions import db, login_manager, bootstrap

def create_app():
    app = Flask(__name__)

    # Secret key for WTForms and Session management.
    # On the live server, set a SECRET_KEY environment variable instead of using the dev key.
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'x-burst-dev-secret-key')

    # SQLite database stored at instance/beyblade.sqlite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///beyblade.sqlite'

    db.init_app(app)

    login_manager.init_app(app)
    bootstrap.init_app(app)

    # Import and register the routing blueprints
    from .routes import bp
    app.register_blueprint(bp)

    from .auth import auth_bp
    app.register_blueprint(auth_bp)

    # Create any missing tables on startup. Existing tables and data are left alone.
    with app.app_context():
        db.create_all()

    # Custom error handlers required by the assignment guidelines
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500

    return app