from flask import Blueprint

docs = Blueprint("docs", __name__)

from . import routes
