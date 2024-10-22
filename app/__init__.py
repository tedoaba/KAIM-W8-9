import os
from dotenv import load_dotenv
from flask import Flask

from app import pages, transactions, data, predict
from app.models import db
from app.database import init_db_command

load_dotenv()

def create_app():
    app = Flask(__name__)

    # Load configuration from environment variables
    app.config.from_prefixed_env()

    # Set SQLAlchemy database URI
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        raise RuntimeError("DATABASE_URL environment variable not set.")
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(pages.bp)
    app.register_blueprint(transactions.bp)
    app.register_blueprint(data.bp)
    app.register_blueprint(predict.bp)
    #app.register_blueprint(train.bp)

    # Add CLI command
    app.cli.add_command(init_db_command)

    # Print environment information for debugging
    print(f"Current Environment: {os.getenv('ENVIRONMENT')}")
    print(f"Using Database: {app.config.get('SQLALCHEMY_DATABASE_URI')}")

    return app
