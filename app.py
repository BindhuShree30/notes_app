import os

from flask import Flask, render_template

from extensions import db
from config import config
from models import User, Note

# Import Blueprints
from routes.auth import auth_bp
from routes.notes import notes_bp
from routes.api import api_bp


def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config)

    # Initialize SQLAlchemy
    db.init_app(app)

    # Create instance folder if it doesn't exist
    os.makedirs(app.instance_path, exist_ok=True)

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(notes_bp)
    app.register_blueprint(api_bp)

    # Home Page
    @app.route("/")
    def home():
        return render_template("index.html")

    # Create database tables
    with app.app_context():
        db.create_all()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)