from flask import request
from flask_restful import Resource
from ..logics.logic_daily import Logic_daily
from . import api_bp


class DailyOPT(Resource):
    def post(self):
        data = request.json
        result = Logic_daily(data).daily_send()
        print(result)
        return result


class DailyOPTLastTen(Resource):
    def post(self):
        data = request.json
        result = Logic_daily(data).daily_lastTen()
        print(result)
        return result