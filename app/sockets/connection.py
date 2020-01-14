#!/usr/bin/env python
from threading import Lock
from flask_socketio import emit, disconnect
from flask import Flask, session, request, copy_current_request_context
from .. import socketio

languages = ['en', 'es', 'pt-br']

thread = None
thread_lock = Lock()

def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(10)
        count += 1
        socketio.emit('my_response',
                      {'data': 'Server generated event', 'count': count},
                      namespace='/test')

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