from flask import current_app
from app.models import db
import click
from sqlalchemy import text

def init_app(app):
    db.init_app(app)

@click.command("init-db")
def init_db_command():
    """Clear existing data and create new tables."""
    with current_app.app_context():
        db.drop_all()
        db.create_all()

        with current_app.open_resource("schema.sql") as f:
            schema_sql = f.read().decode("utf-8")
        
        with db.engine.connect() as connection:
            connection.execute(text(schema_sql))

    click.echo("Initialized the database!")
