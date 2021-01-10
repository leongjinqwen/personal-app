import os
import config
from flask import Flask, request, redirect, url_for, flash
from models.base_model import db
from models.user import User
from flask_login import LoginManager, current_user
import click

web_dir = os.path.join(os.path.dirname(
  os.path.abspath(__file__)), 'app_web')

app = Flask('PERSONAL-MANAGER', root_path=web_dir)

if os.getenv('FLASK_ENV') == 'production':
  app.config.from_object("config.ProductionConfig")
else:
  app.config.from_object("config.DevelopmentConfig")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "sessions.new"
login_manager.login_message = "Please log in before proceeding."
login_manager.login_message_category = "warning"

@login_manager.user_loader
def load_user(user_id):
  return User.get_by_id(int(user_id))

@app.before_request
def before_request():
  db.connect()


@app.teardown_request
def _db_close(exc):
  if not db.is_closed():
    print(db)
    print(db.close())
  return exc

@app.cli.command("email-statement",short_help='Email statement')
def email_statement():
  from app_web.util.mail_helper import create_statement
  from datetime import date
  from calendar import monthrange

  year = date.today().strftime("%Y")
  month = date.today().strftime("%m")
  today = date.today().strftime("%d")
  last_day = monthrange(int(year),int(month))[1]
  if int(today) == last_day:
    print('run email')
    create_statement()
  else:
    print(today,"not last day")

@app.cli.command("seed",short_help='Seed database')
def seed():
  from app_web.util.seed import change_cat
  change_cat()
  print("Seed finish!")

@app.cli.command("statement",short_help='generate statement')
@click.argument('month') # flask statement 2020-12
def statement(month):
  from app_web.util.mail_helper import create_statement

  create_statement(month)
  print(f'generate statement for {month}')

# import logging
# logger = logging.getLogger('peewee')
# logger.addHandler(logging.StreamHandler())
# logger.setLevel(logging.DEBUG)