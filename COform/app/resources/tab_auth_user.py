from flask import request
from flask_restful import Resource
from ..logics.logic_auth_user import LogicAuthUser
from . import api_bp


class AuthUser(Resource):

    def post(self):
        data = request.json
        result = LogicAuthUser().authCode_send(data)
        print(result)
        return result