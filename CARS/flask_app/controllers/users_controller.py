from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user_model import User
from flask_app.models.car_model import Car
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


# INITIAL START
@app.route('/')
def landing():
    return render_template('index.html')


# THE DASHBOARD
@app.route('/dashboard')
def dash():
    if not "user_id" in session:
        return redirect('/')
    user_data = {
        'id' : session['user_id']
    }
    logged_user = User.get_by_id(user_data)
    all_cars = Car.get_all()
    return render_template("dashboard.html", logged_user=logged_user, all_cars=all_cars)

# REGISTRATION
@app.route('/users/register', methods=['POST'])
def reg_user():
    if not User.validator(request.form):
        return redirect('/')
    hashbrowns = bcrypt.generate_password_hash(request.form['password'])
    data = {
        **request.form,
        'password': hashbrowns
    }
    new_id = User.create(data)
    session['user_id'] = new_id
    return redirect('/dashboard')

# LOGIN METHOD
@app.route('/users/login', methods=['POST'])
def log_user():
    data = {
        'email': request.form['email']
    }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Credential","log")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Credential **", "log")
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/dashboard')

# LOGOUT METHOD
@app.route('/users/logout')
def logout():
    session.clear()
    return redirect('/')