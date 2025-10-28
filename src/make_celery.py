"""File running celery."""
from pathlib import Path
import sys

# add the src directory to the Python path
sys.path.append(str(Path(__file__).resolve().parent))

from webapp import create_app

flask_app = create_app()
celery_app = flask_app.extensions["celery"]

celery_app.conf.update(
    task_track_started=True,
    result_expires=3600,
)
