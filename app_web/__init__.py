from app import app
from flask import render_template
from app_web.blueprints.users.views import users_blueprint
from app_web.blueprints.sessions.views import sessions_blueprint
from app_web.blueprints.expenses.views import expenses_blueprint
from app_web.blueprints.reminder.views import reminder_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles
from .util.jinja_filter import register_jinja_filters

register_jinja_filters(app)

assets = Environment(app)
assets.register(bundles)

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(sessions_blueprint, url_prefix="/sessions")
app.register_blueprint(expenses_blueprint, url_prefix="/expenses")
app.register_blueprint(reminder_blueprint, url_prefix="/reminder")

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route("/")
def home():
    return "Home!"
