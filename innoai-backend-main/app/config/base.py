# app/config/base.py
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "YOUR-FALLBACK-SECRET-KEY")
    DATABASE_URI = "sqlite:///database.db"
    RATELIMIT_ENABLED = os.environ.get("RATELIMIT_ENABLED", "False") == "True"
    RATELIMIT_STORAGE_URI = os.environ.get("RATELIMIT_STORAGE_URI", "memory://")
    CACHE_TYPE = os.environ.get("CACHE_TYPE", "SimpleCache")
    CACHE_ENABLED = os.environ.get("CACHE_ENABLED", "False") == "True"
    CACHE_STORAGE_URL = os.environ.get("CACHE_STORAGE_URL", None)
    CACHE_EXEMPTED_ROUTES = ["/api/auth/"]
    CACHE_KEY_PREFIX = "flask_cache_"
    if CACHE_TYPE != "SimpleCache" and CACHE_STORAGE_URL:
        CACHE_REDIS_URL = CACHE_STORAGE_URL
        CACHE_DEFAULT_TIMEOUT = 180
    else:
        CACHE_DEFAULT_TIMEOUT = 60