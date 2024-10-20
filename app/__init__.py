from flask import Flask, session
from flask_pymongo import PyMongo
from dotenv import load_dotenv
from flask_mail import Mail
from instance.config import Config  # Import from the instance folder
from .eda_route import eda_bp
from .fraud_route import fraud_bp
from .policyrenewal_route import policyrenewal_bp
from .policyrecommend_route import policy_recommend_bp
from .sales_route import saleforecast_bp
from .channel_route import channel_bp
from .healthcare_route import health_bp

import os

load_dotenv()  # Load environment variables from .env file

mail = Mail()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    
    # Load the default configuration from the `instance/config.py`
    app.config.from_object(Config)
    
    # Set the secret key to some random bytes or a unique string
    app.secret_key = os.environ.get('SECRET_KEY')

    # mail = Mail(app)

    # Flask-Mail Configuration
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
    app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('EMAIL_USER')  # Default sender

    # Initialize the mail extension with the app
    mail.init_app(app)

    # Use environment variables
    app.config['MONGO_URI'] = os.getenv('MONGO_URI')

    # MongoDB and other configurations here...
    global mongo
    mongo = PyMongo(app)

    # Declare users_collection
    global users_collection
    users_collection = mongo.db.users
    
    # Import routes
    from .routes import main_bp
    from .risk_route import risk_bp  # Import the Blueprint
    
    app.register_blueprint(main_bp)
    app.register_blueprint(eda_bp)
    app.register_blueprint(risk_bp)
    app.register_blueprint(fraud_bp)
    app.register_blueprint(policyrenewal_bp)
    app.register_blueprint(policy_recommend_bp)
    app.register_blueprint(saleforecast_bp)
    app.register_blueprint(channel_bp)
    app.register_blueprint(health_bp)

    return app
