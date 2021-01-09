from flask import Blueprint, render_template,request,url_for,redirect,flash,jsonify
from models.user import User
from models.reminder import Reminder
from flask_login import current_user, login_required
from peewee import fn
from datetime import date

reminders_blueprint = Blueprint('reminders',
                            __name__,
                            template_folder='templates')

@reminders_blueprint.before_request
@login_required
def before_request():
  pass

@reminders_blueprint.route('/new', methods=['GET'])
def new():
  return render_template('reminders/new.html')


@reminders_blueprint.route('/<user_id>', methods=['POST'])
def create(user_id):
  user = User.get_by_id(user_id)
  if request.form.get('dateRequired') == "on":
    reminder = Reminder(user=user.id,group=request.form.get('group'),description=request.form.get('desc'),dateline=request.form.get('dateline'))
  else:
    reminder = Reminder(user=user.id,group=request.form.get('group'),description=request.form.get('desc'))

  if reminder.save():
    flash("Successfully add reminder.","primary")
    return redirect(url_for('reminders.show',group="all"))
  else:
    flash("Something happened, try again later.","danger")
    return render_template('reminders/new.html')

@reminders_blueprint.route('/<group>', methods=['GET'])
def show(group):
  if current_user.is_authenticated:
    if group == 'all':
      reminders = Reminder.select().where(Reminder.user==current_user.id).order_by(Reminder.created_at.asc())
    else:
      reminders = Reminder.select().where(Reminder.group==group.title(),Reminder.user==current_user.id).order_by(Reminder.created_at.asc())
    return render_template('reminders/show.html',reminders=reminders)
  return render_template('reminders/new.html')

@reminders_blueprint.route('/<id>/edit', methods=['POST'])
def edit(id):
  reminder = Reminder.get_by_id(id)
  reminder.status = not reminder.status
  if reminder.save():
    flash("Successfully update.","primary")
    return redirect(url_for('reminders.show',group=reminder.group.lower()))
  else:
    flash("Something happened, try again later.","danger")
    return render_template('reminders/show.html',reminders=reminders)