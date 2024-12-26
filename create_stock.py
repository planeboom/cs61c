from app.models import Stock
import random
from config import SQLALCHEMY_DATABASE_URI
from flask import session
from sqlalchemy import text
from app import db, app
from app import models
import os.path
with app.app_context():
    sql_query = text("SELECT * FROM concerts")
    result = db.session.execute(sql_query)
    results = [
        {
            "id": concert.id,
            "name": concert.name,
            "description": concert.description,
            "start_time": concert.start_time,
            "location": concert.location,
            "city": concert.city,
            "link": concert.link,
            "type": concert.type,
            "duration": concert.duration,
            "start_price": concert.start_price,
            "end_price": concert.end_price,
            "end_time": concert.end_time
        }
        for concert in result
    ]
    for record in results:
        for i in range(record["duration"]):
            if i==0:
                day=record["start_time"]
            else:
                day=record["end_time"]
            if record["start_price"] == record["end_price"]:
                total_tickets=random.randint(10000,20000)
                stock=Stock(concert_id=record["id"],day=day,price=record["start_price"],total_tickets=total_tickets,remaining_tickets=total_tickets)
                db.session.add(stock)
                db.session.commit()
            else:
                total_tickets=random.randint(10000,20000)
                stock = Stock(concert_id=record["id"], day=day, price=record["start_price"], total_tickets=total_tickets, remaining_tickets=total_tickets)
                db.session.add(stock)
                stock = Stock(concert_id=record["id"], day=day, price=record["end_price"], total_tickets=total_tickets, remaining_tickets=total_tickets)
                db.session.add(stock)
                db.session.commit()
