from flask import Blueprint, url_for, redirect, flash, request
from models.user import User
from models.category import Category
from flask_login import current_user, login_required

categories_blueprint = Blueprint('categories',
                            __name__,
                            template_folder='templates')


@categories_blueprint.before_request
@login_required
def before_request():
  pass

@categories_blueprint.route('/create', methods=['POST'])
def create():
  if len(current_user.categories) < 10:
    category = Category(user=current_user.id, name=request.form['name'])
    if category.save():
      flash("Category created.", "primary")
    else:
      flash("Something went wrong, try again later.", "danger")
  else:
    flash("Your category limit is reached, consider delete or combine other category to proceed.", "danger")
  return redirect(url_for('users.show', username=current_user.username))


@categories_blueprint.route('/<id>', methods=['POST'])
def update(id):
  category = Category.get_or_none(id=id)
  category.name = request.form['name']
  if category.save():
    flash("Category updated.", "primary")
  else:
    flash("Something went wrong, try again later.", "danger")
  return redirect(url_for('users.show', username=current_user.username))


@categories_blueprint.route('/<id>/delete', methods=['POST'])
def destroy(id):
  q = Category.delete().where(Category.id == id)
  if q.execute():
    flash("Category deleted.", "primary")
  else:
    flash("Something went wrong, try again later.", "danger")
  return redirect(url_for('users.show', username=current_user.username))


