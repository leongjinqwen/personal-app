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
  return render_template("statements/new.html",statements=statements)




