#!/usr/bin/env python
from threading import Lock
from flask import Flask, render_template, session, request, \
    copy_current_request_context
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
import json
# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()

class my_room:
    name = ""
    my_players = []
    def __init__(self, name, username, user_id):
        self.name = name
        self.my_players.append(my_player(username, user_id))
class my_player:
    username = ""
    user_id = ""
    def __init__(self, username, user_id):
        self.username = username
        self.user_id = user_id

my_rooms = []

# def add_room():
#     break;
def add_player(room_name, user_id, username):
    if(len(my_rooms) == 0):
        my_rooms.append(my_room(user_id, username, user_id));
        return;
    for actual_room in my_rooms:
        if(actual_room.name == room_name):
            for actual_player in actual_room.my_players:
                if(actual_player.user_id == user_id):
                    return;
    my_rooms.append(my_room(user_id, username, user_id));
def remove_player(username, room_name):
    if(len(my_rooms) > 0):
        for actual_room in my_rooms:
            if(actual_room.name == room_name):
                for num, actual_player in enumerate(actual_room.my_players, start = 0):
                    if(actual_player.username == username):
                        actual_room.my_players.pop(num);

def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(10)
        count += 1
        socketio.emit('my_response',
                      {'data': 'Server generated event', 'count': count},
                      namespace='/test')

@app.route('/')
def main():
    return 'teste'

@app.route('/app')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


@socketio.on('my_event', namespace='/haveYouHeard')
def test_message(message):
    if(isinstance(message, str)):
        message = json.loads(message)
    username = "unknown"
    if 'username' in message:
        username = message['username']
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count'], 'username': username})


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
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count'], 'username': username},
         broadcast=True)


@socketio.on('join', namespace='/haveYouHeard')
def join(message):
    if(isinstance(message, str)):
        message = json.loads(message)
    username = "unknown"
    if 'username' in message:
        username = message['username']
    join_room(message['room'])
    add_player(rooms()[1], rooms()[0], username)
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count'], 'username': username})


@socketio.on('leave', namespace='/haveYouHeard')
def leave(message):
    if(isinstance(message, str)):
        message = json.loads(message)
    username = "unknown"
    if 'username' in message:
        username = message['username']
    leave_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count'], 'username': username})


@socketio.on('close_room', namespace='/haveYouHeard')
def close(message):
    if(isinstance(message, str)):
        message = json.loads(message)
    username = "unknown"
    if 'username' in message:
        username = message['username']
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response', {'data': 'Room ' + message['room'] + ' is closing.',
                         'count': session['receive_count'], 'username': username},
         room=message['room'])
    close_room(message['room'])


@socketio.on('my_room_event', namespace='/haveYouHeard')
def send_room_message(message):
    if(isinstance(message, str)):
        message = json.loads(message)
    username = "unknown"
    if 'username' in message:
        username = message['username']
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count'], 'username': username},
         room=message['room'])


@socketio.on('disconnect_request', namespace='/haveYouHeard')
def disconnect_request():
    @copy_current_request_context
    def can_disconnect():
        disconnect()

    session['receive_count'] = session.get('receive_count', 0) + 1
    # for this emit we use a callback function
    # when the callback function is invoked we know that the message has been
    # received and it is safe to disconnect
    emit('my_response',
         {'data': 'Disconnected!', 'count': session['receive_count']},
         callback=can_disconnect)


@socketio.on('my_ping', namespace='/haveYouHeard')
def ping_pong():
    emit('my_pong')


@socketio.on('connect', namespace='/haveYouHeard')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)
    emit('my_response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect', namespace='/haveYouHeard')
def test_disconnect():
    print('Client disconnected', request.sid)


if __name__ == '__main__':
    socketio.run(app, debug=True)
