<<<<<<< HEAD

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
 
# creates db objects and create_app factory. same create_app function as uused in main.py
#points to the db_beyblade.sqlite file
db = SQLAlchemy()
 
 
def create_app():
    app = Flask(__name__)
    app.secret_key = "change-me"  # needed later for forms/sessions
 
    basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "db_beyblade.sqlite")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
 
    db.init_app(app)

    from . import models  # importing and registering models with sqlalchemy 

    from .routes import main_bp
    app.register_blueprint(main_bp)
 
    #with app.app_context():
        #db.create_all() DB.CREATE_ALL ONLY CREATES TABLES IF THEY DONT EXIST. COMMENTED OUT FOR NOW, WILL UNCOMMENT WHEN WE NEED TO CREATE TABLES
 
=======
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

>>>>>>> f86cab5e2b542268c0820e7dad9c237b999423a0
    return app