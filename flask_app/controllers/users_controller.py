from crypt import methods
from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_bcrypt import Bcrypt
from flask_app.models.user_model import User
from flask_app.models.card_model import Card

bcrypt = Bcrypt(app)

#bcrypt.generate_password_hash(password_string)
#bcrypt.check_password_hash(hashed_password, password_string)

@app.route('/')
def index():
    # if "user_id" in session:
    #     return redirect("/")
    return render_template('index.html')

@app.route('/welcome')
def welcome():
    if not "user_id" in session:
        return redirect("/")
    user = User.get_by_id({'id': session['user_id']})
    all_cards = Card.get_all()
    return render_template('welcome.html', user = user)

@app.route("/users/register", methods=["POST"])
def register():
    if not User.validate(request.form):
        return redirect('/')
    hashed_pw = bcrypt.generate_password_hash(request.form['password'])
    data = {
        **request.form,
        'password': hashed_pw
    }
    session['user_id'] = User.create(data)
    return redirect('/welcome')

@app.route("/users/search")
def search():
    if not "user_id" in session:
        return redirect("/")
    return render_template("search.html")

@app.route("/users/logout")
def logout():
    del session['user_id']
    return redirect('/')

@app.route("/users/login", methods=['POST'])
def login():
    data = {
        'email': request.form['email']
    }
    user_from_db = User.get_by_email(data)
    if not user_from_db:
        flash("Invalid credentials", "log")
        return redirect('/')
    if not bcrypt.check_password_hash(user_from_db.password, request.form['password']):
        flash("Invalid credentials", "log")
        return redirect('/')
    session['user_id'] = user_from_db.id
    flash("User credentials provided are great thank you so much", "success")
    return redirect('/welcome')

@app.route("/users/<int:id>/update", methods=['POST'])
def update_user(id):
    if not 'user_id' in session:
        return redirect("/")
    if not User.validator(request.form):
        return redirect(f"/my_magazines")
    data = {
        **request.form,
        'id': session['user_id']
    }
    User.update(data)
    return redirect("/welcome")

# @app.route("/my_magazines")
# def my_magazines():
#     if not "user_id" in session:
#         return redirect("/")
#     user = User.get_by_id({'id':session['user_id']})
#     magazines = Magazine.get_all_by_id({'id':session['user_id']})
#     return render_template("my_magazines.html", user = user, magazines = magazines)
