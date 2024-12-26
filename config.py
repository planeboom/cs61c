import os

basedir = os.path.abspath(os.path.dirname(__file__))
SECRET_KEY = os.urandom(24)
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_NATIVE_UNICODE=False
SQLALCHEMY_TRACK_MODIFICATIONS = False
