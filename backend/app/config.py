import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "aura-sbi-hackathon-dev-secret-2025")

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///aura.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Celery (Celery 5 uses lowercase config keys)
    CELERY = {
        "broker_url": os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0"),
        "result_backend": os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/0"),
        "task_serializer": "json",
        "result_serializer": "json",
        "accept_content": ["json"],
        "timezone": "Asia/Kolkata",
        "enable_utc": True,
        "task_track_started": True,
    }
