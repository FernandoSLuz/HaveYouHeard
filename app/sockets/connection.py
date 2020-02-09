#!/usr/bin/env python
from threading import Lock
from flask_socketio import emit, disconnect
from flask import Flask, session, request, copy_current_request_context
from .. import socketio

thread = None
thread_lock = Lock()

def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(10)
        count += 1
        socketio.emit('user_response',
                      {'data': 'Server generated event', 'count': count})

@socketio.on('disconnect_request')
def disconnect_request():
    @copy_current_request_context
    def can_disconnect():
        disconnect()

    session['receive_count'] = session.get('receive_count', 0) + 1
    # for this emit we use a callback function
    # when the callback function is invoked we know that the message has been
    # received and it is safe to disconnect
    emit('user_response',
         {'action': 'connection',
         'count': session['receive_count'],
         'data': {'status' : 'disconnected'}
         },
         callback=can_disconnect)

@socketio.on('my_ping')
def ping_pong():
    emit('my_pong')

@socketio.on('connect')
def test_connect():

    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)
    # received and it is safe to disconnect
    emit('user_event',
         {'action': 'connection',
         'count' : 0,
         'data': 'connected'
         })

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected', request.sid)