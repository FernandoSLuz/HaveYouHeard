from flask import render_template
from flask import request
from . import http
from .. import socketio
from .. import db
import json
from . import routes_tools
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
    status_code = 0
    callbackDict = {}
    if(routes_tools.check_json(form, ['id']) == False):
        callbackDict = {'feedback': 'missing GET body data'}
        status_code = 406
    else:
        callbackDict = db.querys.get_user(form)
        verification = routes_tools.check_db_callback(callbackDict, 'user found', 'user not found')
        callbackDict = verification[1]
        status_code = verification[0]
    return json.dumps(callbackDict, indent=2, default=str), status_code

@http.route('/add_user', methods=['POST'])
def add_user():
    form = request.get_json(silent=True, force=True)
    status_code = 0
    callbackDict = {}
    if(routes_tools.check_json(form, ['username', 'country']) == False):
        status_code = 406
        callbackDict = {'feedback': 'missing POST body data'}
    else:
        callbackDict = db.querys.add_user(form)
        verification = routes_tools.check_db_callback(callbackDict, 'user created', 'user not created')
        callbackDict = verification[1]
        status_code = verification[0]
    return json.dumps(callbackDict, indent=2, default=str), status_code

@http.route('/get_language', methods=['GET'])
def get_language():
    return 'add_user'

@http.route('/join_match', methods=['POST'])
def join_match():
    form = request.get_json(silent=True, force=True)
    status_code = 0
    callbackDict = {}
    if(routes_tools.check_json(form, ['user_data', 'match_data', 'is_player']) == False):
        status_code = 406
        callbackDict = {'feedback': 'missing POST body data'}
    else:
        callbackDict = db.querys.join_match(form)
        verification = routes_tools.check_db_callback(callbackDict, 'match joined', 'match not joined')
        callbackDict = verification[1]
        status_code = verification[0]
    return json.dumps(callbackDict, indent=2, default=str), status_code

@http.route('/create_match', methods=['POST'])
def create_match():
    form = request.get_json(silent=True, force=True)
    status_code = 0
    callbackDict = {}
    if(routes_tools.check_json(form, ['user_data', 'is_public']) == False):
        status_code = 406
        callbackDict = {'feedback': 'missing POST body data'}
    else:
        callbackDict = db.querys.create_match(form)
        verification = routes_tools.check_db_callback(callbackDict, 'match created', 'match not created')
        callbackDict = verification[1]
        status_code = verification[0]
    return json.dumps(callbackDict, indent=2, default=str), status_code

@http.route('/get_match', methods=['GET'])
def get_match():
    form = request.get_json(silent=True, force=True)
    status_code = 0
    callbackDict = {}
    if(routes_tools.check_json(form, ['id']) == False):
        status_code = 406
        callbackDict = {'feedback': 'missing POST body data'}
    else:
        callbackDict = db.querys.get_match(form)
        verification = routes_tools.check_db_callback(callbackDict, 'match found', 'match not found')
        callbackDict = verification[1]
        status_code = verification[0]
    return json.dumps(callbackDict, indent=2, default=str), status_code
