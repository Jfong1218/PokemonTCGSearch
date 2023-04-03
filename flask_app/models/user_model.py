from flask_app.config.mysqlconnection import connectToMySQL 
from flask_app import DATABASE 
from flask import flash
import re
from flask_app.models import card_model


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod 
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        print (results)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod 
    def get_by_id(cls, data):
        query = "SELECT * FROM users LEFT JOIN favorites ON favorites.user_id = users.id LEFT JOIN cards ON favorites.card_id = cards.id WHERE users.id = %(id)s"
        # query = "SELECT * FROM users WHERE users.id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query,data)
        if len(results) < 1:
            return False
        user = cls(results[0])
        list_of_cards=[]
        for row in results:
            card_data = {
                **row,
                'id':row['cards.id'],
                'created_at':row['cards.created_at'],
                'updated_at':row['cards.updated_at']
            }
            this_card = card_model.Card(card_data)
            list_of_cards.append(this_card)
        user.cards = list_of_cards
        print(user)
        return user

    @classmethod
    def get_id_by_email(cls, data):
        query = "SELECT id FROM user WHERE email = %(email)s"
        results = connectToMySQL(DATABASE).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_password_by_id(cls, data):
        query = "SELECT password FROM user WHERE id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    # @classmethod
    # def update(cls, data):
    #     query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s WHERE id = %(id)s"
    #     return connectToMySQL(DATABASE).query_db(query,data)

    @staticmethod
    def validate(user_data):
        is_valid = True
        if len(user_data['first_name']) <3:
            flash("First name must be at least 3 characters","reg")
            is_valid = False
        if len(user_data['last_name']) <3:
            flash("Last name must be at least 3 characters","reg")
            is_valid = False
        if len(user_data['email']) <1:
            flash("Please provide email","reg")
            is_valid = False
        if len(user_data['password']) <1:
            flash("Please provide password","reg")
            is_valid = False
        elif len(user_data['password']) < 8:
            flash("Password must be at least 8 characters", "reg")
            is_valid = False
        if not EMAIL_REGEX.match(user_data['email']):
            is_valid = False
            flash('invalid email', "reg")
        else:
            potential_user = User.get_by_email({'email': user_data['email']})
            if potential_user: #if we have a user, don't let them register with this email since they exist already
                is_valid = False
                flash("Email already registered", "reg")
        if not user_data['password'] == user_data['confirm_password']:
            flash("Passwords don't match", 'reg')
            is_valid = False
        return is_valid

    @staticmethod
    def validate_login(user_data):
        is_valid = True
        id = User.get_id_by_email(data)
        print(id) #can check from terminal
        if len(id) == 0:
            flash("email or password do not match records")
            is_valid = False
        else:
            data = {
                "id": User.get_id_by_email(data)[0]
            }
            password = User.get_password(data['id'])
            if not bcrypt.check_password_hash(password[0]['password'], data['password']):
                flash("email or password do not match records")
                is_valid = False
        return is_valid

    @staticmethod #for validating when updating user name and email
    def validator(form_data):
        is_valid = True
        if len(form_data['first_name']) <3:
            flash("first name required and cannot be less than 3 characters", 'reg')
            is_valid = False
        if len(form_data['last_name']) <3:
            flash("last name required and cannot be less than 3 characters", 'reg')
            is_valid = False
        if len(form_data['email']) <1:
            flash("Please enter email", 'reg')
            is_valid = False
        if not EMAIL_REGEX.match(form_data['email']):
            is_valid = False
            flash('invalid email', 'reg')
        return is_valid
