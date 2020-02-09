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
        print("error")
        return { 'query_successful': False, 'query_message': str(e)}

def add_user(form):
    cur = conn.cursor(cursor_factory=RealDictCursor)
    command = "INSERT INTO users (username, country, created_at) VALUES(%s, %s, %s) RETURNING id,username,country,created_at;"
    data = (form['username'], form['country'], dt.datetime.now(),)
    return query(cur, command, data, False)

def get_user(form):
    cur = conn.cursor(cursor_factory=RealDictCursor)
    command = "SELECT * FROM users WHERE id  = %s;"
    data = (form['id'],)
    return query(cur, command, data, False)

def update_user():
    print('get user query')

def create_match(form):
    cur = conn.cursor(cursor_factory=RealDictCursor)
    command = "INSERT INTO matches (is_public, status, country, created_at) VALUES(%s, %s, %s, %s) RETURNING id, is_public, status, country, created_at;"
    data = (form['is_public'], 'finding_users',form['user_data']['country'], dt.datetime.now(),)
    return query(cur, command, data, False)

def join_match(form):
    cur = conn.cursor(cursor_factory=RealDictCursor)
    command = "INSERT INTO match_users (id_user, id_match, is_player, won, created_at) VALUES(%s, %s, %s, %s, %s) RETURNING id, id_user, id_match, is_player, won, created_at;"
    data = (form['user_data']['id'], form['match_data']['id'], form['is_player'], False, dt.datetime.now(),)
    return query(cur, command, data, False)

def get_match(form):
    cur = conn.cursor(cursor_factory=RealDictCursor)
    command = "SELECT * FROM matches WHERE id  = %s;"
    data = (form['id'],)
    return query(cur, command, data, False)

