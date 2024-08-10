import logging
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

logging.basicConfig(level=logging.WARNING)

db_username = os.environ.get("DB_USERNAME")
if db_username is None:
    logging.warning("DB_USERNAME is not set in the environment variables.")

db_password = os.environ.get("DB_PASSWORD")
if db_password is None:
    logging.warning("DB_PASSWORD is not set in the environment variables.")

db_host = os.environ.get("DB_HOST")
if db_host is None:
    logging.warning("DB_HOST is not set in the environment variables.")

db_port = os.environ.get("DB_PORT")
if db_port is None:
    logging.warning("DB_PORT is not set in the environment variables.")

db_name = os.environ.get("DB_NAME", "mydatabase")
if db_name is None:
    logging.warning("DB_NAME is not set in the environment variables.")

logging.info(f"Configured to connect to database {db_name} on {db_host}:{db_port} as {db_username}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"

db = SQLAlchemy(app)

app.logger.setLevel(logging.DEBUG)