import os
import config
from flask import Flask
from models.base_model import db
from models.user import User
from flask_login import LoginManager
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
# login_manager.login_view = "sessions.new"

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
    from app_web.util.mail_helper import send_email
    from datetime import date
    from calendar import monthrange

    year = date.today().strftime("%Y")
    month = date.today().strftime("%m")
    today = date.today().strftime("%d")
    last_day = monthrange(int(year),int(month))[1]
    if today == str(last_day):
        print(today)
        send_email()
    else:
        print(today,"not last day")
