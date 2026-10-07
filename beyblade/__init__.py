from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # Secret key for WTForms and Session management
    app.config['SECRET_KEY'] = 'x-burst-dev-secret-key'

    # SQLite database configuration for Eric's models
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///beyblade.sqlite'

    db.init_app(app)

    # Flask-Login: redirect anonymous users to the login page for @login_required routes
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access that page.'
    login_manager.login_message_category = 'warning'

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

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
