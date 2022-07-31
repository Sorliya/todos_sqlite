from flask import Flask, request, jsonify
import json
import sqlite3

app = Flask(__name__)


def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("todos.sqlite")
    except sqlite3.error as e:
        print(e)
    return conn


@app.route("/todos", methods=["GET", "POST"])
def todos():
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == "GET":
        cursor = conn.execute("SELECT * FROM todo")
        todos = [
            dict(id=row[0], name=row[1], description=row[2], currency=row[3])
            for row in cursor.fetchall()
        ]
        if todos is not None:
            return jsonify(todos)

    if request.method == "POST":
        new_name = request.form["name"]
        new_description = request.form["description"]
        new_currency = request.form["currency"]
        sql = """INSERT INTO todo (name, description, currency)
                 VALUES (?, ?, ?)"""
        cursor = cursor.execute(sql, (new_name, new_description, new_currency))
        conn.commit()
        return f"Todo with the id: {cursor.lastrowid} created successfully", 201


@app.route("/todo/<int:id>", methods=["GET", "PUT", "DELETE"])
def single_todo(id):
    conn = db_connection()
    cursor = conn.cursor()
    todo = None
    if request.method == "GET":
        cursor.execute("SELECT * FROM todo WHERE id=?", (id,))
        rows = cursor.fetchall()
        for r in rows:
            todo = r
        if todo is not None:
            return jsonify(todo), 200
        else:
            return "Something wrong", 404

    if request.method == "PUT":
        sql = """UPDATE todo
                SET name=?,
                    description=?,
                    currency=?
                WHERE id=? """

        name = request.form["name"]
        description = request.form["description"]
        currency = request.form["currency"]
        updated_todo = {
            "id": id,
            "name": name,
            "description": description,
            "currency": currency,
        }
        conn.execute(sql, (name, description, currency, id))
        conn.commit()
        return jsonify(updated_todo)

    if request.method == "DELETE":
        sql = """ DELETE FROM todo WHERE id=? """
        conn.execute(sql, (id,))
        conn.commit()
        return "The todo with id: {} has been deleted.".format(id), 200


if __name__ == "__main__":
    app.run(debug=True)