import time
from flask import Blueprint, redirect, render_template, flash, request
from .database import db_connector as db
from .database import script

views_movies = Blueprint('views_movies', __name__)
# connect to database
db_connection = db.connect_to_database()


@views_movies.route('/movies', methods=["POST", "GET"])
def movies():
    if request.method == "POST":
        # grab input
        title = request.form["title"]
        stock = request.form["stock"]
        price = request.form["price"]
        # validate -- refactor maybe
        if len(title) < 2:
            script.flashMessage('Title', 1, 'error')
        elif len(stock) < 1:
            script.flashMessage('Stock', 1, 'error')
        elif len(price) < 1:
            script.flashMessage('Price', 1, 'error')
        else:
            # add to db
            query = "INSERT INTO Movies (title, stock, price) VALUES (%s, %s, %s)"
            query_params=(title, stock, price)
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=query_params)
            # flash success
            script.flashMessage(crud='create')

    # Default to GET behavior and update table if entry added
    query = "SELECT * FROM Movies;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    result = cursor.fetchall()
    # a potential query2 that populates the dropdown etc.
    return render_template("movies.html", movies=result)

@views_movies.route('/delete_movie/<int:id>')
def delete_movie(id):
    query = "DELETE FROM Movies WHERE movie_id = '%s';"
    db.execute_query(db_connection=db_connection, query=query, query_params=(id,))
    time.sleep(1)
    return redirect("/movies")

@views_movies.route('/edit_movie/<int:id>', methods=["POST", "GET"])
def edit_movie_id(id):

    if request.method == "POST":
        # grab input
        title = request.form["title"]
        stock = request.form["stock"]
        price = request.form["price"]
        # validate -- refactor maybe
        if len(title) < 2:
            script.flashMessage('Title', 1, 'error')
        elif len(stock) < 1:
            script.flashMessage('Stock', 1, 'error')
        elif len(price) < 1:
            script.flashMessage('Price', 1, 'error')
        else:
            # add to db
            query = "UPDATE Movies SET title = %s, stock = %s, price = %s WHERE movie_id = %s"
            query_params=(title, stock, price, id)
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=query_params)
            # flash success
            script.flashMessage(crud='update')
            return redirect('/movies')

    # Default to GET behavior and update table if entry added
    query = "SELECT * FROM Movies WHERE movie_id='%s';"
    cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(id,))
    result = cursor.fetchall()
    # a potential query2 that populates the dropdown etc.
    return render_template("edit/edit_movie.html", movies=result)