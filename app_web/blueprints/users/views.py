from flask import Blueprint, render_template,request,url_for,redirect,flash,jsonify
from models.user import User
from flask_login import login_required,login_user,current_user

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    user_password = request.form['password']
    user = User(username=request.form['username'].lower(),email=request.form['email'].lower(),password=user_password)
    if user.save():
        login_user(user)
        flash("Successfully signed up and logged in.","primary")
        return redirect(url_for('users.show',username=user.username))
    else:
        for error in user.errors:
            flash(error,"danger")
        return render_template('users/new.html')


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    return render_template('users/show.html',username=username)


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
