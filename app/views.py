from datetime import datetime

from flask import render_template, request, redirect, session, flash, url_for, \
    jsonify
import bcrypt
import sys
import base64
from sqlalchemy import text, func, desc

from app import app, db
from app import models
from app.models import Order,Stock,Concert,User

@app.route('/')
def index():
    # session['user_id'] = 0
    # session['username'] = "飞机炸弹"
    sql_query = text(
        "SELECT * FROM concerts WHERE type = :type_value ORDER BY start_time ASC LIMIT 4")
    concerts = db.session.execute(sql_query, {'type_value': '演唱会'})
    opera = db.session.execute(sql_query, {'type_value': '歌剧话剧'})
    sports = db.session.execute(sql_query, {'type_value': '体育'})
    concert_list = [
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
        for concert in concerts
    ]
    opera_list = [
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
        for concert in opera
    ]

    sports_list = [
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
        for concert in sports
    ]

    return render_template('html/index.html', concerts=concert_list,
                           sports=sports_list, opera=opera_list)


@app.route('/user_info')
def user_info():
    return render_template('html/user_info.html')


@app.route('/class')
def clas():
    # session['user_id'] = 0
    # session['username'] = "飞机炸弹"
    city = request.args.get('city', 'all')
    cur_class = request.args.get('cur_class', 'all')
    page_num = request.args.get('page_num', '1')
    sort_by = request.args.get('sort_by', 'name')
    search = int(request.args.get('search', 0))
    searchinfo = request.args.get('searchinfo', '123')
    page_num = int(page_num)

    if search == 0:

        # 动态构建 WHERE 子句
        where_clauses = []
        params = {}

        if cur_class != "all":
            where_clauses.append("type = :type_value")
            params["type_value"] = cur_class

        if city != "all":
            where_clauses.append("city = :city_value")
            params["city_value"] = city

        where_clause = " AND ".join(where_clauses) if where_clauses else "1=1"

        # 构建查询
        sql_query = text(f"""
            SELECT * 
            FROM concerts 
            WHERE {where_clause}
        """)
        concerts = db.session.execute(sql_query, params)
    else:
        searchinfo = request.args.get('searchinfo', '@#$')
        new_searchinfo = "%{}%".format(searchinfo)  # 添加通配符
        sql_query = text("SELECT * FROM concerts WHERE name LIKE :searchinfo")
        concerts = db.session.execute(sql_query,
                                      {'searchinfo': new_searchinfo})
    concert_list = [
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
        for concert in concerts if
        (concert.city == city or city == "all") and (
                    concert.type == cur_class or cur_class == "all")
    ]
    top_concerts = (
        Concert.query
        .order_by(desc(Concert.score))  # 按照 score 降序排列
        .limit(3)  # 限制为前 3 条记录
        .all()  # 执行查询并返回结果
    )
    top_concerts = [
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
        for concert in top_concerts
    ]
    select = 3
    concert_list = sorted(concert_list, key=lambda x: x[sort_by])
    cnt = len(concert_list)
    page_num_total = (cnt + select - 1) // select
    if page_num > page_num_total:
        page_num = page_num_total
    elif page_num <= 0:
        page_num = 1
    start_index = (page_num - 1) * int(select)
    end_index = page_num * int(select)
    concert_list = concert_list[start_index:end_index]
    cnt = len(concert_list)
    return render_template('html/class.html', cnt=cnt, searchinfo=searchinfo,
                           cur_class=cur_class, sort_by=sort_by, city=city,
                           concerts=concert_list, page_num=page_num,
                           page_num_total=page_num_total,top_concerts=top_concerts)


@app.route('/user_order')
def user_order():
    # session['user_id'] = 0
    # session['username'] = "飞机炸弹"
    user_id = session.get('user_id')
    orders = db.session.query(Order, Concert).join(Concert,
                                                   Order.concert_id == Concert.id).filter(
        Order.user_id == user_id).all()
    order_list = [
        {
            'order_id': order.id,
            'concert_id': concert.id,
            'name': concert.name,
            'location': concert.location,
            'total_price':order.total_price,
            'number':order.number,
            'day':order.day
        }
        for order, concert in orders
    ]
    return render_template('html/user_order.html', orders=order_list)


