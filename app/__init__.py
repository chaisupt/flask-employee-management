from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import DevelopmentConfig, ProductionConfig
import os

from app.utils import init_status

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # Check FLASK_ENV environment variable and apply the right configuration
    env = os.getenv('FLASK_ENV', 'production')  # Default to production if not set
    if env == 'development':
        app.config.from_object(DevelopmentConfig)
        print("Running in Development Mode")
    else:
        app.config.from_object(ProductionConfig)
        print("Running in Production Mode")

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Import and register blueprints
    from .routes import main
    app.register_blueprint(main)

    # Create database tables
    with app.app_context():
        db.create_all()
        init_status()

    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))   

    return app
