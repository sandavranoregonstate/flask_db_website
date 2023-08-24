import time
from flask import Blueprint, redirect, render_template, flash, request
from .database import db_connector as db
from .database import script

views_performances = Blueprint('views_performances', __name__)
# connect to database
db_connection = db.connect_to_database()


@views_performances.route('/performances', methods=["POST", "GET"])
def performances():
    if request.method == "POST":
        # grab input
        movie_id = request.form["movie_id"]
        actor_id = request.form["actor_id"]

        # validate - Should refactor
        if len(movie_id) < 1:
            script.flashMessage('Last name', 0, 'error')
        elif len(actor_id) < 1:
            script.flashMessage('Street name', 0, 'error')
        else:
            # add to db
            query = "INSERT INTO Performances (movie_id, actor_id) VALUES (%s, %s)"
            query_params=(movie_id, actor_id)
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=query_params)
            # flash success
            script.flashMessage(crud='create')

    # Default to GET behavior and update table if entry added
    query = "SELECT * FROM Performances;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    result = cursor.fetchall()
    # a potential query2 that populates the dropdown etc.
    return render_template("performances.html", performances=result)

@views_performances.route('/delete_performance/<int:id>')
def delete_performance(id):
    query = "DELETE FROM Performances WHERE performance_id = '%s';"
    db.execute_query(db_connection=db_connection, query=query, query_params=(id,))
    time.sleep(1)
    return redirect("/performances")

@views_performances.route('/edit_performance/<int:id>', methods=["POST", "GET"])
def edit_performance_id(id):

    if request.method == "POST":
        # grab input
        movie_id = request.form["movie_id"]
        actor_id = request.form["actor_id"]
        # validate -- refactor maybe
        if len(movie_id) < 1:
            script.flashMessage('Last name', 0, 'error')
        elif len(actor_id) < 1:
            script.flashMessage('Street name', 0, 'error')
        else:
            # add to db
            query = "UPDATE Performances SET movie_id = %s, actor_id = %s WHERE performance_id = %s"
            query_params=(movie_id, actor_id, id)
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=query_params)
            # flash success
            script.flashMessage(crud='update')
            return redirect('/performances')

    # Default to GET behavior and update table if entry added
    query = "SELECT * FROM Performances WHERE performance_id='%s';"
    cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(id,))
    result = cursor.fetchall()
    # a potential query2 that populates the dropdown etc.
    return render_template("edit/edit_performance.html", performances=result)