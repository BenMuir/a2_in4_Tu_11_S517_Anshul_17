from os import makedirs

from flask import Flask, flash, redirect, render_template, request
from .extensions import db, login_manager

def create_app():
    app = Flask(__name__)

    # Secret key for WTForms and Session management
    app.config['SECRET_KEY'] = 'x-burst-dev-secret-key'

    # SQLite database configuration for Eric's models
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///beyblade.sqlite'

    db.init_app(app)

    login_manager.init_app(app)

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

    # Configuring photo uploads for the application
    app.config['UPLOAD_FOLDER'] = 'static/uploads'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Error handling for large file uploads
    @app.errorhandler(413)
    def file_too_large(e):
        flash("That image is too large. The maximum size is 5 MB.", "danger")
        return redirect(request.referrer or "/") 

    return app