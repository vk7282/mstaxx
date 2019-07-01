import os
project_dir = os.path.dirname(os.path.abspath(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "postgresql://localhost/book"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
