#!/bin/env python
from app import create_app, socketio
from app.db import connect_database

connect_database()
app = create_app(debug=True)

if __name__ == '__main__':

    socketio.run(app, debug=True)