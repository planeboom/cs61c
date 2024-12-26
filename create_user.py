from app.models import Stock, User
import random
from config import SQLALCHEMY_DATABASE_URI
from flask import session
from sqlalchemy import text
from app import db, app
from app import models
import os.path
with app.app_context():

    for _ in range(30):
        user = User(username=f"User{_}",password=1,email=f"{_}@aaa",admin=0,phone=1)
        db.session.add(user)
        db.session.commit()
