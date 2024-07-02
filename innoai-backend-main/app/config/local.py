# app/config/local.py
import os
from dotenv import load_dotenv
from .base import Config, BASE_DIR

ENV_FILE_PATH = BASE_DIR / ".env.local"
load_dotenv(ENV_FILE_PATH)

class LocalConfig(Config):
    TESTING = True
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True
    STATIC_AUTO_RELOAD = True
    EXPLAIN_TEMPLATE_LOADING = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "YOUR-FALLBACK-SECRET-KEY")
    SQLALCHEMY_DATABASE_URI = Config.DATABASE_URI