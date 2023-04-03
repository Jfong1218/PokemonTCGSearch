from crypt import methods
from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.user_model import User
from flask_app.models.card_model import Card


@app.route('/cards/new')
def new_card_form():
    if not 'user_id' in session:
        return redirect("/")
    user = User.get_by_id({"id": session['user_id']})
    return render_template('card_new.html', user=user)

@app.route("/cards/create", methods=['POST'])
def create_card():
    if not 'user_id' in session:
        return redirect("/")
    if not Card.validator(request.form):
        return redirect("/cards/new")
    print(request.form)
    data = {
        **request.form,
        'user_id': session['user_id']
    }
    Card.create(data)
    return redirect("/welcome")

@app.route('/cards/<int:id>/edit')
def edit_card_form(id):
    if not 'user_id' in session:
        return redirect("/")
    card = Card.get_by_id({"id": id})
    return render_template('magazine_edit.html', card = card)

# this block of code not needed since wireframe did not call for magazine edits
# @app.route("/magazines/<int:id>/update", methods=['POST'])
# def update_magazine(id):
#     if not 'user_id' in session:
#         return redirect("/")
#     if not Card.validator(request.form):
#         return redirect(f"/magazines/{id}/edit")
#     data = {
#         **request.form,
#         'id': id
#     }
#     Card.update(data)
#     return redirect("/welcome")

@app.route("/cards/<id>/delete")
def delete_card(id):
    if not "user_id" in session:
        return redirect(("/"))
    data = {
        "id": id
    }
    # to_be_deleted = Card.get_by_id(data)
    #not on exam but good to know
    # if not session['user_id'] == to_be_deleted.user_id:
    #     flash("Quit Trying to delete other people's stuff")
    #     return redirect('/')
    Card.delete(data)
    return redirect('/welcome')

@app.route("/cards/<int:id>")
def show_one_card(id):
    print(id)
    if not "user_id" in session:
        return redirect('/')
    data = {
        'id': id
    }
    card = Card.get_by_id(data)
    return render_template("card_one.html", card=card)