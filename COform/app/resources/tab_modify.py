from flask import request
from flask_restful import Resource
from ..logics.logic_modify import Logic_Mod
from . import api_bp

class COformMods(Resource):
    def post(self):
        data = request.json
        index = 0
        if len(data) > 10:
            return "超過修改筆數限制，一次最多只能修改10筆，拒絕存取",403
        for item in data["data"]:
            index += 1
            if index > 0 and index <= 9:
                sequence = "00%s" % index
                print(sequence)
                item["mod_id"] += sequence
            elif index >= 10 and index <= 99:
                sequence = "0%s" % index
                print(sequence)
            elif index >= 100 and index <= 999:
                sequence = "%s" % index
                print(sequence)
            try:
                print('processing the modify logic \n')
                test = Logic_Mod(item).insert_COform()
            except Exception as e:
                return 'error', 500
        return '資料修改完成', 200


