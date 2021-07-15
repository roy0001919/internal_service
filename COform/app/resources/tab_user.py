from flask import request, make_response, jsonify, current_app
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash
from ..logics.logic_coform import Logic_coform
# from ..dbmodels.models import User
from . import api_bp
import jwt
import datetime

class Login(Resource):
    def get(self):
        auth = request.authorization
        print("username: "+auth.username+" /n password: "+auth.password)
        if not auth or not auth.username:
            return make_response('無法驗證', 401, {'www-Authenticate' : 'Basic realm="Login Required!"'})

        user = User.query.filter_by(id=auth.username).first()
        print (user)
        if not user:
            return make_response('無法驗證', 401, {'www-Authenticate' : 'Basic realm="Could not find corresponding user to the id supplied!"'})
        print(check_password_hash(generate_password_hash('smarterAPIpwd!@'), auth.password))
        if check_password_hash(generate_password_hash('smarterAPIpwd!@'), auth.password):
            token = jwt.encode({'id':user.id, 'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=30)}, current_app.config['SECRET_KEY'])
            print(token)
            return jsonify ({'token': token})
        
        return make_response('無法驗證', 401, {'www-Authenticate' : 'Basic realm="Couldn not login!"'})