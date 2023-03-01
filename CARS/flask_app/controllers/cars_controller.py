from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user_model import User
from flask_app.models.car_model import Car

# ADDS A NEW CAR

@app.route('/cars/new')
def new_car_form():
    return render_template("car_new.html")

@app.route('/cars/create', methods=['POST'])
def create_car():
    if 'user_id' not in session:
        return redirect('/')
    if not Car.validator(request.form):
        return redirect('/cars/new')
    data = {
      **request.form,
      'user_id': session['user_id']
    }
    id = Car.create(data)
    return redirect('/dashboard')

# DISPLAY CAR BY THEIR USER ID (VIEW THEM)

@app.route('/cars/<int:id>')
def one_car(id):
    if 'user_id' not in session:
        return redirect('/')
    this_car = Car.get_by_id({'id':id})
    return render_template("car_one.html", this_car=this_car)

# EDITS THE CAR THAT BELONGS TO THE USER ID

@app.route('/cars/<int:id>/edit')
def edit_car(id):
    if 'user_id' not in session:
        return redirect('/')
    this_car = Car.get_by_id({'id':id})
    return render_template("car_edit.html", this_car=this_car)

# UPDATES IT

@app.route('/cars/<int:id>/update', methods=['POST'])
def update_car(id):
    if not Car.validator(request.form):
        return redirect(f'/cars/{id}/edit')
    car_data = {
        **request.form,
        'id':id
    }
    Car.update(car_data)
    return redirect('/dashboard')

# THIS DELTES THE CAR FROM DATABASE W/ BACKEND VALIDATION 

@app.route('/cars/<int:id>/delete')
def delete_car(id):
    Car.delete({'id':id})
    return redirect('/dashboard')