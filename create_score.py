from app.models import Stock, Concert
import random
from config import SQLALCHEMY_DATABASE_URI
from flask import session
from sqlalchemy import text
from app import db, app
from app import models
import os.path

from create_stock import results

with app.app_context():

    result=Concert.query.all()
    for record in result:
        record.score=11
    db.session.commit()


