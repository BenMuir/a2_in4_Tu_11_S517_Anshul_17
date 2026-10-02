from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Secret key for WTForms and Session management
    app.config['SECRET_KEY'] = 'x-burst-dev-secret-key'
    
    # SQLite database configuration for Eric's models
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///beyblade.sqlite'
    
    db.init_app(app)

    # Import and register the routing blueprint we defined earlier
    from .routes import bp
    app.register_blueprint(bp)

    # Custom error handlers required by the assignment guidelines
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500

    return app