@app.route('/sign_in')
def sign_in():
    return render_template('html/sign in.html')


@app.route('/sign_up')
def sign_up():
    return render_template('html/sign up.html')


@app.route('/submit_sign_up')
def submit_sign_up():
    username = request.args.get('username')
    email = request.args.get('email')
    password = request.args.get('password')
    user = User.query.filter_by(email=email).first()
    if user :
        flash('该邮箱已被注册','error')
        return redirect(url_for('sign_up'))
    else:
        phone = request.args.get('phone')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        user = models.User(username=username, email=email,
                           password=base64.b64encode(hashed_password).decode(
                               'utf-8'), phone=phone)
        db.session.add(user)
        db.session.commit()
        app.logger.info(f"New user registered: {user.id}")
    return redirect('/sign_in')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # 查询用户
        user = models.User.query.filter_by(email=email).first()
        if user:
            hashed_pw_str = user.password
            hashed_pw = base64.b64decode(hashed_pw_str.encode('utf-8'))
            success = bcrypt.checkpw(password.encode('utf-8'), hashed_pw)
            if success:
                # 登录成功，设置 session
                session['user_id'] = user.id
                session['username'] = user.username
                session['admin'] = user.admin
                app.logger.info(f"user {user.id} login")
                flash('登录成功！', 'success')
                return redirect('/')
            else:
                flash('用户名或密码错误！', 'error')
                app.logger.error(f"user {user.id} failed to login")
        else:
            flash('用户名或密码错误！', 'error')
            app.logger.error(f"user failed to login")
    return redirect(url_for('sign_in'))


@app.route('/sign_out')
def sign_out():
    session.clear()
    return redirect('/')


# change sort type
@app.route('/sort/<sort_by>')
def sort(sort_by):
    searchinfo = request.args.get('searchinfo', '')
    search = request.args.get('search', '0')
    cur_class = request.args.get('cur_class', 'all')
    city = request.args.get('city', 'all')
    page_num = 1
    return redirect(
        url_for('clas', page_num=page_num, cur_class=cur_class,
                sort_by=sort_by,
                city=city, searchinfo=searchinfo, search=search))


@app.route('/city/<city>')
def city(city):
    searchinfo = request.args.get('searchinfo', '')
    search = request.args.get('search', '0')
    cur_class = request.args.get('cur_class', 'all')
    sort_by = request.args.get('sort_by', 'name')
    page_num = 1
    return redirect(
        url_for('clas', page_num=page_num, cur_class=cur_class,
                sort_by=sort_by,
                city=city, searchinfo=searchinfo, search=search))


@app.route('/choose_class/<cclass>')
def choose_class(cclass):
    searchinfo = request.args.get('searchinfo', '')
    search = request.args.get('search', '0')
    city = request.args.get('city', 'all')
    sort_by = request.args.get('sort_by', 'name')
    page_num = 1
    return redirect(
        url_for('clas', page_num=page_num, cur_class=cclass, sort_by=sort_by,
                city=city, searchinfo=searchinfo, search=search))


@app.route('/detail_base/<int:id_value>')
def detail_base(id_value):
    # session['user_id'] = 0
    # session['username'] = "飞机炸弹"
    sql_query = text(
        "SELECT * FROM concerts WHERE id = :id_value")
    concerts = db.session.execute(sql_query, {'id_value': id_value})

    concert_list = [
        {
            "id": concert.id,
            "name": concert.name,
            "description": concert.description,
            "start_time": concert.start_time,
            "location": concert.location,
            "city": concert.city,
            "link": concert.link,
            "duration": concert.duration,
            "start_price": concert.start_price,
            "end_price": concert.end_price,
            "end_time": concert.end_time
        }
        for concert in concerts
    ]
    concert = Concert.query.get(id_value)
    if concert:
        concert.score+=1
        db.session.commit()
    top_concerts = (
        Concert.query
        .order_by(desc(Concert.score))  # 按照 score 降序排列
        .limit(1)  # 限制为前 3 条记录
        .all()  # 执行查询并返回结果
    )
    top_concerts = [
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
        for concert in top_concerts
    ]
    return render_template('html/detail_base.html', concert=concert_list[0],top_concert=top_concerts[0])


