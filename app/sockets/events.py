from .. import socketio
from flask_socketio import emit
import json
from flask import session
from . import events_tools

@socketio.on('user_event')
def user_event(form):
    if(isinstance(form, str)):
        form = json.loads(form)
    print('sending message')
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('user_response',
    {'action': form['action'],
    'count': session['receive_count'],
    'data': form['data']
    })

@socketio.on('global_event')
def global_event(form):
    if(isinstance(form, str)):
        form = json.loads(form)
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('global_response',
    {'action': form['action'],
    'count': session['receive_count'],
    'data': form['data']},
    broadcast=True)

@socketio.on('match_event')
def send_room_message(message):
    if(isinstance(form, str)):
        form = json.loads(form)
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('global_response',
    {'action': form['action'],
    'count': session['receive_count'],
    'data': form['data']},
    room=form['match_data']['id'])