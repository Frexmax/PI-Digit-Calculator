"""File running the flask web application."""
from pathlib import Path
import sys

# add the src directory to the Python path
sys.path.append(str(Path(__file__).resolve().parent))

from webapp import create_app

flask_app = create_app()

if __name__ == "__main__":
     flask_app.run(debug=True)