# change page num
@app.route('/page_num/<int:page_num>')
def page(page_num):
    searchinfo = request.args.get('searchinfo', '')
    search = request.args.get('search', '0')
    cur_class = request.args.get('cur_class', 'all')
    sort_by = request.args.get('sort_by', 'name')
    city = request.args.get('city', 'all')

    return redirect(
        url_for('clas', page_num=page_num, cur_class=cur_class,
                sort_by=sort_by,
                city=city, searchinfo=searchinfo, search=search))

@app.route('/admin_show/<int:page_num>')
def admin_show(page_num):
    concerts=Concert.query.all()
    results = (
        db.session.query(
            Stock.concert_id,
            func.sum(Stock.total_tickets).label('total_inventory')
        )
        .group_by(Stock.concert_id)
        .all()
    )
    result_dict = {concert_id: total_inventory for concert_id, total_inventory
                   in results}

    concerts = [
        {
            "id": concert.id,
            "name": concert.name,
            "description": concert.description,
            "start_time": concert.start_time,
            "location": concert.location,
            "city": concert.city,
            "link": concert.link,
            "duration": concert.duration,
            "start_price": concert.start_price,
            "end_price": concert.end_price,
            "end_time": concert.end_time,
            "stock":result_dict[concert.id]
        }
        for concert in concerts
    ]
    select = 8
    cnt = len(concerts)
    page_num_total = (cnt + select - 1) // select
    if page_num > page_num_total:
        page_num = page_num_total
    elif page_num <= 0:
        page_num = 1
    start_index = (page_num - 1) * int(select)
    end_index = page_num * int(select)
    concerts = concerts[start_index:end_index]
    return render_template('html/admin_show.html',concerts=concerts,page_num=page_num,page_num_total=page_num_total)

@app.route('/admin_user/<int:page_num>')
def admin_user(page_num):
    users = User.query.filter_by(admin=False).all()
    select = 8
    cnt = len(users)
    page_num_total = (cnt + select - 1) // select
    if page_num > page_num_total:
        page_num = page_num_total
    elif page_num <= 0:
        page_num = 1
    start_index = (page_num - 1) * int(select)
    end_index = page_num * int(select)
    users = users[start_index:end_index]
    return render_template('html/admin_user.html',users=users,page_num=page_num,page_num_total=page_num_total)
@app.route('/search/<searchinfo>', methods=['GET', 'POST'])
def search(searchinfo):
    city = request.args.get('city', 'all')
    cur_class = request.args.get('cur_class', 'all')
    page_num = request.args.get('page_num', '1')
    sort_by = request.args.get('sort_by', 'name')
    return redirect(
        url_for('clas', page_num=page_num, cur_class=cur_class,
                sort_by=sort_by,
                city=city, searchinfo=searchinfo, search=1))


@app.route('/order_submit', methods=['GET', 'POST'])
def order_submit():
    user_id = request.form.get('user_id')
    concert_id = request.form.get('concert_id')
    day = request.form.get('day')
    price = int(request.form.get('price'))
    quantity = int(request.form.get('quantity'))
    stock_record = Stock.query.filter_by(concert_id=concert_id,
                                         price=price,day=day)
    stock_record=stock_record.first()
    if not stock_record:
        return jsonify({"error": "Stock record not found"}), 404

        # 检查库存是否足够
    if stock_record.remaining_tickets < quantity:
        return jsonify({"error": "Not enough tickets in stock"}), 400

        # 减少库存
    stock_record.remaining_tickets -= quantity
    try:
        day = datetime.strptime(day, '%Y-%m-%d').date()
    except ValueError as e:
        return f"Invalid date format for 'day': {day}", 400
    total_price = price * quantity
    order = Order(user_id=user_id, number=quantity, price=price,
                  total_price=total_price
                  , concert_id=concert_id, day=day)
    app.logger.info(f"user {user_id} order concert {concert_id} is submitted")
    concert = Concert.query.get(concert_id)
    if concert:
        concert.score+=5
    db.session.add(order)
    db.session.commit()
    return '', 204
