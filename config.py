import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "smart-krishi-insecure-secret-key-3849")
    DATABASE_PATH = BASE_DIR / os.getenv("DATABASE", "database/smart_krishi.db")
    UPLOAD_FOLDER = BASE_DIR / "static" / "uploads"
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
    
    # Supported Languages
    LANGUAGES = ["en", "te"]
    DEFAULT_LANGUAGE = "en"
    
    # Weather settings
    WEATHER_PROVIDER = os.getenv("WEATHER_PROVIDER", "open-meteo")
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")
    
    # AI Model Settings
    AI_MODEL_PROVIDER = os.getenv("AI_MODEL_PROVIDER", "hybrid")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
