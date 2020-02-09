from .. import socketio
import json
from flask_socketio import join_room, join_room, leave_room, close_room, rooms, emit
from flask import session
from . import events_tools

@socketio.on('join', namespace='/haveYouHeard')
def join(form):
    print("JOINING ----------------------------")
    if(isinstance(form, str)):
        form = json.loads(form)
    join_room(form['match_data']['id'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    data = {
        'user_data': form['user_data'],
        'match_data': form['match_data'],
        'match_user_data': form['match_user_data']
    }
    emit('match_response',
         {'action': 'user_joined ' + ', '.join(rooms()),
          'count': session['receive_count'],
          'data': data
    })

@socketio.on('leave', namespace='/haveYouHeard')
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

@socketio.on('close_room', namespace='/haveYouHeard')
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