from flask import request
from flask_restful import Resource
from ..logics.logic_coform import Logic_coform
from . import api_bp


class COform(Resource):
    def post(self):
        data = request.json
        print(data)
        # result = "ok"
        result = Logic_coform(data).insert()
        print ("COform POST method. The data is: "+str(data))
        print (result)
        return result


class COformSearchOpen(Resource):
    def post(self):
        data = request.json
        # id is required for such operations
        result = Logic_coform(data).coform_search_open()
        return result

