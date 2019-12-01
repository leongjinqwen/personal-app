from flask import Blueprint, render_template,request,url_for,redirect,flash,jsonify
from models.user import User
from models.expense import Expense
from flask_login import current_user
from peewee import fn
from datetime import date

expenses_blueprint = Blueprint('expenses',
                            __name__,
                            template_folder='templates')


@expenses_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('expenses/new.html')


@expenses_blueprint.route('/<user_id>', methods=['POST'])
def create(user_id):
    user = User.get_by_id(user_id)
    expense = Expense(user=user.id,category=request.form.get('category'),amount=request.form.get('amount'),source=request.form.get('source'),description=request.form.get('desc'))
    if expense.save():
        flash("Successfully create expense record.","primary")
        return redirect(url_for('users.show',username=user.username))
    else:
        flash("Something happened, try again later.","danger")
        return render_template('expenses/new.html')

@expenses_blueprint.route('/<category>')
def category(category):
    if current_user.is_authenticated:
        if category == 'all':
            expenses = Expense.select().where(Expense.user==current_user.id,Expense.month==date.today().strftime("%b"))
            new_list = []
            ttl = Expense.select(fn.SUM(Expense.amount).alias('total')).where(Expense.user==current_user.id,Expense.month==date.today().strftime("%b"))
        else:
            expenses = Expense.select().where(Expense.user==current_user.id,Expense.category==category.title(),Expense.month==date.today().strftime("%b"))
            ttl = Expense.select(fn.SUM(Expense.amount).alias('total')).where(Expense.user==current_user.id,Expense.category==category.title(),Expense.month==date.today().strftime("%b"))
            print(ttl[0].total)
        return render_template('expenses/show.html',expenses=expenses,ttl=ttl,cat=category.title())
    return render_template('expenses/new.html')  

