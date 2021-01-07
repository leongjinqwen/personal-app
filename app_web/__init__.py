from app import app
from flask import render_template, redirect, url_for
from app_web.blueprints.users.views import users_blueprint
from app_web.blueprints.sessions.views import sessions_blueprint
from app_web.blueprints.expenses.views import expenses_blueprint
from app_web.blueprints.reminders.views import reminders_blueprint
from app_web.blueprints.statements.views import statements_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles
from .util.jinja_filter import register_jinja_filters
import os
import sendgrid
from flask_login import current_user

register_jinja_filters(app)
sg = sendgrid.SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
assets = Environment(app)
assets.register(bundles)

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(sessions_blueprint, url_prefix="/sessions")
app.register_blueprint(expenses_blueprint, url_prefix="/expenses")
app.register_blueprint(reminders_blueprint, url_prefix="/reminders")
app.register_blueprint(statements_blueprint, url_prefix="/statements")

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for('users.dashboard'))
    return render_template('home.html')
