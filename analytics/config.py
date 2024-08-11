import logging
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Fetch and validate environment variables
db_username = os.environ.get("DB_USERNAME")
db_password = os.environ.get("DB_PASSWORD")
db_host = os.environ.get("DB_HOST")
db_port = os.environ.get("DB_PORT")
db_name = os.environ.get("DB_NAME")

# Ensure all required variables are set
if not all([db_username, db_password, db_host, db_port]):
    raise EnvironmentError("One or more required database environment variables are missing.")

# Log the database connection details, avoiding logging sensitive information
print(f"Configured to connect to database {db_name} on {db_host}:{db_port} as {db_username}")

# Construct the database URI
db_uri = f"postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"
print(f"Database URI: {db_uri}")

# Initialize Flask app and SQLAlchemy
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = db_uri

db = SQLAlchemy(app)

# Set logging level for the application
app.logger.setLevel(logging.DEBUG)
