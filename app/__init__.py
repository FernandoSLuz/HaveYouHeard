from flask import Flask
from flask_socketio import SocketIO
import psycopg2
from flask_cors import CORS

socketio = SocketIO()

def create_app(debug=False):
    """Create an application."""
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})
    app.debug = debug
    app.config['SECRET_KEY'] = 'gjr39dkjn344_!67#'

    from .http import http as http_blueprint
    from .sockets import sockets as sockets_blueprint
    app.register_blueprint(http_blueprint)
    app.register_blueprint(sockets_blueprint)

    socketio.init_app(app)
    return app





