from flask_sqlalchemy import SQLAlchemy

from app import db

# 用户表
class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.Date, server_default=db.func.now())
    admin=db.Column(db.Boolean, default=False)
    orders = db.relationship('Order', back_populates='user')

# 演唱会表
class Concert(db.Model):
    __tablename__ = 'concerts'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    start_time = db.Column(db.Date, nullable=False)
    end_time = db.Column(db.Date)
    location = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(20), nullable=False)
    link = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    start_price = db.Column(db.Integer, nullable=False)
    end_price = db.Column(db.Integer, nullable=False)
    orders = db.relationship('Order', back_populates='concert')
    score = db.Column(db.Integer, nullable=False)

# 票表 (关联表实现多对多关系)
class Ticket(db.Model):
    __tablename__ = 'tickets'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    concert_id = db.Column(db.Integer, db.ForeignKey('concerts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    section = db.Column(db.String(50))
    row = db.Column(db.String(50))
    seat_number = db.Column(db.String(50))
    price = db.Column(db.Float, nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    # concert = db.relationship('Concert', back_populates='tickets')
    # user = db.relationship('User', back_populates='tickets')

# 订单表
class Order(db.Model):
    __tablename__ = 'orders'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    number = db.Column(db.Integer, nullable=False)
    concert_id = db.Column(db.Integer, db.ForeignKey('concerts.id'), nullable=True)
    order_time = db.Column(db.Date, server_default=db.func.now())
    price = db.Column(db.Integer, nullable=False)
    day = db.Column(db.DATE, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    user = db.relationship('User', back_populates='orders')
    concert= db.relationship('Concert', back_populates='orders')


# 库存表
class Stock(db.Model):
    __tablename__ = 'stock'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    concert_id = db.Column(db.Integer, db.ForeignKey('concerts.id'), nullable=False)
    day = db.Column(db.DATE, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    total_tickets = db.Column(db.Integer, nullable=False)  # 总票数
    remaining_tickets = db.Column(db.Integer, nullable=False)  # 剩余票数
    concert = db.relationship('Concert', backref='ticket_inventory')
