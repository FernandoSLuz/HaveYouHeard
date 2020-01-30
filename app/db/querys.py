import psycopg2
from psycopg2.extras import RealDictCursor
import datetime as dt
conn = None
import json

def query(cur, command, data, multiple):

    try:
        cur.execute(command, data)
        conn.commit()
        query_result = cur.fetchall() if multiple else cur.fetchone()
        cur.close()
        return { 'query_successful': True, 'query_message': 'query successful', 'data' : query_result}
    except Exception as e: 
        cur.close()
        return { 'query_successful': False, 'query_message': str(e)}

def add_user(username):
    cur = conn.cursor(cursor_factory=RealDictCursor)
    command = "INSERT INTO users (username, created_at) VALUES(%s, %s) RETURNING id,username,created_at;"
    data = (username, dt.datetime.now(),)
    return query(cur, command, data, False)

def get_user(user_id):
    cur = conn.cursor(cursor_factory=RealDictCursor)
    command = "SELECT * FROM users WHERE id  = %s;"
    data = (user_id,)
    return query(cur, command, data, False)

def update_user():
    print('get user query')

