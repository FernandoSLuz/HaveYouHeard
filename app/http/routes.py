from flask import render_template
from . import http
from .. import socketio

#async_mode = None

@http.route('/')
def main():
    return 'teste'

@http.route('/app')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)