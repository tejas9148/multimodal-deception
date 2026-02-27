import os
from dotenv import load_dotenv

load_dotenv()

# Base model directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, 'models')

# Development Configuration
class DevelopmentConfig:
    """Development configuration"""
    DEBUG = True
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'deceptra-secret-key-dev')
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB max file size
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'webp'}
    MODEL_DIR = MODEL_DIR
    TEXT_MODEL_PATH = os.path.join(MODEL_DIR, 'text_classifier.pkl')
    IMAGE_MODEL_PATH = os.path.join(MODEL_DIR, 'image_classifier.pkl')
    VECTORIZER_PATH = os.path.join(MODEL_DIR, 'vectorizer.pkl')
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///deceptra.db')
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:5173,http://localhost:3000')

# Testing Configuration
class TestingConfig:
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    SECRET_KEY = 'test-secret-key'
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'webp'}
    MODEL_DIR = MODEL_DIR
    TEXT_MODEL_PATH = os.path.join(MODEL_DIR, 'text_classifier.pkl')
    IMAGE_MODEL_PATH = os.path.join(MODEL_DIR, 'image_classifier.pkl')
    VECTORIZER_PATH = os.path.join(MODEL_DIR, 'vectorizer.pkl')
    DATABASE_URL = 'sqlite:///:memory:'
    CORS_ORIGINS = 'http://localhost:5173,http://localhost:3000'

# Production Configuration
class ProductionConfig:
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'change-me-in-production')
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'webp'}
    MODEL_DIR = MODEL_DIR
    TEXT_MODEL_PATH = os.path.join(MODEL_DIR, 'text_classifier.pkl')
    IMAGE_MODEL_PATH = os.path.join(MODEL_DIR, 'image_classifier.pkl')
    VECTORIZER_PATH = os.path.join(MODEL_DIR, 'vectorizer.pkl')
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost/deceptra')
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'https://deceptra.ai')

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
