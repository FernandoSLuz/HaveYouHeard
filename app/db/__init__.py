from flask import Blueprint
import psycopg2

from . import querys

db = Blueprint('db', __name__)
conn = None

def connect_database():
    try:
        conn = psycopg2.connect("dbname='d2v31g70cbfnt4' user='vqguereszarywj' host='ec2-107-20-185-16.compute-1.amazonaws.com' password='0c3d928894c1266f42284913df056801b902a92fb42ec3bc4213ea58991ee2d8'")
        print ("connected to database")
        querys.conn = conn
    except:
        print ("I am unable to connect to the database")