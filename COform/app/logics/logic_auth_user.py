from ..dbmodels.dbOperator import DBoperator
from ..dbmodels.models import AuthUser
from ..dbmodels.models import WebHrEmp
import os


class LogicAuthUser:
    def authCode_send(self, data):
        try:
            print(data)
            query_dict = {}
            index = 0
            # for key, value in data.items():
            #     print(key, value)
            records = DBoperator(WebHrEmp).auth_user_query(data)
            print(records)
            for r in records:
                print(r.id)
                print(r.jobstatus)
                print(r.username)
                print(r.depart_name)
                query_dict.update({index: {
                    "id": r.id,
                    "jobstatus": r.jobstatus,
                    "username": r.username,
                    "depart_name": r.depart_name
                }})
                index += 1
            print(query_dict)
            return query_dict
        except Exception as e:
            return str(e), 401