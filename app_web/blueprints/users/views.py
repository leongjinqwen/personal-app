from flask import Blueprint, render_template, request, url_for, redirect, flash, jsonify
from models.user import User
from models.expense import Expense
from models.category import Category
from flask_login import login_required, login_user, current_user
import datetime
from peewee import fn
from decimal import *

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
  return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
  user_password = request.form['password']
  user = User(username=request.form['username'].lower(),email=request.form['email'].lower(),password=user_password)
  if user.save():
    login_user(user)
    flash("Successfully signed up and logged in.","primary")
    return redirect(url_for('users.show',username=user.username))
  else:
    for error in user.errors:
      flash(error,"danger")
    return render_template('users/new.html')


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
  return render_template('users/show.html',username=username)


@users_blueprint.route('/', methods=["GET"])
def index():
  return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
  pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
  pass

@users_blueprint.route('/dashboard', methods=["GET"])
def dashboard():
  categories = Category.select().where(Category.user==current_user.id)
  data = {}
  '''sample data
  [
    { "General" : 100 },
    { "Food" : 150 },
  ]
  '''
  for cat in categories:
    current = datetime.datetime.now()
    ttl = Expense.select(fn.SUM(Expense.amount).alias('total')).where(Expense.cat == cat,Expense.month==datetime.date.today().strftime("%b"),Expense.created_at.year==current.year)
    data[cat.name] = 0.0 if ttl[0].total == None else str(ttl[0].total)
  months = {
    1:'Jan',
    2:'Feb',
    3:'Mar',
    4:'Apr',
    5:'May',
    6:'Jun',
    7:'Jul',
    8:'Aug',
    9:'Sep',
    10:'Oct',
    11:'Nov',
    12:'Dec',
  }

  def _get_last_twelve(current):
    last_twelve = [] # last 12months
    # check current month and year => 1, 2021
    month = current.month
    year = current.year
    for i in range(12):  # loop for 12 times
      # if month - 1 not equal to zero, then year == current.year, else year == current.year - 1 and month == 12
      if not month == 0:
        last_twelve.append((year, month))
      else:
        month = 12
        year = year - 1
        last_twelve.append((year, month))
      month = month - 1
    last_twelve.reverse()
    return last_twelve

  twelve = _get_last_twelve(current)
  
  
  
  '''
  datum = [
    "Jan, 2021": {
      "Total": 0,
      "General": 0,
      "Entertainment": 0,
    }
  ]
  '''
  def _get_category_monthly_total(category,twelve):
    expenses_list = []
    for pairs in twelve:
      ttl = Expense.select(fn.SUM(Expense.amount).alias('total')).where(Expense.cat == category, Expense.month==months[pairs[1]],Expense.created_at.year==pairs[0])
      expenses_list.append(0 if ttl[0].total == None else str(ttl[0].total))
    return expenses_list

  result = {}

  month_labels = []
  aggregate = [] # to get aggregate amount for each month

  for pairs in twelve:
    ttl = Expense.select(fn.SUM(Expense.amount).alias('total')).where(Expense.month==months[pairs[1]],Expense.created_at.year==pairs[0])
    month_labels.append(f"{months[pairs[1]]}, {pairs[0]}")
    aggregate.append(0 if ttl[0].total == None else str(ttl[0].total))
  result["Total"] = aggregate

  categories = Category.select().where(Category.user==current_user.id)
  for cat in categories:
    result[cat.name] = _get_category_monthly_total(cat, twelve)

  return render_template(
    'users/dashboard.html', 
    labels = list(data.keys()), 
    data = list(data.values()), 
    month_year = f'{datetime.date.today().strftime("%b")} {current.year}',
    month_labels = month_labels,
    main_values = result,
  )

