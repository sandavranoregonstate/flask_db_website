import time
from flask import Blueprint, redirect, render_template, flash, request
from .database import db_connector as db
from .database import script

#TODO: Implement off of the views_employee.py file.

views_order_items = Blueprint('views_order_items', __name__)
# connect to database
db_connection = db.connect_to_database()

@views_order_items.route('/order_items', methods=["POST", "GET"])
def order_items():
    if request.method == "POST":
        # grab input
        order_selection = request.form["order_selection"]
        movie_selection = request.form["movie_selection"]
        quantity = request.form["quantity"]
        # validate - Should refactor
        # check for duplicate composite key
        querycheck = "SELECT * FROM Order_items WHERE order_id=%s AND movie_id=%s;"
        query_params=(order_selection, movie_selection)
        cursorcheck = db.execute_query(db_connection=db_connection, query=querycheck, query_params=query_params)
        checkdup = cursorcheck.fetchall()

        if len(checkdup) == 1:
            script.flashMessage(message='Duplicate entry! Check table!', crud='custom')
        elif int(quantity) <= 0:
            script.flashMessage('Quantity', 0, 'error')
        else:
            # add to db
            query = "INSERT INTO Order_items (order_id, movie_id, quantity) VALUES (%s, %s, %s)"
            query_params=(order_selection, movie_selection, quantity)
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=query_params)
            # flash success
            script.flashMessage(crud='create')

    # Default to GET behavior and update table if entry added
    query1 = """SELECT Order_items.order_id, Order_items.movie_id,
                CONCAT_WS(', ', Movies.title, Movies.price) AS 'Movie Detail', 
                Order_items.quantity
                FROM Order_items
                INNER JOIN Movies ON Movies.movie_id=Order_items.movie_id;
            """
    cursor = db.execute_query(db_connection=db_connection, query=query1)
    result = cursor.fetchall()
    query2 = "SELECT Orders.order_id FROM Orders"
    cursor2 = db.execute_query(db_connection=db_connection, query=query2)
    result2 = cursor2.fetchall()
    query3 = "SELECT Movies.title, Movies.movie_id FROM Movies"
    cursor3 = db.execute_query(db_connection=db_connection, query=query3)
    result3 = cursor3.fetchall()

    return render_template("order_items.html", order_items=result, dropdown_order=result2, dropdown_movie=result3)

@views_order_items.route('/delete_order_item/<int:id>/<int:id2>')
def delete_order(id, id2):
    query = "DELETE FROM Order_items WHERE Order_items.order_id = '%s' AND Order_items.movie_id = '%s';"
    db.execute_query(db_connection=db_connection, query=query, query_params=(id, id2))
    time.sleep(1)
    return redirect("/order_items")

@views_order_items.route('/edit_order_items/<int:id>/<int:id2>', methods=["POST", "GET"])
def edit_order_id(id, id2):

    if request.method == "POST":
        # grab input
        order_selection = request.form["order_selection"]
        movie_selection = request.form["movie_selection"]
        quantity = request.form["quantity"]
        # validate - Should refactor
        # check for duplicate composite key
        querycheck = "SELECT * FROM Order_items WHERE order_id=%s AND movie_id=%s;"
        query_params=(order_selection, movie_selection)
        cursorcheck = db.execute_query(db_connection=db_connection, query=querycheck, query_params=query_params)
        checkdup = cursorcheck.fetchall()

        if len(checkdup) == 1 and not (int(order_selection) == int(id) and int(movie_selection) == int(id2)):
            script.flashMessage(message='Duplicate entry! Check table!', crud='custom')
        elif int(quantity) <= 0:
            script.flashMessage('Quantity', 0, 'error')
        else:
            # add to db
            query = "UPDATE Order_items SET order_id = %s, movie_id = %s, quantity = %s WHERE order_id = %s AND movie_id = %s"
            query_params=(order_selection, movie_selection, quantity, id, id2)
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=query_params)
            # flash success
            script.flashMessage(crud='update')
            return redirect('/order_items')

    # Default to GET behavior and update table if entry added
    query = """SELECT Order_items.order_id, Order_items.movie_id,
                CONCAT_WS(', ', Movies.title, Movies.price) AS 'Movie Detail', 
                Order_items.quantity
                FROM Order_items
                INNER JOIN Movies ON Movies.movie_id=Order_items.movie_id
                WHERE Order_items.movie_id=%s AND Order_items.order_id='%s;'
            """
    cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(id2, id))
    result = cursor.fetchall()
    query2 = "SELECT Orders.order_id FROM Orders"
    cursor2 = db.execute_query(db_connection=db_connection, query=query2)
    result2 = cursor2.fetchall()
    query3 = "SELECT Movies.title, Movies.movie_id FROM Movies"
    cursor3 = db.execute_query(db_connection=db_connection, query=query3)
    result3 = cursor3.fetchall()
    # a potential query2 that populates the dropdown etc.
    return render_template("edit/edit_order_items.html", order_items=result, dropdown_order=result2, dropdown_movie=result3)