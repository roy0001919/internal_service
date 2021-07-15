from flask import Blueprint
models_bp = Blueprint('models_bp', __name__)
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from . import dbOperator
from . import models