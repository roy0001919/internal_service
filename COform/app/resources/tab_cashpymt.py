from flask import request
from flask_restful import Resource
from ..logics.logic_cashPymt import Logic_cashPymt
from . import api_bp


class Cashpymt(Resource):
        
    def post(self):
        data = request.json
        result = Logic_cashPymt(data).pymtUnrec_query()
        print(result)
        return result


class cashPymtSend(Resource):

    def post(self):
        data = request.json
        result = Logic_cashPymt(data).cashPymt_send()
        print(result)
        return result