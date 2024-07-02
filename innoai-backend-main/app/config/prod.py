# app/config/prod.py
import os
from dotenv import load_dotenv
from .base import Config, BASE_DIR

ENV_FILE_PATH = BASE_DIR / ".env.prod"
load_dotenv(ENV_FILE_PATH)

class ProdConfig(Config):
    TESTING = False
    DEBUG = False
    TEMPLATES_AUTO_RELOAD = False
    STATIC_AUTO_RELOAD = False
    SECRET_KEY = os.getenv("SECRET_KEY", "YOUR-FALLBACK-SECRET-KEY")
    SQLALCHEMY_DATABASE_URI = Config.DATABASE_URI