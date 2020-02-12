from flask import Blueprint

http = Blueprint('http', __name__)

from . import routes
from . import routes_tools