@app.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        app.logger.info(
            f"user {user_id} is deleted by Admin")
        db.session.query(Order).filter_by(concert_id=user_id).delete()
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for('admin_user'))
@app.route('/delete_concert/<int:id_value>')
def delete_concert(id_value):
    concert = Concert.query.get(id_value)
    if concert:
        app.logger.info(
            f"concert {id_value} is deleted by Admin")

        db.session.query(Order).filter_by(concert_id=id_value).delete()
        db.session.query(Stock).filter_by(concert_id=id_value).delete()
        db.session.delete(concert)
        db.session.commit()
    return redirect(url_for('admin_show', page_num=1))
@app.route('/edit_concert/<int:id_value>',methods=['GET', 'POST'])
def edit_concert(id_value):
    concert = Concert.query.get(id_value)
    start_time =request.form['start_time']
    start_time = datetime.strptime(start_time, '%Y-%m-%d')
    end_time =request.form['end_time']
    end_time = datetime.strptime(end_time, '%Y-%m-%d')
    start_price=request.form['start_price']
    page_num=int(request.form['page_num'])
    end_price=request.form['end_price']
    stock=int(request.form['stock'])
    specific_stocks = Stock.query.filter_by(concert_id=id_value).all()
    normal_stock=specific_stocks[0]
    vip_stock=specific_stocks[1]
    normal_stock.remaining_tickets=stock//2
    vip_stock.remaining_tickets=stock-stock//2
    name = request.form['name']
    if concert:
        concert.start_time = start_time
        concert.end_time = end_time
        concert.start_price = start_price
        concert.end_price = end_price
        concert.name = name
        app.logger.info(
            f"concert {id_value} is edited by Admin")
        db.session.commit()
    return redirect(url_for('admin_show', page_num=page_num))
@app.route('/add_concert',methods=['GET', 'POST'])
def add_concert():
    start_time = request.form['start_time']
    start_time = datetime.strptime(start_time, '%Y-%m-%d')
    end_time = request.form['end_time']
    end_time = datetime.strptime(end_time, '%Y-%m-%d')
    start_price = request.form['start_price']
    end_price = request.form['end_price']
    name = request.form['name']
    location = request.form['location']
    city=request.form['city']
    type= request.form['type']
    stock=request.form['stock']
    if start_time==end_time:
        duration=1
    else:
        duration=2
    concert=Concert(start_time=start_time,link='no.png',description='',location=location,duration=duration,type=type, end_time=end_time, start_price=start_price,end_price=end_price, name=name, city=city)
    db.session.add(concert)
    db.session.commit()
    if duration==1:
        stock1=Stock(concert_id=concert.id,price=concert.start_price,day=concert.start_time,total_tickets=stock,remaining_tickets=stock)
        stock2 = Stock(concert_id=concert.id, price=concert.end_price,
                   day=concert.start_time, total_tickets=stock,
                   remaining_tickets=stock)
        db.session.add(stock1)
        db.session.add(stock2)
        db.session.commit()
    else:
        stock1=Stock(concert_id=concert.id,price=concert.start_price,day=concert.start_time,total_tickets=stock,remaining_tickets=stock)
        stock2 = Stock(concert_id=concert.id, price=concert.end_price,
                       day=concert.start_time, total_tickets=stock,
                       remaining_tickets=stock)
        stock3=Stock(concert_id=concert.id,price=concert.start_price,day=concert.end_time,total_tickets=stock,remaining_tickets=stock)
        stock4=Stock(concert_id=concert.id,price=concert.start_price,day=concert.end_time,total_tickets=stock,remaining_tickets=stock)
        db.session.add(stock1)
        db.session.add(stock2)
        db.session.add(stock3)
        db.session.add(stock4)
        db.session.commit()

    app.logger.info(
        f"concert {concert.id} is added by Admin")
    return redirect(url_for('admin_show', page_num=1))
