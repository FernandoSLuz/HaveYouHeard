from .. import socketio
import json
from flask_socketio import join_room, join_room, leave_room, close_room, rooms, emit
from flask import session

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

def add_player(room_name, user_id, username):
    if(len(my_rooms) == 0):
        my_rooms.append(my_room(user_id, username, user_id))
        return
    for actual_room in my_rooms:
        if(actual_room.name == room_name):
            for actual_player in actual_room.my_players:
                if(actual_player.user_id == user_id):
                    return
    my_rooms.append(my_room(user_id, username, user_id))
def remove_player(username, room_name):
    if(len(my_rooms) > 0):
        for actual_room in my_rooms:
            if(actual_room.name == room_name):
                for num, actual_player in enumerate(actual_room.my_players, start = 0):
                    if(actual_player.username == username):
                        actual_room.my_players.pop(num)

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