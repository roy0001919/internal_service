from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_login import LoginManager, UserMixin, current_user
from flask_cors import CORS
from .resources import api_bp
from .dbmodels import models_bp
from .dbmodels.models import db
from . import urls
from config import Config
from functools import wraps
# # DB initialisation
# db=SQLAlchemy()
app = Flask(__name__)
app.config.from_object(Config)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:roy0001919@35.73.233.92/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = True
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'k%x9)k8&z3)yxbj=@-y!vvvx&gxns6bp&(7o_-@u5u+pr+nvpp'

db.init_app(app)

#set CORS
CORS(app, resources={r"/*":{"origins":"*"}})
app.config['CORS_HEADERS'] = 'Cotent-Type'

# register blueprint
app.register_blueprint(api_bp, url_prefix='/api')
app.register_blueprint(models_bp)

# #initialising login manager
# '''This is for the login mechanism'''
# login_manager = LoginManager()
# login_manager.init_app(app)

# #associate the user_id in the cookies to the actual User object
# from .dbmodels.models import User
# @login_manager.user_loader
# def load_user(user_id):
#     user = User.query.filter(self.table.jobstatus == '正式').get(user_id)
#     if not user:
#         return

# def token_required(f):
#     @wraps(f)
#     def decoreated(*args, **kwargs):
#         token = None
#         if 'x-access-token' in request.headers:
#             token = request.headers['x-access-token']
#         if not token:
#             return jsonify({'message':'Token is missing!'})
#         try:
#             data = jwt.decode(token, app.config['SECRET_KEY'])
#             current_user = User.query.filter_by(id=data['id']).first()
#         except:
#             return jsonify({'message':'Token is invalid!'}),401
#         return f(current_user, *args, **kwargs)
#     return decoreated