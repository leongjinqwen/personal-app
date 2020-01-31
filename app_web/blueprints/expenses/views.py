from flask import Blueprint, render_template,request,url_for,redirect,flash,jsonify
from models.user import User
from models.expense import Expense
from models.category import Category
from flask_login import current_user
from peewee import fn
from datetime import date
import os
import pdfkit

expenses_blueprint = Blueprint('expenses',
                            __name__,
                            template_folder='templates')


@expenses_blueprint.route('/new', methods=['GET'])
def new():
    categories = Category.select().where(Category.user==current_user.id)
    return render_template('expenses/new.html',categories=categories)


@expenses_blueprint.route('/<user_id>', methods=['POST'])
def create(user_id):
    user = User.get_by_id(user_id)
    expense = Expense(category=request.form.get('category'),amount=request.form.get('amount'),source=request.form.get('source'),description=request.form.get('desc'))
    if expense.save():
        flash("Successfully create expense record.","primary")
        return redirect(url_for('expenses.category',category="all"))
    else:
        flash("Something happened, try again later.","danger")
        categories = Category.select().where(Category.user==current_user.id)
        return render_template('expenses/new.html',categories=categories)

@expenses_blueprint.route('/<category>')
def category(category):
    if current_user.is_authenticated:
        if category == 'all':
            categories = Category.select().where(Category.user==current_user.id)
            expenses = Expense.select().where(Expense.category in categories,Expense.month==date.today().strftime("%b")).order_by(Expense.created_at.asc())
            ttl = Expense.select(fn.SUM(Expense.amount).alias('total')).where(Expense.category in categories,Expense.month==date.today().strftime("%b"))
        else:
            selected = Category.get(Category.name==category.title())
            # categories = Category.select().where(Category.user==current_user.id,Category.name==category.title())
            expenses = Expense.select().where(Expense.category==selected.id,Expense.month==date.today().strftime("%b")).order_by(Expense.created_at.asc())
            ttl = Expense.select(fn.SUM(Expense.amount).alias('total')).where(Expense.category==selected.id,Expense.month==date.today().strftime("%b"))
            print(ttl[0].total)
        return render_template('expenses/show.html',expenses=expenses,ttl=ttl,cat=category.title())
    return render_template('sessions/new.html')  

@expenses_blueprint.route('/edit/<id>',methods=["GET"])
def edit(id):
    expense = Expense.get_by_id(id)
    return render_template('expenses/edit.html',expense=expense)  
    
@expenses_blueprint.route('/<id>/update',methods=["POST"])
def update(id):
    if current_user.is_authenticated:
        expense = Expense.get_by_id(id)
        category = Category.get(Category.name==request.form.get('category'))
        expense.category = category.id
        expense.source = request.form.get('source')
        expense.desc = request.form.get('desc')
        expense.amount = request.form.get('amount')
        if expense.save():
            flash("Successfully update expense record.","primary")
            return redirect(url_for('expenses.edit',id=expense.id))
        else:
            flash("Something happened, try again later.","danger")
            return render_template('expenses/edit.html',expense=expense) 
    return render_template('sessions/new.html')  

@expenses_blueprint.route('/summary',methods=["GET"])
def summary_list():
    months = [] 
    for cat in current_user.categories:
        for expense in cat.expenses:
            if not expense.month in months:
                months.append(expense.month)
    return render_template('expenses/list.html',months=months)

@expenses_blueprint.route('/<month>/summary',methods=["GET"])
def summary(month):
    month_exp = []
    for cat in current_user.categories:
        cat_exp = []
        for expense in cat.expenses:
            if expense.month == month.title():
                cat_exp.append(expense)
        month_exp.append({
            "name":cat.name,
            "expenses":cat_exp
        })
    total = Expense.select().where(Expense.month==month.title())
    return render_template('expenses/summary.html',month_exp=month_exp,month=month,total=total)

 