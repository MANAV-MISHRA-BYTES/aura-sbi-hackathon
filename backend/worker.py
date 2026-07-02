# Entry point for Celery worker
# Run: celery -A worker:celery_app worker --loglevel=info
from app import create_app

flask_app  = create_app()
celery_app = flask_app.extensions["celery"]

import app.tasks  # noqa: registers tasks with Celery
