import sqlite3

conn = sqlite3.connect("todos.sqlite")

cursor = conn.cursor()
sql_query = """ CREATE TABLE todo (
    id integer PRIMARY KEY,
    name text NOT NULL,
    description text NOT NULL,
    currency text NOT NULL
)"""
cursor.execute(sql_query)