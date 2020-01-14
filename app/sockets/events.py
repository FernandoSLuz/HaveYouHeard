from .. import socketio
from flask_socketio import emit
import json
from flask import session

@socketio.on('my_event', namespace='/haveYouHeard')
def test_message(message):
    if(isinstance(message, str)):
        message = json.loads(message)
    username = "unknown"
    if 'username' in message:
        username = message['username']
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response', {'data': message['data'], 'count': session['receive_count'], 'username': username})


@socketio.on('my_broadcast_event', namespace='/haveYouHeard')
def test_broadcast_message(message):
    if(isinstance(message, str)):
        message = json.loads(message)
    username = "unknown"
    if 'username' in message:
        username = message['username']
    session['receive_count'] = session.get('receive_count', 0) + 1
    print(type(message))
    print({'data': message['data']})
    emit('my_response', {'data': message['data'], 'count': session['receive_count'], 'username': username},
         broadcast=True)


@socketio.on('my_room_event', namespace='/haveYouHeard')
def send_room_message(message):
    if(isinstance(message, str)):
        message = json.loads(message)
    username = "unknown"
    if 'username' in message:
        username = message['username']
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response', {'data': message['data'], 'count': session['receive_count'], 'username': username},
         room=message['room'])