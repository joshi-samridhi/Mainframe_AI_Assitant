"""
Configuration settings for Mainframe AI Support Assistant
"""
import os
from datetime import timedelta

# Get the base directory
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Base configuration"""
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database Configuration
    # Use absolute path for SQLite database
    instance_path = os.path.join(basedir, 'instance')
    os.makedirs(instance_path, exist_ok=True)
    
    db_path = os.path.join(instance_path, 'mainframe_assistant.db')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or f'sqlite:///{db_path}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session Configuration
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # File Upload Configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'txt', 'log', 'png', 'jpg', 'jpeg'}
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    
    # Tesseract OCR Configuration
    TESSERACT_PATH = os.environ.get('TESSERACT_PATH') or \
        'C:/Program Files/Tesseract-OCR/tesseract.exe'
    
    # Application Settings
    APP_NAME = 'Mainframe AI Support Assistant'
    APP_VERSION = '1.0.0'
    
    # Output Directory
    OUTPUT_FOLDER = 'output'
    
    @staticmethod
    def init_app(app):
        """Initialize application with config"""
        pass


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True  # Require HTTPS


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/test.db'
    WTF_CSRF_ENABLED = False


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

# Made with Bob
