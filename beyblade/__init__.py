
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
 
    return app