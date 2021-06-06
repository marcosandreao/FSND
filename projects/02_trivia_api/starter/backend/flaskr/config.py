import os
SECRET_KEY = os.urandom(32)
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = os.getenv("FLASK_DEBUG", True)

db_user = os.getenv("DB_USER", "caryn")
db_password = os.getenv("DB_PASSWORD", "caryn")
db_host = os.getenv("DB_HOST", "localhost")
db_port = os.getenv("DB_PORT", "5432")
db_name = os.getenv("DB_NAME", "trivia")

# Connect to the database
SQLALCHEMY_DATABASE_URI = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(db_user, db_password, db_host, db_port, db_name)
SQLALCHEMY_TRACK_MODIFICATIONS = False
