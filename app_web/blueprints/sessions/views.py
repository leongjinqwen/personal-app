from flask import Blueprint, render_template,request,url_for,redirect,flash,jsonify
from models.user import User
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_required,logout_user,login_user,current_user

sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates')


@sessions_blueprint.route('/new', methods=['GET'])
def new():
    if current_user.is_authenticated:
        return redirect(url_for('users.show',username=current_user.username))
    else:
        return render_template('sessions/new.html')


@sessions_blueprint.route('/', methods=['POST'])
def create():
    user = User.get_or_none(User.email == request.form['email'])
    if user :
        password_to_check = request.form['password']
        hashed_password = user.password
        result = check_password_hash(hashed_password, password_to_check)
        if result :
            login_user(user)
            flash("Successfully logged in.",'link')
            return redirect(url_for('users.dashboard'))
        else:
            flash("Please fill in valid username and password.",'danger')
            return render_template('sessions/new.html')

@sessions_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('sessions.new'))
