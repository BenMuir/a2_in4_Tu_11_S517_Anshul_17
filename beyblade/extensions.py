from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Shared extension objects, created here and attached to the app in create_app()
db = SQLAlchemy()
login_manager = LoginManager()

# Flask-Login: redirect anonymous users to the login page for @login_required routes
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access that page.'
login_manager.login_message_category = 'warning'


# Reloads the logged-in user from the session's stored user id on each request
@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return db.session.get(User, int(user_id))
