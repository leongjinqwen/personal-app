from flask import Blueprint, render_template,request,url_for,redirect,flash,jsonify
from models.user import User
from models.statement import Statement
from flask_login import current_user, login_required
import json

statements_blueprint = Blueprint('statements',
                            __name__,
                            template_folder='templates')

@statements_blueprint.route('/', methods=['GET'])
@login_required
def index():
  statements = Statement.select().where(Statement.user==current_user.id).order_by(Statement.created_at.desc())
  return render_template("statements/new.html",statements=statements)




