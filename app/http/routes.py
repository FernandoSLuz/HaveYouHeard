from flask import render_template
from flask import request
from . import http
from .. import socketio
from .. import db
import json
#async_mode = None

@http.route('/')
def main():
    return 'teste'

@http.route('/app')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

@http.route('/get_user', methods=['GET'])
def get_user():
    form = request.get_json(silent=True, force=True)
    db.querys.get_user(form['id'])
    if('id' not in form or form['id'] == ""):
        callbackDict = {'feedback': 'missing GET body data'}
        return json.dumps(callbackDict), 406
    else:
        callbackDict = db.querys.get_user(form['id'])
        if(callbackDict['query_successful'] == True):
            callbackDict['feedback'] = 'user found'
        else:
            callbackDict['feedback'] = 'user not found'
        return json.dumps(callbackDict, indent=2, default=str)

@http.route('/add_user', methods=['POST'])
def add_user():
    form = request.get_json(silent=True, force=True)
    if('username' not in form or form['username'] == ""):
        callbackDict = {'feedback': 'missing POST body data'}
        return json.dumps(callbackDict), 406
    else:
        callbackDict = db.querys.add_user(form['username'])
        if(callbackDict['query_successful'] == True):
            callbackDict['feedback'] = 'user created'
        else:
            callbackDict['feedback'] = 'user not created'
        return json.dumps(callbackDict, indent=2, default=str)

@http.route('/get_language', methods=['GET'])
def get_language():
    return 'add_user'