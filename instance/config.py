from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://localhost:27017/mydatabase'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_very_secure_key'
    SESSION_TYPE = 'filesystem'  # Or 'redis' if using a Redis session store
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour

# You can also define different configurations for different environments (optional)
class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    SESSION_TYPE = 'redis'  # Example for using Redis in production

class TestingConfig(Config):
    TESTING = True

