from flask import Blueprint, render_template,request,url_for,redirect,flash,jsonify
from models.user import User
from models.statement import Statement
from flask_login import current_user
import json

statements_blueprint = Blueprint('statements',
                            __name__,
                            template_folder='templates')

@statements_blueprint.route('/', methods=['GET'])
def index():
    statements = Statement.select().where(Statement.user==current_user.id)
    months = []
    for s in statements:
      months.append(s.month)
    return render_template("statements/new.html",statements=statements)


@statements_blueprint.route('/<month>', methods=['GET'])
def show(month):
    statement = Statement.get_or_none(Statement.month==month,Statement.user==current_user.id)
    if statement:
      return jsonify({
        "ok": True,
        "exp_url": statement.exp_url,
      })    
    else:
      return jsonify({
        "ok": False,
        "exp_url": '',
      })    




