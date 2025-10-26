"""File running the flask web application."""
from src.webapp import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
