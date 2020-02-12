from .. import socketio
import json
from flask_socketio import join_room, join_room, leave_room, close_room, rooms, emit
from flask import session
from . import events_tools

@socketio.on('join')
def join(form):
    if(isinstance(form, str)):
        form = json.loads(form)
    print("joining")
    join_room(form['match_data']['id'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    events_tools.user_joined(form)
    data = events_tools.get_match_info(form['match_data']['id'])
    print(data)
    emit('match_response',
         {'action': 'join_match',
          'count': session['receive_count'],
          'data': data
    })

@socketio.on('leave')
def leave(form):
    if(isinstance(form, str)):
        form = json.loads(form)
    leave_room(form['match_data']['id'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('match_response',
         {'action': 'user_left ' + ', '.join(rooms()),
          'count': session['receive_count'],
          'data': form['user_data']
    })

@socketio.on('close_room')
def close(form):
    if(isinstance(form, str)):
        form = json.loads(form)
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('match_response',
         {'action': 'match_closed - ' + str(form['match_data']['id']),
          'count': session['receive_count'],
          'data': ''
    }, room=form['match_data']['id'])
    close_room(form['match_data']['id'])