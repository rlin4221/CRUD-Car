from flask_app.config.mysqlcontroller import connectToMySQL
from flask_app import DATABASE
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__(self,data) -> None:
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.password = data['password']

# CREATES THE USER IN DATABASE

    @classmethod
    def create(cls,data):
      query = "INSERT INTO users (first_name, last_name, email, password) VALUES "\
        "(%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
      return connectToMySQL(DATABASE).query_db(query,data)

# MAKES SURE THE EMAIL IS INPUTTED CORECT

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        if len(results) > 0:
            return cls(results[0])
        return False

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        if len(results) > 0:
            return cls(results[0])
        return False

# MAKES SURE ALL THE INFO IS CORRECTLY INPUTTED

    @staticmethod
    def validator(potential_user):
        is_valid = True
        if len(potential_user['first_name']) < 3:
            flash("First name is required","reg")
            is_valid = False
        if len(potential_user['last_name']) < 3:
            flash("Last name is required","reg")
            is_valid = False
        if len(potential_user['email']) < 1:
            flash("email is required","reg")
            is_valid = False
        elif not EMAIL_REGEX.match(potential_user['email']):
            flash("email must be valid","reg")
            is_valid = False
        else:
            data = {
              'email': potential_user ['email']
            }
            user_in_db = User.get_by_email(data)
            if user_in_db:
                flash("email already registered","reg")
                is_valid = False
        if len(potential_user['password']) < 8:
            flash("Password must be 8 characters","reg")
            is_valid = False
        elif not potential_user['password'] == potential_user['confirm_pass']:
            flash("double check your password confirmation","reg")
            is_valid = False
        return is_valid