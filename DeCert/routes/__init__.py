from flask import Blueprint

did_bp = Blueprint('did', __name__)

from . import did_routes
