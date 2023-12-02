# flask_app/db.py
from flask import g
import pymysql

DB_HOST = '127.0.0.1'
DB_USER = 'jyyang'
DB_PASSWORD = 'didwhdduf'
DB_DATABASE = 'QuizSystemDB'

def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_DATABASE)
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db_connection(app):
    app.teardown_appcontext(close_db)
