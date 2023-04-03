from flask_app.config.mysqlconnection import connectToMySQL 
from flask_app import DATABASE 
from flask import flash
from flask_app.models import user_model

class Card:
    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create(cls, data):
        query = "INSERT INTO cards (title, user_id, card_id) JOIN favorites ON cards.id = favorites.card_id VALUES (%(title)s, %(card_id)s,%(user_id)s);"
        return connectToMySQL(DATABASE).query_db(query,data)

    # not needed since we're not implementing magazine update functions
    # @classmethod
    # def update(cls, data):
    #     query = "UPDATE magazines SET title = %(title)s, description = %(description)s WHERE id = %(id)s"
    #     return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod #returns all cards by all users
    def get_all(cls):
        query = "SELECT * FROM cards JOIN favorites ON cards.id = favorites.card_id JOIN users ON users.id = favorites.user_id;"
        results = connectToMySQL(DATABASE).query_db(query)
        if results:
            all_cards = []
            for row in results:
                this_card = cls(row)
                user_data = {
                    **row,
                    'id': row['users.id'],
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at']
                }
                this_user = user_model.User(user_data)
                this_card.planner = this_user
                all_cards.append(this_card)
            return all_cards
        return results

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM cards JOIN favorites ON cards.id = favorites.card_id JOIN users ON users.id = favorites.user_id WHERE cards.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        if len(results) < 1:
            return False
        row = results[0]
        this_card = cls(row)
        user_data = {
            **row,
            'id': row['users.id'],
            'created_at': row['users.created_at'],
            'updated_at': row['users.updated_at']
        }   
        planner = user_model.User(user_data)
        this_card.planner = planner
        return this_card

    @classmethod #need this method because get_by_id only returns 1 card and i need a list for the my_cards page
    def get_all_by_id(cls, data):
        query = "SELECT * FROM cards JOIN favorites ON cards.id = favorites.user_id JOIN users ON users.id = favorites.user_id WHERE users.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        if results:
            all_cards = []
            for row in results:
                this_card = cls(row)
                user_data = {
                    **row,
                    'id': row['users.id'],
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at']
                }
                this_user = user_model.User(user_data)
                this_card.planner = this_user
                all_cards.append(this_card)
            return all_cards
        return results

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM cards WHERE id = %(id)s"
        return connectToMySQL(DATABASE).query_db(query,data)

    @staticmethod
    def validator(form_data):
        is_valid = True
        if len(form_data['title']) <2:
            flash("Title requeired and cannot be less than 2 characters")
            is_valid = False
        # if len(form_data['description']) <10:
        #     flash("Description required and cannot be less than 10 characters")
        #     is_valid = False
        return is_valid

