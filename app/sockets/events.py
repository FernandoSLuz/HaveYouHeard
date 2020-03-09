from .. import socketio
from flask_socketio import emit
import json
from flask import session
from . import events_tools

@socketio.on('user_event')
def user_event(form):
    if(isinstance(form, str)):
        form = json.loads(form)
    session['receive_count'] = session.get('receive_count', 0) + 1
    if(form['action'] == "check_match_status"):
        form['data'] = events_tools.get_match_status(form)
    elif(form['action'] == "send_character_selection"):
        events_tools.process_character_selection(form)
        return
    elif(form['action'] == "news_fulfilled"):
        events_tools.process_news_fulfillment(form)
        return
    elif(form['action'] == "send_vote"):
        events_tools.process_vote_selection(form)
        return
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
def match_event(form):
    if(isinstance(form, str)):
        form = json.loads(form, encoding='utf-8')
    session['receive_count'] = session.get('receive_count', 0) + 1
    data = {}
    if(form['action'] == "user_ready"):
        data = events_tools.user_ready(form)
    elif(form['action'] == "user_selected_character"):
        data = events_tools.add_character_selection(form)
    elif(form['action'] == "characters_voted"):
        data = form['data']
    elif(form['action'] == "news_fulfilled"):
        data = form['data']
    elif(form['action'] == "news_voting_finished"):
        data = form['data']  
    emit('match_response',
    {'action': form['action'],
    'count': session['receive_count'],
    'data': data},
    room=form['data']['match_data']['id'])