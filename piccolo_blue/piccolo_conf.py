import os

from piccolo.conf.apps import AppRegistry
from piccolo.engine.postgres import PostgresEngine


DB = PostgresEngine(
    config={
        "port": 5432,
        "user": os.environ.get("POSTGRES_USER"),
        "password": os.environ.get("POSTGRES_PASSWORD"),
        "database": os.environ.get("POSTGRES_DB"),
        "host": os.environ.get("DB_HOST"),
    }
)

APP_REGISTRY = AppRegistry(apps=['piccolo_project.piccolo_app'])
