from config import SQLALCHEMY_DATABASE_URI


from app import db, app
import os.path


# Creates all the tables and the database.
with app.app_context():
    db.drop_all()
    db.create_all()

