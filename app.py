# import os
# from datetime import datetime
# from datetime import date
#
# from flask import (Flask, render_template, request, redirect,
#                    flash, url_for)
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.cyextension.processors import date_cls
#
# basedir = os.path.abspath(os.path.dirname(__file__))
# app = Flask(__name__)
# app.secret_key = os.urandom(24)
# app.config['SQLALCHEMY_DATABASE_URI'] = ('sqlite:///' +
#                                          os.path.join(basedir, 'example.db'))
# app.config['SQLALCHEMY_MIGRATE_REPO'] = os.path.join(basedir, 'db_repository')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
#
#
# class Assessment(db.Model):
#     # table name
#     __tablename__ = 'assessments'
#     # items
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(15), nullable=False)
#     code = db.Column(db.String(10), nullable=False)
#     description = db.Column(db.String(255))
#     state = db.Column(db.Integer)
#     date = db.Column(db.Date)
#     priority = db.Column(db.Integer)
#     __table_args__ = (
#         db.UniqueConstraint('code', 'name', name='uix_code_name'),
#     )
#
#
# # edit one item, renew its info
# @app.route('/edit/<int:todo_id>', methods=['POST'])
# def edit(todo_id):
#     # get args in request
#     sort_by = request.args.get('sort_by', 'date')
#     page_num = request.args.get('page_num', '1')
#     cur_page = request.args.get('cur_page', 'all')
#     select = request.args.get('select', '8')
#     # avoid select is passed by user as string type
#     if select.isdigit():
#         select = int(select)
#     else:
#         select = 8
#     if page_num.isdigit():
#         page_num = int(page_num)
#     else:
#         page_num = 1
#     name = request.form['name']
#     description = request.form['description']
#     deadline = request.form['date']
#     # check there is no too large year
#     try:
#         deadline_val = datetime.strptime(deadline, "%Y-%m-%d").date()
#         if deadline_val.year < 1900 or deadline_val.year > 2100:
#             raise ValueError("Date out of range")
#     except ValueError as e:
#         flash("Invalid date: " + str(e), 'error')
#         return redirect(url_for('index', page_num=page_num, cur_page=cur_page,
#                                 sort_by=sort_by, select=select))
#     # validation
#     deadline = datetime.strptime(deadline, '%Y-%m-%d')
#     state = int(request.form['status'])
#     priority = int(request.form['priority'])
#     code = request.form['code']
#     todo = Assessment.query.get(todo_id)
#     existing_module = Assessment.query.filter_by(code=code, name=name).first()
#     # if there is already same assessment
#     if existing_module and existing_module.id != todo_id:
#         flash("An assessment with same name and module code already exists.",
#               'error')
#         return redirect(url_for('index',
#                                 page_num=page_num, cur_page=cur_page,
#                                 sort_by=sort_by, select=select))
#
#     # if missing data
#     if not name or not code or not deadline:
#         flash("Submission failed due to lack of necessary information",
#               'error')
#         return redirect(url_for('index',
#                                 page_num=page_num, cur_page=cur_page,
#                                 sort_by=sort_by, select=select))
#     # if invalid data
#     if ((state != 0 and state != 1) or
#             priority <= 0 or
#             priority >= 4 or
#             not (isinstance(deadline, date_cls))):
#         flash("Invalid input", 'error')
#         return redirect(url_for('index', page_num=page_num, cur_page=cur_page,
#                                 sort_by=sort_by,
#                                 select=select))
#     # if oversize data
#     if len(name) > 15 or len(code) > 10 or len(description) > 255:
#         flash("Excessive data length", "error")
#         return redirect(url_for('index', page_num=page_num, cur_page=cur_page,
#                                 sort_by=sort_by, select=select))
#     # update to db
#     if todo:
#         todo.name = name
#         todo.code = code
#         todo.description = description
#         todo.date = deadline
#         todo.state = state
#         todo.priority = priority
#         db.session.commit()
#         flash("Edit Successfully", "success")
#     return redirect(
#         url_for('index', page_num=page_num, cur_page=cur_page, sort_by=sort_by,
#                 select=select))
#
#
# # update state with todo_id
# @app.route('/update_todo/<int:todo_id>', methods=['GET'])
# def update_todo(todo_id):
#     sort_by = request.args.get('sort_by', 'date')
#     page_num = request.args.get('page_num', '1')
#     cur_page = request.args.get('cur_page', 'all')
#     select = request.args.get('select', '8')
#     if select.isdigit():
#         select = int(select)
#     else:
#         select = 8
#     if page_num.isdigit():
#         page_num = int(page_num)
#     else:
#         page_num = 1
#     todo = Assessment.query.get(todo_id)
#     if todo:
#         todo.state = 1 - todo.state
#         db.session.commit()
#     return redirect(
#         url_for('index', page_num=page_num, cur_page=cur_page, sort_by=sort_by,
#                 select=select))
#
#
# # change sort type
# @app.route('/sort/<sort_by>')
# def sort(sort_by):
#     cur_page = request.args.get('cur_page', 'all')
#     select = int(request.args.get('select', '8'))
#     page_num = 1
#     return redirect(
#         url_for('index', page_num=page_num, cur_page=cur_page, sort_by=sort_by,
#                 select=select))
#
#
# # change page num
# @app.route('/page_num/<int:page_num>')
# def page(page_num):
#     cur_page = request.args.get('cur_page', 'all')
#     sort_by = request.args.get('sort_by', 'date')
#     select = request.args.get('select', '8')
#     if select.isdigit():
#         select = int(select)
#     else:
#         select = 8
#     return redirect(
#         url_for('index', page_num=page_num, cur_page=cur_page, sort_by=sort_by,
#                 select=select))
#
#
# # change batch size
# @app.route('/batch_change/<int:select>')
# def batch_change(select):
#     cur_page = request.args.get('cur_page', 'all')
#     sort_by = request.args.get('sort_by', 'date')
#     page_num = 1
#     return redirect(
#         url_for('index', page_num=page_num, cur_page=cur_page, sort_by=sort_by,
#                 select=select))
#
#
# # delete todo_id item
# @app.route('/delete_todo/<int:todo_id>')
# def delete_todo(todo_id):
#     todo = Assessment.query.get(todo_id)
#     if todo:
#         db.session.delete(todo)
#         db.session.commit()
#     sort_by = request.args.get('sort_by', 'date')
#     cur_page = request.args.get('cur_page', 'all')
#     select = request.args.get('select', '8')
#     page_num = request.args.get('page_num', '1')
#     if select.isdigit():
#         select = int(select)
#     else:
#         select = 8
#     if page_num.isdigit():
#         page_num = int(page_num)
#     else:
#         page_num = 1
#     return redirect(
#         url_for('index', page_num=page_num, cur_page=cur_page, sort_by=sort_by,
#                 select=select))
#
#
# # home page
# @app.route('/')
# def index():
#     # get args in request
#     sort_by = request.args.get('sort_by', 'date')
#     cur_page = request.args.get('cur_page', 'all')
#     select = request.args.get('select', '8')
#     page_num = request.args.get('page_num', '1')
#     # avoid user visit invalid url
#     if select.isdigit():
#         select = int(select)
#     else:
#         select = 8
#     if page_num.isdigit():
#         page_num = int(page_num)
#     else:
#         page_num = 1
#     # avoid invalid url
#     if sort_by not in ["date", "name", "priority"]:
#         sort_by = "date"
#     if cur_page not in ["all", "incomplete", "complete"]:
#         cur_page = "all"
#     if select not in [5, 8, 10]:
#         select = 8
#     # select how to show page
#     if cur_page == 'all':
#         todos = Assessment.query.order_by(Assessment.date.asc()).all()
#     elif cur_page == 'incomplete':
#         todos = Assessment.query.filter(Assessment.state == 0).order_by(
#             Assessment.date.asc()).all()
#     else:
#         todos = Assessment.query.filter(Assessment.state == 1).order_by(
#             Assessment.date.asc()).all()
#     # change todos into list of dict
#     todos = [{'id': todo.id, 'code': todo.code, 'name': todo.name,
#               'date': todo.date, 'state': todo.state,
#               'priority': todo.priority,
#               'description': todo.description} for todo in todos]
#     # determine todos pill state
#     for i in range(len(todos)):
#         map_pill = todos[i]
#         if map_pill['date'] < date.today():
#             map_pill['pill'] = 'red'
#         elif map_pill['priority'] == 3:
#             map_pill['pill'] = 'blue'
#         elif map_pill['priority'] == 2:
#             map_pill['pill'] = 'gray'
#         elif (map_pill['date'] - date.today()).days <= 10:
#             map_pill['pill'] = 'yellow'
#         else:
#             map_pill['pill'] = 'green'
#     # sort todos
#     todos = sorted(todos, key=lambda x: x[sort_by])
#     cnt = len(todos)
#     page_num_total = (cnt + select - 1) // select
#     # avoid delete last item
#     if page_num > page_num_total:
#         page_num = page_num_total
#     elif page_num <= 0:
#         page_num = 1
#
#     if sort_by == "priority":
#         todos.reverse()
#     # get index to choose page
#     start_index = (page_num - 1) * int(select)
#     end_index = page_num * int(select)
#     todos = todos[start_index:end_index]
#     return render_template('html/index.html', todos=todos,
#                            page_num_total=page_num_total, page_num=page_num,
#                            count=cnt,
#                            sort_by=sort_by, cur_page=cur_page, select=select)
#
#
# # change cur_page
# @app.route('/page_change/<page_id>')
# def page_change(page_id):
#     cur_page = page_id
#     sort_by = request.args.get('sort_by', 'date')
#     page_num = 1
#     select = request.args.get('select', '8')
#     if select.isdigit():
#         select = int(select)
#     else:
#         select = 8
#     return redirect(
#         url_for('index', cur_page=cur_page, sort_by=sort_by, select=select,
#                 page_num=page_num))
#
#
# # submit form according to form transmitted
# @app.route('/submit_form/', methods=['POST'])
# def submit_form():
#     sort_by = request.args.get('sort_by', 'date')
#     page_num = request.args.get('page_num', '1')
#     cur_page = request.args.get('cur_page', 'all')
#     select = request.args.get('select', '8')
#     if select.isdigit():
#         select = int(select)
#     else:
#         select = 8
#     if page_num.isdigit():
#         page_num = int(page_num)
#     else:
#         page_num = 1
#     name = request.form.get('name')
#     code = request.form.get('code')
#     description = request.form.get('description')
#     state = int(request.form.get('status'))
#     deadline = request.form.get('date')
#     priority = int(request.form.get('priority'))
#     try:
#         deadline_val = datetime.strptime(deadline, "%Y-%m-%d").date()
#         if deadline_val.year < 1900 or deadline_val.year > 2100:
#             raise ValueError("Date out of range")
#     except ValueError as e:
#         flash("Invalid date: " + str(e), 'error')
#         return redirect(url_for('index', page_num=page_num, cur_page=cur_page,
#                                 sort_by=sort_by, select=select))
#     # validation
#     deadline = datetime.strptime(deadline, '%Y-%m-%d')
#     existing_module = Assessment.query.filter_by(code=code, name=name).first()
#     if existing_module:
#         flash("An assessment with same name and module code already exists.",
#               'error')
#         return redirect(url_for('index', page_num=page_num, cur_page=cur_page,
#                                 sort_by=sort_by, select=select))
#     if not name or not code or not deadline:
#         flash("Submission failed due to lack of necessary information",
#               'error')
#         return redirect(url_for('index', page_num=page_num, cur_page=cur_page,
#                                 sort_by=sort_by, select=select))
#     if ((state != 0 and state != 1) or
#             priority <= 0 or
#             priority >= 4 or
#             not (isinstance(deadline, date_cls))):
#         flash("Invalid input", 'error')
#         return redirect(url_for('index', page_num=page_num, cur_page=cur_page,
#                                 sort_by=sort_by,
#                                 select=select))
#     if len(name) > 15 or len(code) > 10 or len(description) > 255:
#         flash("Excessive data length", "error")
#         return redirect(url_for('index', page_num=page_num, cur_page=cur_page,
#                                 sort_by=sort_by, select=select))
#
#     flash("Assessment submitted successfully", 'success')
#     assessment = Assessment(name=name, code=code, description=description,
#                             state=state, date=deadline, priority=priority)
#     db.session.add(assessment)
#     db.session.commit()
#     return redirect(
#         url_for('index', page_num=page_num, cur_page=cur_page, sort_by=sort_by,
#                 select=select))
#
#
# with app.app_context():
#     db.drop_all()
#     db.create_all()
# if __name__ == '__main__':
#     app.run(debug=True)
